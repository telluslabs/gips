#!/usr/bin/env python
################################################################################
#    GIPS: Geospatial Image Processing System
#
#    AUTHOR: Matthew Hanson
#    EMAIL:  matt.a.hanson@gmail.com
#
#    Copyright (C) 2014-2018 Applied Geosolutions
#
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program. If not, see <http://www.gnu.org/licenses/>
################################################################################

import os
import sys
import errno
from osgeo import gdal, ogr
from datetime import datetime, timedelta
import glob
import re
from itertools import groupby
from shapely.wkt import loads
import tarfile
import zipfile
import json
import traceback
import ftplib
import shutil
import commands
from urllib import urlencode
import urllib2
from cookielib import CookieJar
import argparse

# from functools import lru_cache <-- python 3.2+ can do this instead
from backports.functools_lru_cache import lru_cache
import requests
import backoff

import gippy
from gippy.algorithms import CookieCutter
from gips import __version__
from gips.utils import (settings, VerboseOut, RemoveFiles, File2List, List2File, Colors,
        basename, mkdir, open_vector)
from gips import utils
from ..inventory import dbinv, orm


"""
The data.core classes are the base classes that are used by individual Data modules.
For a new dataset create children of Repository, Asset, and Data
"""

gippy_index_product_glossary = (
    ('ndvi',   'Normalized Difference Vegetation Index'),
    ('evi',    'Enhanced Vegetation Index'),
    ('lswi',   'Land Surface Water Index'),
    ('ndsi',   'Normalized Difference Snow Index'),
    ('bi',     'Brightness Index'),
    ('satvi',  'Soil-Adjusted Total Vegetation Index'),
    ('msavi2', 'Modified Soil-adjusted Vegetation Index'),
    ('vari',   'Visible Atmospherically Resistant Index'),
    ('brgt',   'VIS and NIR reflectance, weighted by solar energy distribution.'),
    # index products related to tillage
    ('ndti',   'Normalized Difference Tillage Index'),
    ('crc',    'Crop Residue Cover (uses BLUE)'),
    ('crcm',   'Crop Residue Cover, Modified (uses GREEN)'),
    ('isti',   'Inverse Standard Tillage Index'),
    ('sti',    'Standard Tillage Index'),
)

def add_gippy_index_products(p_dict, p_groups, a_types):
    """Add index products to a driver's Data._products & _productgroups."""
    p_groups['Index'] = [i for (i, _) in gippy_index_product_glossary]
    p_dict.update(
        (p, {'description': d,
             'assets': a_types,
             'bands': [{'name': p, 'units': Data._unitless}]}
         ) for p, d in gippy_index_product_glossary)

def _gs_stop_trying(e):
    """Should backoff keep retrying based on this HTTPError?
    
    For searching using backoff per GCP docs:
    Clients should use truncated exponential backoff for all requests
    to Cloud Storage that return HTTP 5xx and 429 response codes,
    including uploads and downloads of data or metadata.
    """
    return (e.response is not None
            and e.response.status_code != 429
            and (499 < e.response.status_code < 600))


class GoogleStorageMixin(object):
    """Mix this into a class (probably Asset) to use data in google storage.

    The class should set gs_bucket_name.
    """
    _gs_query_url_base = 'https://www.googleapis.com/storage/v1/b/{}/o'
    _gs_object_url_base = 'http://storage.googleapis.com/{}/'

    @classmethod
    @backoff.on_exception(backoff.expo,
                          requests.exceptions.RequestException,
                          max_time=120,
                          giveup=_gs_stop_trying)
    def gs_api_search(cls, prefix, delimiter='/'):
        """Convenience wrapper for searching in google cloud storage."""
        params = {'prefix': prefix}
        if delimiter is not None:
            params['delimiter'] = delimiter
        r = requests.get(cls._gs_query_url_base.format(cls.gs_bucket_name),
                         params=params)
        r.raise_for_status()
        return r.json()

    @classmethod
    def gs_object_url_base(cls):
        """Return the google store URL for the driver's bucket."""
        return cls._gs_object_url_base.format(cls.gs_bucket_name)

    @classmethod
    def gs_vsi_prefix(cls, streaming=False):
        """Generate the first part of a VSI path for gdal."""
        vsi_magic_string = '/vsicurl_streaming/' if streaming else '/vsicurl/'
        return vsi_magic_string + cls.gs_object_url_base()

    @classmethod
    def gs_stage_asset(cls, basename, urls):
        """Write the urls as json to the given basename in the stage."""
        stage_dn = cls.Repository.path('stage')
        with utils.make_temp_dir(prefix='fetch', dir=stage_dn) as tmp_dir:
            tmp_fp = tmp_dir + '/' + basename
            with open(tmp_fp, 'w') as tfo:
                json.dump(urls, tfo)
            shutil.copy(tmp_fp, stage_dn)

    @classmethod
    @backoff.on_exception(backoff.expo,
                              requests.exceptions.RequestException,
                              max_time=120,
                              giveup=_gs_stop_trying)
    def gs_backoff_downloader(cls, src, dst, chunk_size=512 * 1024):
        r = requests.get(src, stream=True)# NOTE the stream=True
        r.raise_for_status()
        with open(dst, 'wb') as f:
            for chunk in r.iter_content(chunk_size=chunk_size):
                if chunk: # filter out keep-alive new chunks
                    f.write(chunk)

    @classmethod
    def _cache_if_vsicurl(cls, filelist, tmpdir):
        '''Google Storage-based assets use vsicurl paths.  This method will
        download GS objects to a local dir, and returns the resulting list of
        geo_image paths.  There is certainly some cleanup to be done with this,
        but it works for now.
        '''
        ofiles = []
        for i in filelist:
            if i.startswith('/vsicurl/'):
                dest_path = os.path.join(tmpdir, os.path.basename(i))
                cls.gs_backoff_downloader(i[9:], dest_path)
                ofiles.append(dest_path)
            else:
                ofiles.append(i)
        return ofiles


def validate_s3_env_vars():
    vs = set(['AWS_SECRET_ACCESS_KEY', 'AWS_ACCESS_KEY_ID'])
    missing = tuple(vs - set(os.environ.keys()))
    if len(missing) > 0:
        raise EnvironmentError(
            "Missing AWS S3 auth credentials:  {}".format(missing))


# TODO mixin with one not-really-classmethod is not a mixin at all
class S3Mixin(object):
    """Mix this into a subclass of Asset to use data in AWS S3.

    <subclass requirements go here>
    """
    @classmethod
    @lru_cache(maxsize=1)
    def s3_prefix_search(cls, prefix):
        validate_s3_env_vars()
        # find the layer and metadata files matching the current scene
        import boto3 # import here so it only breaks if it's actually needed
        s3 = boto3.resource('s3')
        bucket = s3.Bucket(cls._s3_bucket_name)
        keys = [o.key for o in bucket.objects.filter(Prefix=prefix)]
        utils.verbose_out("Found {} S3 keys while searching for for key fragment"
                    " '{}'".format(len(keys), prefix), 5)
        return keys



class Repository(object):
    """ Singleton (all classmethods) of file locations and sensor tiling system  """
    # Description of the data source
    description = 'Data source description'
    # Format code of date directories in repository
    _datedir = '%Y%j'
    # attribute holding the tile id
    _tile_attribute = 'tile'
    # valid sub directories in repo
    _subdirs = ['tiles', 'stage', 'quarantine', 'composites']

    default_settings = {}

    @classmethod
    def feature2tile(cls, feature):
        """ Get tile designation from a geospatial feature (i.e. a row) """
        fldindex = feature.GetFieldIndex(cls._tile_attribute)
        return str(feature.GetField(fldindex))


    ##########################################################################
    # Override these functions if not using a tile/date directory structure
    ##########################################################################
    @classmethod
    def data_path(cls, tile='', date=''):
        """ Get absolute data path for this tile and date """
        path = cls.path('tiles')
        if tile != '':
            path = os.path.join(path, tile)
        if date != '':
            path = os.path.join(path, str(date.strftime(cls._datedir)))
        return path

    @classmethod
    def find_tiles(cls):
        """Get list of all available tiles for the current driver."""
        if orm.use_orm():
            return dbinv.list_tiles(cls.name.lower())
        return os.listdir(cls.path('tiles'))

    @classmethod
    def find_dates(cls, tile):
        """ Get list of dates available in repository for a tile """
        if orm.use_orm():
            return dbinv.list_dates(cls.name.lower(), tile)
        tdir = cls.data_path(tile=tile)
        if os.path.exists(tdir):
            return sorted([datetime.strptime(os.path.basename(d), cls._datedir).date() for d in os.listdir(tdir)])
        else:
            return []

    @classmethod
    def validate_setting(cls, key, value):
        """Override this method to validate settings.

        Validation, for this purpose, includes transformations,
        such as changing types.
        """
        return value

    ##########################################################################
    # Child classes should not generally have to override anything below here
    ##########################################################################
    @classmethod
    def get_setting(cls, key):
        """Get given setting from settings.REPOS[driver].

        If the key isn't found, it attempts to load a default from
        cls.default_settings, a dict of such things.  If still not found,
        resorts to magic for 'driver' and 'tiles', ValueError otherwise.
        """
        dataclass = cls.__name__[:-10] # name of a class, not the class object
        r = settings().REPOS[dataclass]
        if key in r:
            return cls.validate_setting(key, r[key])
        if key in cls.default_settings:
            return cls.default_settings[key]

        # not in settings file nor default, so resort to magic
        exec('import gips.data.%s as clsname' % dataclass)
        driverpath = os.path.dirname(clsname.__file__)
        if key == 'driver':
            return driverpath
        if key == 'tiles':
            return os.path.join(driverpath, 'tiles.shp')
        raise ValueError("'{}' is not a valid setting for"
                         " {} driver".format(key, cls.name))

    @classmethod
    def managed_request(cls, url, verbosity=1, debuglevel=0):
        """Visit the given http URL and return the response.

        Uses auth settings and cls._manager_url, and also follows custom
        weird redirects (specific to Earthdata servers seemingly).
        Returns urllib2.urlopen(...), or None if errors are encountered.
        debuglevel is ultimately passed in to httplib; if >0, http info,
        such as headers, will be printed on standard out.
        """
        username = cls.get_setting('username')
        password = cls.get_setting('password')
        manager_url = cls._manager_url
        password_manager = urllib2.HTTPPasswordMgrWithDefaultRealm()
        password_manager.add_password(
            None, manager_url, username, password)
        cookie_jar = CookieJar()
        opener = urllib2.build_opener(
            urllib2.HTTPBasicAuthHandler(password_manager),
            urllib2.HTTPHandler(debuglevel=debuglevel),
            urllib2.HTTPSHandler(debuglevel=debuglevel),
            urllib2.HTTPCookieProcessor(cookie_jar))
        urllib2.install_opener(opener)
        try: # try instead of error handler because the exceptions have funny values to unpack
            request = urllib2.Request(url)
            response = urllib2.urlopen(request)
            redirect_url = response.geturl()
            # some data centers do it differently
            if "redirect" in redirect_url: # TODO is this the right way to detect redirects?
                utils.verbose_out('Redirected to ' + redirect_url, 3)
                redirect_url += "&app_type=401"
                request = urllib2.Request(redirect_url)
                response = urllib2.urlopen(request)
            return response
        except urllib2.URLError as e:
            utils.verbose_out('{} gave bad response: {}'.format(url, e.reason),
                              verbosity, sys.stderr)
            return None
        except urllib2.HTTPError as e:
            utils.verbose_out('{} gave bad response: {} {}'.format(url, e.code, e.reason),
                              verbosity, sys.stderr)
            return None

    @classmethod
    def path(cls, subdir=''):
        """ Paths to repository: valid subdirs (tiles, composites, quarantine, stage) """
        return os.path.join(cls.get_setting('repository'), subdir)


    @classmethod
    def vector2tiles(cls, vector, pcov=0.0, ptile=0.0, tilelist=None):
        """ Return matching tiles and coverage % for provided vector """
        from osgeo import ogr, osr

        # open tiles vector
        v = open_vector(cls.get_setting('tiles'))
        shp = ogr.Open(v.Filename())
        if v.LayerName() == '':
            layer = shp.GetLayer(0)
        else:
            layer = shp.GetLayer(v.LayerName())

        # create and warp site geometry
        ogrgeom = ogr.CreateGeometryFromWkt(vector.WKT())
        srs = osr.SpatialReference(vector.Projection())
        trans = osr.CoordinateTransformation(srs, layer.GetSpatialRef())
        ogrgeom.Transform(trans)
        # convert to shapely
        geom = loads(ogrgeom.ExportToWkt())

        # find overlapping tiles
        tiles = {}
        layer.SetSpatialFilter(ogrgeom)
        layer.ResetReading()
        feat = layer.GetNextFeature()
        while feat is not None:
            tgeom = loads(feat.GetGeometryRef().ExportToWkt())
            if tgeom.intersects(geom):
                area = geom.intersection(tgeom).area
                if area != 0:
                    tile = cls.feature2tile(feat)
                    tiles[tile] = (area / geom.area, area / tgeom.area)
            feat = layer.GetNextFeature()

        # remove any tiles not in tilelist or that do not meet thresholds for % cover
        remove_tiles = []
        if tilelist is None:
            tilelist = tiles.keys()
        for t in tiles:
            if (tiles[t][0] < (pcov / 100.0)) or (tiles[t][1] < (ptile / 100.0)) or t not in tilelist:
                remove_tiles.append(t)
        for t in remove_tiles:
            tiles.pop(t, None)
        return tiles


class Asset(object):
    """ Class for a single file asset (usually an original raw file or archive) """
    Repository = Repository

    # Sensors
    _sensors = {
        # Does the data have multiple sensors possible for each asset? If not, a single sensor may be fine
        '': {'description': ''},
    }
    # dictionary of assets
    _assets = {
        '': {
            'pattern': r'.+',
        }
    }

    # TODO - move to be per asset ?
    _defaultresolution = [30.0, 30.0]

    def __init__(self, filename):
        """ Inspect a single file and populate variables. Needs to be extended """
        # full filename to asset
        self.filename = filename
        # the asset code
        self.asset = ''
        # tile designation
        self.tile = ''
        # full date
        self.date = datetime(1858, 4, 6)
        # sensor code (key used in cls.sensors dictionary)
        self.sensor = ''
        # dictionary of existing products in asset {'product name': [filename(s)]}
        self.products = {}
        # gips interpretation of the version of the asset
        # (which may differ from 'version' already used by some drivers)
        self._version = 1

    def sensor_spec(self, *keys):
        """Return one or more entries from the current asset's sensor dict.

        Returns a single value if len(keys) == 1, a list otherwise."""
        s = self._sensors[self.sensor]
        return s[keys[0]] if len(keys) == 1 else [s[k] for k in keys]

    def atd_str(self):
        return 'ATD {} {} {}'.format(
            self.asset, self.tile, self.date.strftime('%Y%j'))

    @classmethod
    def get_setting(cls, key):
        """Convenience method to acces Repository's get_setting."""
        return cls.Repository.get_setting(key)

    def updated(self, newasset):
        '''
        Return:
            'newasset' and existing represent the same data (time,space,sensor)
            AND
            'newasset' _version greater than existing _version.

        '''
        return (self.asset == newasset.asset and
                self.sensor == newasset.sensor and
                self.tile == newasset.tile and
                self.date == newasset.date and
                self._version < newasset._version)


    def version_text(self):
        """string representation of the asset version.

        Example overrides include:
            prism: D1-early D2-early D2-provisional D2-stable
            landsat: T1-YYYYMMDD
        """
        return str(self._version)


    def get_geometry(self):
        """Get the geometry of the asset

        For tiled assets, this will return the geometry of the tile in the
        respective 'tiles.shp' file as WKT. Needs to be extended for
        untiled assets.
        """
        # If tileID is a number, drop leading 0
        try:
            tile_num = int(self.tile)
        except:
            tile_num = self.tile

        v = gippy.GeoVector(self.get_setting("tiles"))
        v.SetPrimaryKey(self.Repository._tile_attribute)
        # If a GeoVector is indexed with an int, it queries using
        # FID field.
        feat = v[str(tile_num)]
        return feat.WKT()

    ##########################################################################
    # Child classes should not generally have to override anything below here
    ##########################################################################
    @classmethod
    def _quarantine_file(cls, filepath, error):
        """if problem with a file, move to quarantine"""
        #TODO: make this ORM compatible
        error.tb_text = traceback.format_exc()
        utils.report_error(error, 'Quarantining ' + filepath)
        qname = os.path.join(cls.Repository.path('quarantine'), os.path.basename(filepath))
        if not os.path.exists(qname):
            os.link(os.path.abspath(filepath), qname)

    def parse_asset_fp(self):
        """Parse self.filename using the class's asset patterns.

        On the first successful match, the re lib match object is
        returned. Raises ValueError on failure to parse.
        """
        asset_bn = os.path.basename(self.filename)
        for av in self._assets.values():
            match = re.match(av['pattern'], asset_bn)
            if match is not None:
                return match
        raise ValueError("Unparseable asset file name:  " + self.filename)

    def datafiles(self):
        """Get list of readable datafiles from asset.

        A 'datafile' in this context is a file contained within the
        asset file, such as for tar, zip, and hdf files.

        In the case of JSON files, the files pointed to are considered 'within'
        the JSON asset."""
        path = os.path.dirname(self.filename)
        indexfile = os.path.join(path, self.filename + '.index')
        if os.path.exists(indexfile):
            datafiles = File2List(indexfile)
            if len(datafiles) > 0:
                return datafiles
        with utils.error_handler('Problem accessing asset(s) in ' + self.filename):
            if tarfile.is_tarfile(self.filename):
                datafiles = tarfile.open(self.filename).getnames()
            elif zipfile.is_zipfile(self.filename):
                datafiles = zipfile.ZipFile(self.filename).namelist()
            elif self.filename.endswith('json'):
                # take strings at the top level, or in lists at the top level
                # TODO this is brittle; drivers implementing json assets
                # should override this method to handle their specific needs
                with open(self.filename) as fp:
                    content = json.load(fp)
                raw_df = []
                for v in content.values():
                    raw_df += v if type(v) is list else [v]
                datafiles = tuple(v.encode('ascii', 'ignore')
                                  for v in raw_df if isinstance(v, basestring))
            else: # Try subdatasets
                fh = gdal.Open(self.filename)
                datafiles = [s[0] for s in fh.GetSubDatasets()]

            # if we found files, record them to save work later:
            if len(datafiles) > 0:
                List2File(datafiles, indexfile)
                return datafiles
            return [self.filename]


    def extract(self, filenames=tuple(), path=None):
        """Extract given files from asset (if it's a tar or zip).

        Extracted files are placed in the same dir as the asset file.  Returns
        a list of extracted files, plus any files that were not extracted due
        to prior existence.
        """
        if tarfile.is_tarfile(self.filename):
            try:
                open_file = tarfile.open(self.filename)
            except tarfile.TarError as te:
                self._quarantine_file(self.filename, te)
                raise Exception('corrupt asset tarfile (has been quarantined): {}'.format(self.filename))

        elif zipfile.is_zipfile(self.filename):
            try:
                open_file = zipfile.ZipFile(self.filename)
            except zipfile.BadZipfile as zfe:
                self._quarantine_file(self.filename, zfe)
                raise Exception('corrupt asset zipfile (has been quarantined): {}'.format(self.filename))
        else:
            raise Exception('%s is not a valid tar or zip file' % self.filename)
        if not path:
            path = os.path.dirname(self.filename)
        if len(filenames) == 0:
            filenames = self.datafiles()
        extracted_fnames, extant_fnames = [], []

        with utils.make_temp_dir(prefix='extract', dir=path) as tmp_dn:
            utils.verbose_out("Extracting files from {} to {}".format(
                self.filename, tmp_dn), 3)
            for f in filenames:
                final_fname = os.path.join(path, f)
                if os.path.exists(final_fname):
                    utils.verbose_out(f + ' exists, not extracting', 3)
                    extant_fnames.append(final_fname)
                    continue
                utils.verbose_out("Extracting " + f, 3)
                open_file.extract(f, tmp_dn)
                tmp_fname = os.path.join(tmp_dn, f)
                # this ensures we have permissions on extracted files
                if not os.path.isdir(tmp_fname):
                    os.chmod(tmp_fname, 0664)
                extracted_fnames.append((tmp_fname, final_fname))
            if extracted_fnames:
                utils.verbose_out("Moving files from {} to {}".format(tmp_dn, path), 3)
            else:
                utils.verbose_out("No files to extract or move", 3)
            for (tfn, ffn) in extracted_fnames:
                # tfn's parent dir may be earlier in the list
                if not os.path.exists(ffn):
                    utils.mkdir(os.path.dirname(ffn))
                    os.rename(tfn, ffn)

        return extant_fnames + [ffn for (_, ffn) in extracted_fnames]

    cloud_storage_a_types = () # override in subclass as needed

    def in_cloud_storage(self):
        """Is this asset's data fetched from the cloud on-demand?"""
        return self.asset in self.cloud_storage_a_types

    ##########################################################################
    # Class methods
    ##########################################################################
    @classmethod
    def discover(cls, tile, date, asset=None):
        """Factory function returns list of Assets for this tile and date.

        Looks in the inventory for this, either the database or the
        filesystem depending on configuration.

        tile:   A tile string suitable for the current class(cls) ie
                'h03v19' for modis
        date:   datetime.date object to limit search in temporal dimension
        asset:  Asset type string, eg for modis could be 'MCD43A2'
        """
        a_types = cls._assets.keys() if asset is None else [asset]
        found = [cls.discover_asset(a, tile, date) for a in a_types]
        return [a for a in found if a is not None] # lastly filter Nones

    @classmethod
    def discover_asset(cls, asset_type, tile, date):
        """Finds an asset for the a-t-d trio and returns an object for it."""
        if orm.use_orm():
            # search for ORM Assets to use for making GIPS Assets
            results = dbinv.asset_search(driver=cls.Repository.name.lower(),
                                    asset=asset_type, tile=tile, date=date)
            if len(results) == 0:
                return None
            assert len(results) == 1 # sanity check; DB should enforce
            return cls(results[0].name)

        # The rest of this fn uses the filesystem inventory
        d_path = cls.Repository.data_path(tile, date)
        if not os.path.isdir(d_path):
            return None
        files = utils.find_files(cls._assets[asset_type]['pattern'], d_path)
        # Confirm only one asset
        if len(files) > 1:
            raise IOError("Duplicate(?) assets found: {}".format(files))
        if len(files) == 1:
            return cls(files[0])
        return None


    @classmethod
    def start_date(cls, asset):
        """Get starting date for this asset type."""
        return cls._assets[asset]['startdate']

    @classmethod
    def end_date(cls, asset):
        """Get ending date for this asset.

        One of 'enddate' or 'latency' must be present in
        cls._assets[asset]. Returns either the enddate, or else a
        computation of the most recently-available data, based on the
        (today's date) - asset's known latency.
        """
        a_info = cls._assets[asset]
        if 'enddate' in a_info:
            return a_info['enddate']
        return datetime.now().date() - timedelta(a_info['latency'])

    @classmethod
    def available(cls, asset, date):
        """Check availability of an asset for given date.

        Accepts both dates and datetimes for the `date` parameter."""
        d = date.date() if type(date) is datetime else date
        return cls.start_date(asset) <= d <= cls.end_date(asset)

    # TODO - combine this with fetch to get all dates
    @classmethod
    def dates(cls, asset_type, tile, dates, days):
        """For a given asset type get all dates possible (in repo or not).

        Also prunes dates outside the bounds of the asset's valid date range,
        as given by start_date and end_date.
        """
        # TODO tile arg isn't used
        from dateutil.rrule import rrule, DAILY
        req_start_dt, req_end_dt = dates

        # if the dates are outside asset availability dates, use those instead
        a_start_dt = cls.start_date(asset_type)
        a_end_dt   = cls.end_date(asset_type)
        start_dt = a_start_dt if a_start_dt > req_start_dt else req_start_dt
        end_dt   = a_end_dt   if a_end_dt   < req_end_dt   else req_end_dt

        # degenerate case:  There is no valid date range; notify user
        if start_dt > end_dt:
            utils.verbose_out("For {}, requested dates, {} - {},"
                              " are not in the valid range of {} - {}.".format(
                                    asset_type, req_start_dt, req_end_dt,
                                    a_start_dt, a_end_dt))
            return []
        utils.verbose_out('Computed date range for processing: {} - {}'.format(
                start_dt, end_dt), 5)

        # default assumes daily regardless of asset or tile
        datearr = rrule(DAILY, dtstart=start_dt, until=end_dt)
        dates = [dt for dt in datearr if days[0] <= int(dt.strftime('%j')) <= days[1]]
        return dates

    @classmethod
    def query_provider(cls, asset, tile, date):
        """Query the data provider for files matching the arguments.

        Drivers must override this method or else query_service. Must
        return (filename, url), or (None, None) if nothing found. This
        method has a more convenient return value for drivers that never
        find multiple files for the given (asset, tile, date), and don't
        need to unpack a nested data structure in their fetch methods.
        """
        raise NotImplementedError('query_provider not supported for' + cls.__name__)

    @classmethod
    @lru_cache(maxsize=100) # cache size chosen arbitrarily
    def query_service(cls, asset, tile, date, **fetch_kwargs):
        """Query the data provider for files matching the arguments.

        Drivers must override this method, or else query_provider, to contact a
        data source regarding the given arguments, and report on whether
        anything is available for fetching. Must return a dict containing an
        available asset filename.  The dict is passed to the driver's
        Asset.fetch method so additional data can be passed along in other
        keys. When nothing is available, must return None.
        """
        if not cls.available(asset, date):
            return None
        utils.verbose_out('querying ATD {} {} {}'.format(asset, tile, date), 5)
        bn, url = cls.query_provider(asset, tile, date, **fetch_kwargs)
        utils.verbose_out('queried ATD {} {} {}, found {} at {}'.format(
                          asset, tile, date, bn, url), 5)
        if (bn, url) == (None, None):
            return None
        return {'basename': bn, 'url': url}

    @classmethod
    def download(cls, url, download_fp, **kwargs):
        """Override this method to provide custom download code."""
        raise NotImplementedError('download not supported for ' + cls.__name__)

    @classmethod
    def stage_asset(cls, asset_full_path):
        """Copy the given asset to the stage."""
        stage_full_path = os.path.join(cls.Repository.path('stage'),
                                       os.path.basename(asset_full_path))
        os.rename(asset_full_path, stage_full_path) # atomic on POSIX
        return stage_full_path

    @classmethod
    def fetch(cls, a_type, tile, date, **fetch_kwargs):
        """Standard fetch method; calls query_service() and download().

        Outputs from query_service and fetch_kwargs are passed in to
        download as kwargs, so one can talk to the other in a standard
        way.
        """
        qs_rv = cls.query_service(a_type, tile, date, **fetch_kwargs)
        if qs_rv is None:
            return []
        stage_dir_fp = cls.Repository.path('stage')
        if os.path.exists(os.path.join(stage_dir_fp, qs_rv['basename'])):
            utils.verbose_out('Asset `{}` needed but already in stage/,'
                              ' skipping.'.format(qs_rv['basename']))
            return []
        with utils.make_temp_dir(prefix='fetch-', dir=stage_dir_fp) as td_fp:
            qs_rv['download_fp'] = os.path.join(td_fp, qs_rv['basename'])
            fetch_kwargs.update(**qs_rv)
            if cls.download(**fetch_kwargs):
                return [cls.stage_asset(qs_rv['download_fp'])]
        return []

    @classmethod
    def ftp_connect(cls, working_directory):
        """Connect to an FTP server and chdir according to the args.

        Returns the ftplib connection object."""
        utils.verbose_out('Connecting to {}'.format(cls._host), 5)
        conn = ftplib.FTP(cls._host)
        conn.login('anonymous', settings().EMAIL)
        conn.set_pasv(True)
        utils.verbose_out('Changing to {}'.format(working_directory), 5)
        conn.cwd(working_directory)
        return conn

    @classmethod
    def fetch_ftp(cls, asset, tile, date):
        """ Fetch via FTP """
        url = cls._assets[asset].get('url', '')
        if url == '':
            raise Exception("%s: URL not defined for asset %s" % (cls.__name__, asset))
        VerboseOut('%s: fetch tile %s for %s' % (asset, tile, date), 3)
        ftpurl = url.split('/')[0]
        ftpdir = url[len(ftpurl):]
        with utils.error_handler("Error downloading from {}".format(ftpurl)):
            ftp = ftplib.FTP(ftpurl)
            ftp.login('anonymous', settings().EMAIL)
            pth = os.path.join(ftpdir, date.strftime('%Y'), date.strftime('%j'))
            ftp.set_pasv(True)
            ftp.cwd(pth)

            for f in ftp.nlst('*'):
                VerboseOut("Downloading %s" % f, 2)
                ftp.retrbinary('RETR %s' % f,
                               open(os.path.join(cls.Repository.path('stage'), f), "wb").write)
            ftp.close()

    @classmethod
    def archive(cls, path, recursive=False, keep=False, update=False):
        """Move asset into the archive.

        Pass in a path to a file or a directory.  If a directory, its
        contents are scanned for assets and any found are archived; it
        won't descend into subdirectories unless `recursive`.  Any found
        assets are given hard links in the archive.  The original is
        then removed, unless `keep`. If a found asset would replace an
        extant archived asset, replacement is only performed if
        `update`.  kwargs is unused and likely without purpose.

        Returns a pair of lists:  A list of Asset objects that were archived,
        and a list of asset objects whose files have been overwritten (by the
        update flag).
        """
        start = datetime.now()

        fnames = []
        if not os.path.isdir(path):
            fnames.append(path)
        elif recursive:
            for root, subdirs, files in os.walk(path):
                for a in cls._assets.values():
                    files = utils.find_files(a['pattern'], root)
                    fnames.extend(files)
        else:
            for a in cls._assets.values():
                files = utils.find_files(a['pattern'], path)
                fnames.extend(files)
        numlinks = 0
        numfiles = 0
        assets = []
        overwritten_assets = []
        if not fnames:
            utils.verbose_out('No files found; nothing to archive.')
        for f in fnames:
            (asset_obj, link_count, overwritten_ao) = cls._archivefile(f,
                                                                       update)
            if overwritten_ao is not None:
                overwritten_assets.append(overwritten_ao)
            if link_count >= 0:
                if not keep:
                    # user wants to remove the original hardlink to the file
                    RemoveFiles([f], ['.index', '.aux.xml'])
            if link_count > 0:
                numfiles = numfiles + 1
                numlinks = numlinks + link_count
                assets.append(asset_obj)

        # Summarize
        if numfiles > 0:
            VerboseOut('%s files (%s links) from %s added to archive in %s' %
                      (numfiles, numlinks, path, datetime.now() - start))
        if numfiles != len(fnames):
            VerboseOut('%s files not added to archive' % (len(fnames) - numfiles))
        return assets, overwritten_assets

    @classmethod
    def _archivefile(cls, filename, update=False):
        """Move the named file into the archive.

        If update == True, replace any old versions and associated files.
        Returns a 3-tuple:  An Asset object if anything was archived, or
        None, a count of hardlinks made, believed to be just 1 or 0, and
        an asset object for any asset file that was overwritten.
        """
        bname = os.path.basename(filename)
        overwritten_ao = None
        try:
            asset = cls(filename)
        except Exception, e:
            cls._quarantine_file(filename, e)
            return (None, 0, None)

        # make an array out of asset.date if it isn't already
        dates = asset.date
        if not hasattr(dates, '__len__'):
            dates = [dates]
        numlinks = 0
        otherversions = False
        for d in dates:
            tpath = cls.Repository.data_path(asset.tile, d)
            newfilename = os.path.join(tpath, bname)
            if not os.path.exists(newfilename):
                # check if another asset exists
                # QUESTION: Can it be that len(existing) > 1?
                # Not changing much now, but adding an immediate assert to
                # verify that there can only be one-or-none of an asset in the
                # archive (2017-09-29).  Assuming it isn't a problem, we could
                # drop some of these for-loops.
                existing = cls.discover(asset.tile, d, asset.asset)
                assert len(existing) in (0, 1), (
                    'Apparently there can be more than one asset file for a'
                    ' given ({}, {}, {}).'.format(asset.tile, d, asset.asset)
                )
                if len(existing) > 0 and (not update or not existing[0].updated(asset)):
                    # gatekeeper case:  No action taken because other assets exist
                    VerboseOut('%s: other version(s) already exists:' % bname, 1)
                    for ef in existing:
                        VerboseOut('\t%s' % os.path.basename(ef.filename), 1)
                    otherversions = True
                elif len(existing) > 0 and update:
                    # update case:  Remove existing outdated assets
                    #               and install the new one
                    VerboseOut('%s: removing other version(s):' % bname, 1)
                    for ef in existing:
                        if not ef.updated(asset):
                            utils.verbose_out(
                                'Asset {} is not updated version of {}.'
                                .format(ef.filename, asset.filename) +
                                ' Remove existing asset to replace.', 2
                            )
                            # NOTE: This return makes sense iff len(existing)
                            # cannot be greater than 1
                            return (None, 0, None)
                        overwritten_ao = cls(ef.filename)
                        VerboseOut('\t%s' % os.path.basename(ef.filename), 1)
                        errmsg = 'Unable to remove existing version: ' + ef.filename
                        with utils.error_handler(errmsg):
                            RemoveFiles([ef.filename], ['.index', '.aux.xml'])
                    with utils.error_handler('Problem adding {} to archive'.format(filename)):
                        os.link(os.path.abspath(filename), newfilename)
                        asset.archived_filename = newfilename
                        VerboseOut(bname + ' -> ' + newfilename, 2)
                        numlinks = numlinks + 1

                else:
                    # 'normal' case:  Just add the asset to the archive; no other work needed
                    with utils.error_handler('Unable to make data directory ' + tpath):
                        utils.mkdir(tpath)
                    with utils.error_handler('Problem adding {} to archive'.format(filename)):
                        os.link(os.path.abspath(filename), newfilename)
                        asset.archived_filename = newfilename
                        VerboseOut(bname + ' -> ' + newfilename, 2)
                        numlinks = numlinks + 1
            else:
                VerboseOut('%s already in archive' % filename, 2)

        # newly created asset should have only automagical products, and those
        # would have paths in stage with the existing asset.  Re-instantiation
        # using archived_filename rectifies this.
        if len(asset.products) > 0 and hasattr(asset, 'archived_filename'):
            new_asset_obj = cls(asset.archived_filename)
            # next line is strange, but is used by DataInventory.fetch
            new_asset_obj.archived_filename = asset.archived_filename
            asset = new_asset_obj

        if otherversions and numlinks == 0:
            return (asset, -1, overwritten_ao)
        else:
            return (asset, numlinks, overwritten_ao)
        # should return asset instance


class Data(object):
    """Collection of assets/products for single date and tile.

    If the data isn't given in tiles, then another discrete spatial
    region may be used instead.  In general, only one asset of each
    asset type is permitted (self.assets is a dict keyed by asset type,
    whose values are Asset objects).
    """
    name = 'Data'
    version = '0.0.0'
    Asset = Asset

    _unitless = 'unitless' # standard string for expressing that a product has no units

    _pattern = '*.tif'
    _products = {}
    _productgroups = {}

    @classmethod
    def get_setting(cls, key):
        """Convenience method to acces Repository's get_setting."""
        return cls.Asset.Repository.get_setting(key)

    def needed_products(self, products, overwrite):
        """ Make sure all products exist and return those that need processing """
        # TODO calling RequestedProducts twice is strange; rework into something clean
        products = self.RequestedProducts(products)
        products = self.RequestedProducts(
                [p for p in products.products if p not in self.products or overwrite])
        # TODO - this doesnt know that some products aren't available for all dates
        return products

    def process(self, products, overwrite=False, **kwargs):
        """ Make sure all products exist and return those that need processing """
        # TODO replace all calls to this method by subclasses with needed_products, then delete.
        return self.needed_products(products, overwrite)

    @classmethod
    def process_composites(cls, inventory, products, **kwargs):
        """ Process composite products using provided inventory """
        pass

    def copy(self, dout, products, site=None, res=None, interpolation=0, crop=False,
             overwrite=False, tree=False):
        """ Copy products to new directory, warp to projection if given site.

        Arguments
        =========
        dout:       output or destination directory; mkdir(dout) is done if needed.
        products:   which products to copy (passed to self.RequestedProducts())


        """
        # TODO - allow hard and soft linking options
        if res is None:
            res = self.Asset._defaultresolution
            #VerboseOut('Using default resolution of %s x %s' % (res[0], res[1]))
        dout = os.path.join(dout, self.id)
        if tree:
            dout = os.path.join(dout, self.date.strftime('%Y%j'))
        mkdir(dout)
        products = self.RequestedProducts(products)
        bname = '%s_%s' % (self.id, self.date.strftime('%Y%j'))
        for p in products.requested:
            if p not in self.sensors:
                # this product is not available for this day
                continue
            sensor = self.sensors[p]
            fin = self.filenames[(sensor, p)]
            fout = os.path.join(dout, "%s_%s_%s.tif" % (bname, sensor, p))
            if not os.path.exists(fout) or overwrite:
                with utils.error_handler('Problem creating ' + fout, continuable=True):
                    if site is not None:
                        # warp just this tile
                        resampler = ['near', 'bilinear', 'cubic']
                        cmd = 'gdalwarp %s %s -t_srs "%s" -tr %s %s -r %s' % \
                               (fin, fout, site.Projection(), res[0], res[1], resampler[interpolation])
                        print cmd
                        #result = commands.getstatusoutput(cmd)
                    else:
                        gippy.GeoImage(fin).Process(fout)
                        #shutil.copyfile(fin, fout)
        procstr = 'copied' if site is None else 'warped'
        VerboseOut('%s tile %s: %s files %s' % (self.date, self.id, len(products.requested), procstr))

    @classmethod
    def natural_percentage(cls, raw_value):
        """Callable used for argparse, defines a new type for %0.0 to %100.0.

        Receives a string, return a float.  See also:
        https://docs.python.org/2/library/argparse.html#type
        """
        f_value = float(raw_value)
        if not (0 <= f_value <= 100):
            raise argparse.ArgumentTypeError(
                "Value '{}' is outside the range [0 %, 100 %]".format(
                    raw_value))
        return f_value

    @classmethod
    def add_filter_args(cls, parser):
        """Override to add arguments to the command line suitable for filter().

        parser is expected to be a python ArgumentParser."""
        return

    def filter(self, **kwargs):
        """Permit child classes to implement filtering.

        If data.filter() returns False, the Data object will be left out
        of the inventory during DataInventory instantiation.
        """
        return True

    def meta_dict(self, src_afns=None, additional=None):
        """Returns assembled metadata dict.

        returned value contains standard metadata + asset filenames +
        optional additional content.  Asset filenames can be a string or
        iterable of strings; it'll be converted to a list of basenames.  If
        defaulted to None, self.assets' filenames is used instead.
        """
        sa = src_afns
        if src_afns is None:
            sa = [ao.filename for ao in self.assets.values()]
        elif isinstance(src_afns, basestring):
            sa = [src_afns]
        md = {
            'GIPS_Version': __version__,
            'GIPS_Source_Assets': [os.path.basename(fn) for fn in sa]
        }
        with utils.error_handler("Can't set driver version metadata", True):
            gdn = 'GIPS_' + self.Repository.name.capitalize() + '_Version'
            md[gdn] = self.version
        if additional is not None:
            md.update(additional)
        return md

    def prep_meta(self, src_afns, additional=None):
        """Prepare product metadata for consumption by GeoImage.SetMeta()."""
        return utils.stringify_meta_dict(self.meta_dict(src_afns, additional))

    def find_files(self):
        """Search path for non-asset files, usually product files.

        These must match the shell glob in self._pattern, and must not
        be assets, index files, nor xml files.
        """
        filenames = glob.glob(os.path.join(self.path, self._pattern))
        assetnames = [a.filename for a in self.assets.values()]
        badexts = ['.index', '.xml']
        test = lambda x: x not in assetnames and os.path.splitext(f)[1] not in badexts
        filenames[:] = [f for f in filenames if test(f)]
        return filenames


    @classmethod
    def normalize_tile_string(cls, tile_string):
        """Override this method to provide custom processing of tile names.

        This method should raise an exception if the tile string is
        invalid, but should return a corrected string instead if
        possible.  So for modis, 'H03V01' should return 'h03v01', while
        'H03V' should raise an exception.
        """
        return tile_string


    ##########################################################################
    # Child classes should not generally have to override anything below here
    ##########################################################################
    def __init__(self, tile=None, date=None, path='', search=True):
        """ Find all data and assets for this tile and date.

        Note date should be a datetime.date object. search=False will
        prevent searching for assets via Asset.discover().
        """
        self.id = tile
        self.date = date
        self.path = path      # /full/path/to/{driver}/tiles/{tile}/{date}; overwritten below
        self.basename = ''    # product file name prefix, form is <tile>_<date>
        self.assets = {}      # dict of <asset type string>: <Asset instance>
        self.filenames = {}   # dict of (sensor, product): product filename
        self.sensors = {}     # dict of asset/product: sensor
        if tile is not None and date is not None:
            self.path = self.Repository.data_path(tile, date)
            self.basename = self.id + '_' + self.date.strftime(self.Repository._datedir)
            if search:
                [self.add_asset(a) for a in self.Asset.discover(tile, date)] # Find all assets
                fn_to_add = None
                if orm.use_orm():
                    search = {'driver': self.Repository.name.lower(),
                              'date': date, 'tile': tile}
                    fn_to_add = [str(p.name)
                                 for p in dbinv.product_search(**search)]
                self.ParseAndAddFiles(fn_to_add)

    def add_asset(self, asset):
        """Add an Asset object to self.assets and:

        Look at its products, adding metadata to self accordingly.
        """
        self.assets[asset.asset] = asset
        for p, val in asset.products.items():
            self.filenames[(asset.sensor, p)] = val
            self.sensors[p] = asset.sensor
        self.filenames.update({(asset.sensor, p): val for p, val in asset.products.items()})
        self.sensors[asset.asset] = asset.sensor

    @property
    def Repository(self):
        """ The repository for this class """
        return self.Asset.Repository

    @classmethod
    def RequestedProducts(cls, *args, **kwargs):
        from gips.core import RequestedProducts
        return RequestedProducts(cls, *args, **kwargs)

    def __getitem__(self, key):
        """ Get filename for product key """
        if type(key) == tuple:
            return self.filenames[key]
        else:
            return self.filenames[(self.sensor_set[0], key)]

    def __str__(self):
        """ Text representation """
        return '%s: %s: %s' % (self.name, self.date, ' '.join(self.product_set))

    def __len__(self):
        """ Number of products """
        return len(self.filenames)

    @property
    def valid(self):
        return False if len(self.filenames) == 0 and len(self.assets) == 0 else True

    @property
    def day(self):
        return self.date.strftime('%j')

    @property
    def sensor_set(self):
        """ Return list of sensors used """
        return list(set(sorted(self.sensors.values())))

    @property
    def products(self):
        """ Get list of products """
        return sorted([k[1] for k in self.filenames.keys()])

    @property
    def product_set(self):
        """ Return list of products available """
        return list(set(self.products))

    def ParseAndAddFiles(self, filenames=None):
        """Parse and Add filenames to existing filenames.

        If no filenames are provided, a list from find_files() is used
        instead."""
        if filenames is None:
            filenames = self.find_files() # find *product* files actually
        datedir = self.Repository._datedir
        for f in filenames:
            bname = basename(f)
            parts = bname.split('_')
            if len(parts) < 3 or len(parts) > 4:
                # Skip this file
                VerboseOut('Unrecognizable file: %s' % f, 3)
                continue
            offset = 1 if len(parts) == 4 else 0
            with utils.error_handler('Unrecognizable file ' + f, continuable=True):
                # only admit product files matching a single date
                if self.date is None:
                    # First time through
                    self.date = datetime.strptime(parts[0 + offset], datedir).date()
                else:
                    date = datetime.strptime(parts[0 + offset], datedir).date()
                    if date != self.date:
                        raise IOError('Mismatched dates: '
                            'Expected {} but got {}'.format(self.date, date))
                sensor = parts[1 + offset]
                product = parts[2 + offset]
                self.AddFile(sensor, product, f, add_to_db=False)

    def AddFile(self, sensor, product, filename, add_to_db=True):
        """Add named file to this object, taking note of its metadata.

        Optionally, also add a listing for the product file to the
        inventory database.
        """
        utils.verbose_out('adding {} {} {} to Data object'.format(
            sensor, product, filename), 5)
        self.filenames[(sensor, product)] = filename
        # TODO - currently assumes single sensor for each product
        self.sensors[product] = sensor
        if add_to_db and orm.use_orm(): # update inventory DB if such is requested
            dbinv.update_or_add_product(driver=self.name.lower(), product=product, sensor=sensor,
                                        tile=self.id, date=self.date, name=filename)

    def asset_filenames(self, product):
        assets = self._products[product]['assets']
        filenames = []
        for asset in assets:
            emsg = 'no "{}" assets here'.format(asset)
            with utils.error_handler(emsg, continuable=True):
                filenames.extend(self.assets[asset].datafiles())
        if len(filenames) == 0:
            VerboseOut('There are no available assets on %s for tile %s' % (str(self.date), str(self.id), ), 3)
            return None
        return filenames

    def open(self, product, sensor=None, update=False):
        """ Open and return a GeoImage """
        if sensor is None:
            sensor = self.sensors[product]
        with utils.error_handler('({}, {}) not found.'.format(sensor, product)):
            fname = self.filenames[(sensor, product)]
        with utils.error_handler('Error opening "{}"'.format(fname)):
            img = gippy.GeoImage(fname)
        return img


    def open_assets(self, product):
        """ Open and return a GeoImage of the assets """
        return gippy.GeoImage(self.asset_filenames(product))

    # TODO - make general product_filter function
    def masks(self, patterns=None):
        """ List all products that are masks """
        if patterns is None:
            patterns = ['acca', 'fmask', 'mask']
        m = []
        for p in self.products:
            if any(pattern in p for pattern in patterns):
                m.append(p)
        return m

    @classmethod
    def pprint_header(cls):
        """ Print product inventory header showing product coverage"""
        header = Colors.BOLD + Colors.UNDER + '{:^12}'.format('DATE')
        for a in sorted(cls._products.keys()):
            header = header + ('{:^10}'.format(a if a != '' else 'Coverage'))
        return header + '{:^10}'.format('Product') + Colors.OFF

    @classmethod
    def pprint_asset_header(cls):
        """ Print header info for asset coverage """
        header = Colors.BOLD + Colors.UNDER + '{:^12}'.format('DATE')
        for a in sorted(cls.Asset._assets.keys()):
            header = header + ('{:^10}'.format(a if a != '' else 'Coverage'))
        header = header + '{:^10}'.format('Product') + Colors.OFF
        print header

    def pprint(self, dformat='%j', colors=None):
        """ Print product inventory for this date """
        sys.stdout.write('{:^12}'.format(self.date.strftime(dformat)))
        if colors is None:
            sys.stdout.write('  '.join(sorted(self.products)))
        else:
            for p in sorted(self.products):
                sys.stdout.write(colors[self.sensors[p]] + p + Colors.OFF + '  ')
        sys.stdout.write('\n')


    def _time_report(self, msg, reset_clock=False, verbosity=None):
        """Provide the user with progress reports, including elapsed time.

        Reset elapsed time with reset_clock=True; when starting or
        resetting the clock, specify a verbosity, or else accept the
        default of 3.
        """
        start = getattr(self, '_time_report_start', None)
        if reset_clock or start is None:
            start = self._time_report_start = datetime.now()
            self._time_report_verbosity = 3 if verbosity is None else verbosity
        elif verbosity is not None:
            raise ValueError('Changing verbosity is only permitted when resetting the clock')
        utils.verbose_out('{}:  {}'.format(datetime.now() - start, msg),
                self._time_report_verbosity)

    ##########################################################################
    # Class methods
    ##########################################################################
    @classmethod
    def discover(cls, path):
        """Find products in path and return Data object for each date.

        Does not interact with inventory DB as only caller is
        ProjectInventory which needs to read form the filesystem."""
        files = []
        datedir = cls.Asset.Repository._datedir
        for root, dirs, filenames in os.walk(path):
            for filename in filenames:
                f = os.path.join(root, filename)
                VerboseOut(f, 4)
                parts = basename(f).split('_')
                if len(parts) == 3 or len(parts) == 4:
                    with utils.error_handler('Error parsing product date', continuable=True):
                        datetime.strptime(parts[len(parts) - 3], datedir)
                        files.append(f)

        datas = []
        if len(files) == 0:
            return datas

        # Group by date
        sind = len(basename(files[0]).split('_')) - 3

        func = lambda x: datetime.strptime(basename(x).split('_')[sind], datedir).date()
        for date, fnames in groupby(sorted(files), func):
            dat = cls(path=path)
            dat.ParseAndAddFiles(list(fnames))
            datas.append(dat)

        return datas

    @classmethod
    def inventory(cls, site=None, key='', where='', tiles=None, pcov=0.0,
                  ptile=0.0, dates=None, days=None, rastermask=None, **kwargs):
        """ Return list of inventories (size 1 if not looping through geometries) """
        from gips.inventory import DataInventory
        from gips.core import SpatialExtent, TemporalExtent

        spatial = SpatialExtent.factory(
            cls, site=site, rastermask=rastermask, key=key, where=where, tiles=tiles,
            pcov=pcov, ptile=ptile
        )
        temporal = TemporalExtent(dates, days)
        if len(spatial) > 1:
            raise ValueError(
                '{}.inventory: site (or rastermask) may only specify 1'
                '     feature via this API call ({} provided in {})'
                .format(
                    cls.__name__, len(spatial),
                    str((site, key, where)) if site else rastermask
                )
            )
        return DataInventory(cls, spatial[0], temporal, **kwargs)

    @classmethod
    def products2assets(cls, products):
        """ Get list of assets needed for these products """
        assets = []
        for p in products:
            if 'assets' in cls._products[p]:
                assets.extend(cls._products[p]['assets'])
            else:
                assets.append('')
        return set(assets)

    @classmethod
    def need_to_fetch(cls, a_type, tile, date, update, **fetch_kwargs):
        local_ao = cls.Asset.discover_asset(a_type, tile, date)
        # we have something for this atd, and user doesn't want to update,
        # so the decision is easy
        if local_ao is not None and not update:
            return False
        qs_rv = cls.Asset.query_service(a_type, tile, date, **fetch_kwargs)
        if qs_rv is None: # nothing remote; done
            return False
        # if we don't have it already, or if `update` flag
        queried_ao = cls.Asset(qs_rv['basename'])
        return local_ao is None or (update and local_ao.updated(queried_ao))

    need_fetch_kwargs = False # feature toggle:  set in driver's subclass

    @classmethod
    def fetch(cls, products, tiles, textent, update=False, **kwargs):
        """ Download data for tiles and add to archive. update forces fetch """
        fetched = []
        fetch_kwargs = kwargs if cls.need_fetch_kwargs else {}
        atd_pile = ((a, t, d)
            for a in cls.products2assets(products)
            for t in tiles
            for d in cls.Asset.dates(a, t, textent.datebounds, textent.daybounds)
                if cls.need_to_fetch(a, t, d, update, **fetch_kwargs))
        for a, t, d in atd_pile:
            err_msg = 'Problem fetching asset for {}, {}, {}'.format(
                a, t, d.strftime("%y-%m-%d"))
            with utils.error_handler(err_msg, continuable=True):
                cls.Asset.fetch(a, t, d, **fetch_kwargs)
                # fetched may contain both fetched and unfetchable things
                fetched.append((a, t, d))

        return fetched

    @classmethod
    def product_groups(cls):
        """ Return dict of groups and products in each one """
        groups = cls._productgroups
        groups['Standard'] = []
        grouped_products = [x for sublist in cls._productgroups.values() for x in sublist]
        for p in cls._products:
            if p not in grouped_products:
                groups['Standard'].append(p)
        if len(groups['Standard']) == 0:
            del groups['Standard']
        return groups

    @classmethod
    def products2groups(cls, products):
        """ Convert product list to groupings """
        p2g = {}
        groups = {}
        allgroups = cls.product_groups()
        for g in allgroups:
            groups[g] = {}
            for p in allgroups[g]:
                p2g[p] = g
        for p, val in products.items():
            g = p2g[val[0]]
            groups[g][p] = val
        return groups

    @classmethod
    def print_products(cls):
        print Colors.BOLD + "\n%s Products v%s" % (cls.name, cls.version) + Colors.OFF
        groups = cls.product_groups()
        opts = False
        txt = ""
        for group in groups:
            txt = txt + Colors.BOLD + '\n%s Products\n' % group + Colors.OFF
            for p in sorted(groups[group]):
                h = cls._products[p]['description']
                txt = txt + '   {:<12}{:<40}\n'.format(p, h)
                if 'arguments' in cls._products[p]:
                    opts = True
                    #sys.stdout.write('{:>12}'.format('options'))
                    args = [['', a] for a in cls._products[p]['arguments']]
                    for a in args:
                        txt = txt + '{:>12}     {:<40}\n'.format(a[0], a[1])
        if opts:
            print "  Optional qualifiers listed below each product."
            print "  Specify by appending '-option' to product (e.g., ref-toa)"
        sys.stdout.write(txt)

    def make_temp_proc_dir(self):
        """Make a temporary directory in which to perform gips processing.

        Returns a context manager that governs the newly-made directory,
        which is deleted on exiting the context. It is created in the
        driver's stage directory, and has a random name.
        """
        return utils.make_temp_dir(prefix='proc', dir=self.Repository.path('stage'))

    @staticmethod
    def proc_temp_dir_manager(wrapped_method):
        """Decorator for self.process to use a tempdir consistently.

        Decorate a method with it, and it'll create a temp
        directory for the method's use, then destroy it afterwards.
        """
        def wrapper(self, *args, **kwargs):
            assert not hasattr(self, '_temp_proc_dir')
            with self.make_temp_proc_dir() as temp_dir:
                self._temp_proc_dir = temp_dir
                # keys are temp filenames, vals are tuples:  (sensor, prod-type, archive full path)
                try:
                    return wrapped_method(self, *args, **kwargs)
                finally:
                    del self._temp_proc_dir
        return wrapper

    def archive_temp_path(self, temp_fp):
        """Move the product file from the managed temp dir to the archive.

        The archival full path is returned; an appropriate spot in the
        archive is chosen automatically.
        """
        archive_fp = os.path.join(self.path, os.path.basename(temp_fp))
        os.rename(temp_fp, archive_fp)
        return archive_fp

    def generate_temp_path(self, filename):
        """Return a full path to the filename within the managed temp dir.

        The filename's basename is glued to the end of the temp dir.
        This method should be called from within proc_temp_dir_manager.
        """
        return os.path.join(self._temp_proc_dir, os.path.basename(filename))

    def product_filename(self, sensor, prod_type):
        """Returns a standardized product file name."""
        date_string = self.date.strftime(self.Repository._datedir)
        # reminder: self.id is the tile ID string, eg 'h12v04' or '19TCH'
        return '{}_{}_{}_{}.tif'.format(self.id, date_string, sensor, prod_type)

    def temp_product_filename(self, sensor, prod_type):
        """Generates a product filename within the managed temp dir."""
        return self.generate_temp_path(self.product_filename(sensor, prod_type))

    @classmethod
    def archive_assets(cls, path, recursive=False, keep=False, update=False):
        """Adds asset files found in the given path to the repo.

        For arguments see Asset.archive."""
        archived_aol, overwritten_aol = cls.Asset.archive(
                path, recursive, keep, update)
        if overwritten_aol:
            utils.verbose_out('Updated {} assets, checking for stale '
                              'products.'.format(len(overwritten_aol)), 2)
            deletable_p_files = {}
            for asset_obj in overwritten_aol:
                data_obj = cls(asset_obj.tile, asset_obj.date, search=True)
                deletable_p_types = [pt for pt in cls._products
                        if asset_obj.asset in data_obj._products[pt]['assets']]
                #    v-- as usual don't care about the sensor
                for (_, raw_p_type), full_path in data_obj.filenames.items():
                    p_type = raw_p_type.split('-')[0] # take out eg '-toa'
                    if p_type in deletable_p_types:
                        # need to know the key to delete from the ORM
                        p_key = (cls.Asset.Repository.name.lower(), raw_p_type,
                                 asset_obj.tile, asset_obj.date)
                        deletable_p_files[p_key] = full_path

            utils.verbose_out('Found {} stale products:'.format(
                                len(deletable_p_files)), 2)
            for p_key, full_path in deletable_p_files.items():
                utils.verbose_out('Deleting ' + full_path, 2)
                if orm.use_orm():
                    dr, p, t, dt = p_key
                    dbinv.delete_product(driver=dr, product=p, tile=t, date=dt)
                os.remove(full_path)

        return archived_aol


# TODO rebase other drivers on these subclasses as needed
class CloudCoverAsset(Asset):
    """Adds filtering support to the Asset class.

    Together with CloudCoverData, lets Assets and Data objects work
    together to filter by cloud cover. It needs Asset.cloud_cover() to
    be implemented.
    """
    def filter(self, pclouds=100.0, **kwargs):
        if pclouds >= 100.0:
            return True
        cc = self.cloud_cover()
        asset_passes_filter = cc <= pclouds
        msg = ('Asset cloud cover is {}%, meets pclouds threshold of {}%'
               if asset_passes_filter else
               'Asset cloud cover is {}%, fails to meet pclouds threshold of {}%')
        utils.verbose_out(msg.format(cc, pclouds), 3)
        return asset_passes_filter


class CloudCoverData(Data):
    """Adds filtering support to a Data class.

    Together with CloudCoverAsset, lets Assets and Data objects work
    together to filter by cloud cover.
    """
    need_fetch_kwargs = True

    @classmethod
    def add_filter_args(cls, parser):
        super(CloudCoverData, cls).add_filter_args(parser)
        help_str = ('cloud percentage threshold; assets with cloud cover'
                    ' percentages higher than this value will be filtered out')
        parser.add_argument('--pclouds', help=help_str,
                            type=cls.natural_percentage, default=100.0)

    def filter(self, pclouds=100.0, **kwargs):
        # in case filter() actually does something someday
        if not super(CloudCoverData, self).filter(**kwargs):
            return False
        return all([a.filter(pclouds, **kwargs) for a in self.assets.values()])
