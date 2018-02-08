#!/usr/bin/env python
################################################################################
#    GIPS: Geospatial Image Processing System
#
#    AUTHOR: Matthew Hanson
#    EMAIL:  matt.a.hanson@gmail.com
#
#    Copyright (C) 2014 Applied Geosolutions
#
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
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

from __future__ import print_function

from contextlib import contextmanager
import os
import re
from datetime import datetime, date, timedelta
import shutil
import glob
import traceback
from copy import deepcopy
import commands # TODO unused?
import subprocess
import tempfile
import tarfile
import json
from xml.etree import ElementTree

import numpy
# once gippy==1.0, switch to GeoRaster.erode
from scipy.ndimage import binary_erosion

import osr
import gippy
from gips import __version__ as __gips_version__
from gips.core import SpatialExtent, TemporalExtent
from gippy.algorithms import ACCA, Fmask, LinearTransform, Indices, AddShadowMask
from gips.data.core import Repository, Asset, Data
from gips.atmosphere import SIXS, MODTRAN
import gips.atmosphere
from gips.inventory import DataInventory
from gips.utils import RemoveFiles, basename, settings, verbose_out
from gips import utils

import requests
import homura


requirements = ['Py6S>=1.5.0']

def path_row(tile_id):
    """Converts the given landsat tile string into (path, row)."""
    return (tile_id[:3], tile_id[3:])

def binmask(arr, bit):
    """ Return boolean array indicating which elements as binary have a 1 in
        a specified bit position. Input is Numpy array.
    """
    return arr & (1 << (bit - 1)) == (1 << (bit - 1))


class landsatRepository(Repository):
    """ Singleton (all class methods) to be overridden by child data classes """
    name = 'Landsat'
    description = 'Landsat 5 (TM), 7 (ETM+), 8 (OLI)'
    _tile_attribute = 'PR'

    default_settings = {'source': 'usgs'}

    @classmethod
    def feature2tile(cls, feature):
        tile = super(landsatRepository, cls).feature2tile(feature)
        return tile.zfill(6)


class landsatAsset(Asset):
    """ Landsat asset (original raw tar file) """
    Repository = landsatRepository

    # tassled cap coefficients for L5 and L7
    _tcapcoef = [
        [0.3561, 0.3972, 0.3904, 0.6966, 0.2286, 0.1596],
        [-0.3344, -0.3544, -0.4556, 0.6966, -0.0242, -0.2630],
        [0.2626, 0.2141, 0.0926, 0.0656, -0.7629, -0.5388],
        [0.0805, -0.0498, 0.1950, -0.1327, 0.5752, -0.7775],
        [-0.7252, -0.0202, 0.6683, 0.0631, -0.1494, -0.0274],
        [0.4000, -0.8172, 0.3832, 0.0602, -0.1095, 0.0985]
    ]

    # combine sensormeta with sensor
    _sensors = {
        #'LT4': {
        #    'description': 'Landsat 4',
        #},
        'LT5': {
            'description': 'Landsat 5',
            'ee_dataset': 'LANDSAT_TM_C1',
            'startdate': datetime(1984, 3, 1),
            'enddate': datetime(2013, 1, 1),
            'bands': ['1', '2', '3', '4', '5', '6', '7'],
            'oldbands': ['1', '2', '3', '4', '5', '6', '7'],
            'colors': ["BLUE", "GREEN", "RED", "NIR", "SWIR1", "LWIR", "SWIR2"],
            # TODO - update bands with actual L5 values (these are L7)
            'bandlocs': [0.4825, 0.565, 0.66, 0.825, 1.65, 11.45, 2.22],
            'bandwidths': [0.065, 0.08, 0.06, 0.15, 0.2, 2.1, 0.26],
            'E': [1983, 1796, 1536, 1031, 220.0, 0, 83.44],
            'K1': [0, 0, 0, 0, 0, 607.76, 0],
            'K2': [0, 0, 0, 0, 0, 1260.56, 0],
            'tcap': _tcapcoef,
        },
        'LE7': {
            'description': 'Landsat 7',
            'ee_dataset': 'LANDSAT_EMT_C1',
            'startdate': datetime(1999, 4, 15),
            #bands = ['1','2','3','4','5','6_VCID_1','6_VCID_2','7','8']
            'bands': ['1', '2', '3', '4', '5', '6_VCID_1', '7'],
            'oldbands': ['1', '2', '3', '4', '5', '61', '7'],
            'colors': ["BLUE", "GREEN", "RED", "NIR", "SWIR1", "LWIR", "SWIR2"],
            'bandlocs': [0.4825, 0.565, 0.66, 0.825, 1.65, 11.45, 2.22],
            'bandwidths': [0.065, 0.08, 0.06, 0.15, 0.2, 2.1, 0.26],
            'E': [1997, 1812, 1533, 1039, 230.8, 0, 84.90],
            'K1': [0, 0, 0, 0, 0, 666.09, 0],
            'K2': [0, 0, 0, 0, 0, 1282.71, 0],
            'tcap': _tcapcoef,
        },
        'LC8': {
            'description': 'Landsat 8',
            'ee_dataset': 'LANDSAT_8_C1',
            'startdate': datetime(2013, 4, 1),
            # as normal for Landsat 8 but with panchromatic band left out, CF:
            # https://landsat.usgs.gov/what-are-band-designations-landsat-satellites
            'bands': ['1', '2', '3', '4', '5', '6', '7', '9', '10', '11'],
            'oldbands': ['1', '2', '3', '4', '5', '6', '7', '9', '10', '11'],
            'colors': ["COASTAL", "BLUE", "GREEN", "RED", "NIR",
                       "SWIR1", "SWIR2", "CIRRUS", "LWIR", "LWIR2"],
            'bandlocs': [0.443, 0.4825, 0.5625, 0.655, 0.865,
                         1.610, 2.2, 1.375, 10.8, 12.0],
            'bandwidths': [0.01, 0.0325, 0.0375, 0.025, 0.02,
                           0.05, 0.1, 0.015, 0.5, 0.5],
            'E': [2638.35, 2031.08, 1821.09, 2075.48, 1272.96,
                  246.94, 90.61, 369.36, 0, 0],
            'K1': [0, 0, 0, 0, 0,
                   0, 0, 0, 774.89, 480.89],
            'K2': [0, 0, 0, 0, 0,
                   0, 0, 0, 1321.08, 1201.14],
            'tcap': [
                [0.3029, 0.2786, 0.4733, 0.5599, 0.508, 0.1872],
                [-0.2941, -0.243, -0.5424, 0.7276, 0.0713, -0.1608],
                [0.1511, 0.1973, 0.3283, 0.3407, -0.7117, -0.4559],
                [-0.8239, 0.0849, 0.4396, -0.058, 0.2013, -0.2773],
                [-0.3294, 0.0557, 0.1056, 0.1855, -0.4349, 0.8085],
                [0.1079, -0.9023, 0.4119, 0.0575, -0.0259, 0.0252],
            ]
        },
        'LC8SR': {
            'description': 'Landsat 8 Surface Reflectance',
            'startdate': datetime(2013, 4, 1),
        }
    }

    # filename minus extension so that C1 & C1S3 both use the same pattern
    # example:  LC08_L1TP_013030_20151225_20170224_01_T1
    _c1_base_pattern = (
        r'^L(?P<sensor>\w)(?P<satellite>\d{2})_'
        r'(?P<correction_level>.{4})_(?P<path>\d{3})(?P<row>\d{3})_'
        r'(?P<acq_year>\d{4})(?P<acq_month>\d{2})(?P<acq_day>\d{2})_'
        r'(?P<proc_year>\d{4})(?P<proc_month>\d{2})(?P<proc_day>\d{2})_'
        r'(?P<coll_num>\d{2})_(?P<coll_cat>.{2})')

    _assets = {
        # DN & SR assets are no longer fetchable
        'DN': {
            'sensors': ['LT5', 'LE7', 'LC8'],
            'enddate': datetime(2017, 4, 30),
            'pattern': (
                r'^L(?P<sensor>[A-Z])(?P<satellie>\d)'
                r'(?P<path>\d{3})(?P<row>\d{3})'
                r'(?P<acq_year>\d{4})(?P<acq_day>\d{3})'
                r'(?P<gsi>[A-Z]{3})(?P<version>\d{2})\.tar\.gz$'
            ),
        },
        'SR': {
            'sensors': ['LC8SR'],
            'pattern': r'^L.*?-SC.*?\.tar\.gz$',
        },

        # landsat setting 'source' decides which asset type is downloaded:
        # source == usgs -> fetch C1 assets from USGS
        # source == s3 -> fetch C1S3 assets from AWS S3
        'C1': {
            'sensors': ['LT5', 'LE7', 'LC8'],
            'pattern': _c1_base_pattern + r'\.tar\.gz$',
            'latency': 12,
        },
        'C1S3': {
            'sensors': ['LC8'],
            'pattern': _c1_base_pattern + r'_S3\.json$',
            'latency': 12,
        },
    }

    # Field ids are retrieved with `api.dataset_fields()` call
    _ee_datasets = None

    # Set the startdate to the min date of the asset's sensors
    for asset, asset_info in _assets.iteritems():
        asset_info['startdate'] = min(
            [_sensors[sensor]['startdate']
                for sensor in asset_info['sensors']]
        )

    _defaultresolution = [30.0, 30.0]

    def __init__(self, filename):
        """ Inspect a single file and get some metadata """
        super(landsatAsset, self).__init__(filename)

        fname = os.path.basename(filename)

        verbose_out("Attempting to load " + fname, 2)

        sr_pattern_re = re.compile(self._assets['SR']['pattern'])
        dn_pattern_re = re.compile(self._assets['DN']['pattern'])
        c1_pattern_re = re.compile(self._assets['C1']['pattern'])
        c1s3_pattern_re = re.compile(self._assets['C1S3']['pattern'])

        sr_match = sr_pattern_re.match(fname)
        dn_match = dn_pattern_re.match(fname)
        c1_match = c1_pattern_re.match(fname)
        c1s3_match = c1s3_pattern_re.match(fname)

        if sr_match:
            verbose_out('SR asset', 2)
            self.asset = 'SR'
            self.sensor = 'LC8SR'
            self.version = int(fname[20:22])
            self.tile = fname[3:9]
            self.date = datetime.strptime(fname[9:16], "%Y%j")

        elif dn_match:
            verbose_out('DN asset', 2)
            self.tile = dn_match.group('path') + dn_match.group('row')
            year = dn_match.group('acq_year')
            doy = dn_match.group('acq_day')
            self.date = datetime.strptime(year + doy, "%Y%j")

            self.asset = 'DN'
            self.sensor = fname[0:3]
            self.version = int(fname[19:21])
        elif c1_match or c1s3_match:
            self.asset = 'C1' if c1_match else 'C1S3'
            match = c1_match or c1s3_match
            utils.verbose_out(self.asset + ' asset', 2)

            self.tile = match.group('path') + match.group('row')
            year = match.group('acq_year')
            month = match.group('acq_month')
            day = match.group('acq_day')
            self.date = datetime.strptime(year + month + day, "%Y%m%d")

            self.sensor = "L{}{}".format(match.group('sensor'),
                                         int(match.group('satellite')))
            self.collection_number = match.group('coll_num')
            self.collection_category = match.group('coll_cat')
            self.version = 1e6 * int(self.collection_number) + \
                    (self.date - datetime(2017, 1, 1)).days + \
                    {'RT': 0, 'T2': 0.5, 'T1': 0.9}[self.collection_category]
        else:
            msg = "No matching landsat asset type for '{}'".format(fname)
            raise RuntimeError(msg, filename)

        if self.asset in ['DN', 'C1', 'C1S3']:
            smeta = self._sensors[self.sensor]
            self.meta = {}
            self.meta['bands'] = {}
            for i, band in enumerate(smeta['colors']):
                wvlen = smeta['bandlocs'][i]
                self.meta['bands'][band] = {
                    'bandnum': i + 1,
                    'wvlen': wvlen,
                    'wvlen1': wvlen - smeta['bandwidths'][i] / 2.0,
                    'wvlen2': wvlen + smeta['bandwidths'][i] / 2.0,
                    'E': smeta['E'][i],
                    'K1': smeta['K1'][i],
                    'K2': smeta['K2'][i],
                }
            self.visbands = [col for col in smeta['colors'] if col[0:4] != "LWIR"]
            self.lwbands = [col for col in smeta['colors'] if col[0:4] == "LWIR"]

        if self.sensor not in self._sensors.keys():
            raise Exception("Sensor %s not supported: %s" % (self.sensor, filename))
        self._version = self.version

    def cloud_cover(self):
        """Returns the cloud cover for the current asset.

        Caches and returns the value found in self.meta['cloud-cover']."""
        if 'cloud-cover' in self.meta:
            return self.meta['cloud-cover']
        # first attempt to find or download an MTL file and get the CC value
        text = None
        if self.asset == 'C1S3':
            if os.path.exists(self.filename):
                c1s3_content = self.load_c1s3_json()
                text = requests.get(c1s3_content['mtl']).text
            else:
                query_results = self.query_s3(self.tile, self.date)
                if query_results is None:
                    raise IOError('Could not locate metadata for'
                                  ' ({}, {})'.format(self.tile, self.date))
                # [-1] is mtl file path
                text = requests.get(self._s3_url + query_results[-1]).text
        elif os.path.exists(self.filename):
            mtlfilename = self.extract(next(
                    f for f in self.datafiles() if f.endswith('MTL.txt')))
            err_msg = 'Error reading metadata file ' + mtlfilename
            with utils.error_handler(err_msg):
                with open(mtlfilename, 'r') as mtlfile:
                    text = mtlfile.read()

        if text is not None:
            cc_pattern = r".*CLOUD_COVER = (\d+.?\d*)"
            cloud_cover = re.match(cc_pattern, text, flags=re.DOTALL)
            if not cloud_cover:
                raise ValueError("No match for '{}' found in {}".format(
                                    cc_pattern, mtlfilename))
            self.meta['cloud-cover'] = float(cloud_cover.group(1))
            return self.meta['cloud-cover']

        # the MTL file didn't work out; attempt USGS API search instead
        api_key = self.ee_login()
        self.load_ee_search_keys()
        dataset_name = self._sensors[self.sensor]['ee_dataset']
        path_field   = self._ee_datasets[dataset_name]['WRS Path']
        row_field    = self._ee_datasets[dataset_name]['WRS Row']
        date_string = datetime.strftime(self.date, "%Y-%m-%d")
        from usgs import api
        response = api.search(
                dataset_name, 'EE',
                where={path_field: self.tile[0:3], row_field: self.tile[3:]},
                start_date=date_string, end_date=date_string, api_key=api_key)
        metadata = requests.get(
                response['data']['results'][0]['metadataUrl']).text
        xml = ElementTree.fromstring(metadata)
        xml_magic_string = (".//{http://earthexplorer.usgs.gov/eemetadata.xsd}"
                            "metadataField[@name='Scene Cloud Cover']")
        # Indexing an Element instance returns its children
        self.meta['cloud-cover'] = float(xml.find(xml_magic_string)[0].text)
        return self.meta['cloud-cover']

    def filter(self, pclouds=100, **kwargs):
        """
        Filters current asset, currently based on cloud cover.

        pclouds is a number between 0 and 100.

        kwargs is reserved for future filtering parameters.
        """
        if pclouds >= 100:
            return True

        scene_cloud_cover = self.cloud_cover()

        return scene_cloud_cover < pclouds

    def load_c1s3_json(self):
        """Load the content from a C1S3 json asset and return it.

        Returns None if the current asset type isn't C1S3."""
        if self.asset != 'C1S3':
            return None
        with open(self.filename) as aof:
            return json.load(aof)

    @classmethod
    def ee_login(cls):
        if not hasattr(cls, '_ee_key'):
            username = settings().REPOS['landsat']['username']
            password = settings().REPOS['landsat']['password']
            from usgs import api
            cls._ee_key = api.login(username, password)['data']
        return cls._ee_key

    @classmethod
    def load_ee_search_keys(cls):
        if cls._ee_datasets:
            return
        api_key = cls.ee_login()
        from usgs import api
        cls._ee_datasets = {
            ds: {
                r['name']: r['fieldId']
                for r in api.dataset_fields(ds, 'EE', api_key)['data']
                if r['name'] in [u'WRS Path', u'WRS Row']
            }
            for ds in ['LANDSAT_8_C1', 'LANDSAT_ETM_C1', 'LANDSAT_TM_C1']
        }

    _bucket_name = 'landsat-pds'
    _s3_url = 'https://landsat-pds.s3.amazonaws.com/'

    # take advantage of gips' search order (tile is outer, date is inner)
    # and cache search outcomes
    _query_s3_cache = (None, None) # prefix, search results

    @classmethod
    def query_s3(cls, tile, date):
        """Handles AWS S3 queries for landsat data.

        Returns a filename suitable for naming the constructed asset,
        and a list of S3 keys.  Returns None if no asset found for the
        given scene.
        """
        # for finding assets matching the tile
        key_prefix = 'c1/L8/{}/{}/'.format(*path_row(tile))
        # match something like:  'LC08_L1TP_013030_20170402_20170414_01_T1'
        # filters for date and also tier
        # TODO all things not just T1 ----------------vv
        fname_fragment = r'L..._...._{}_{}_\d{{8}}_.._T1'.format(
                tile, date.strftime('%Y%m%d'))
        re_string = key_prefix + fname_fragment
        filter_re = re.compile(re_string)

        missing_auth_vars = tuple(
                set(['AWS_SECRET_ACCESS_KEY', 'AWS_ACCESS_KEY_ID'])
                - set(os.environ.keys()))
        if len(missing_auth_vars) > 0:
            raise EnvironmentError("Missing AWS S3 auth credentials:"
                                   "  {}".format(missing_auth_vars))

        # on repeated searches, chances are we have a cache we can use
        expected_prefix, keys = cls._query_s3_cache
        if expected_prefix != key_prefix:
            verbose_out("New prefix detected; refreshing S3 query cache.", 5)
            # find the layer and metadata files matching the current scene
            import boto3 # import here so it only breaks if it's actually needed
            s3 = boto3.resource('s3')
            bucket = s3.Bucket(cls._bucket_name)
            keys = [o.key for o in bucket.objects.filter(Prefix=key_prefix)]
            cls._query_s3_cache = key_prefix, keys
            verbose_out("Found {} S3 keys while searching for for key fragment"
                        " '{}'".format(len(keys), key_prefix), 5)
        else:
            verbose_out("Found {} cached search results for S3 key fragment"
                        " '{}'".format(len(keys), key_prefix), 5)

        # A rare instance of a stupid for-loop being the right choice:
        _30m_tifs = []
        _15m_tif = mtl_txt = qa_tif = None
        for key in keys:
            if not filter_re.match(key):
                continue
            if key.endswith('B8.TIF'):
                _15m_tif = key
            elif key.endswith('MTL.txt'):
                mtl_txt = key
            elif key.endswith('BQA.TIF'):
                qa_tif = key
            elif key.endswith('.TIF'):
                _30m_tifs.append(key)

        if len(_30m_tifs) != 10 or None in (_15m_tif, mtl_txt, qa_tif):
            verbose_out('Found no complete S3 asset for'
                        ' (C1S3, {}, {})'.format(tile, date), 4)
            return None

        verbose_out('Found complete C1S3 asset for'
                    ' (C1S3, {}, {})'.format(tile, date), 4)

        # have to custom sort thanks to 'B1.TIF' instead of 'B01.TIF':
        def sort_key_f(key):
            match = re.search(r'B(\d+).TIF$', key)
            # sort by band number; anything weird goes last
            return int(match.group(1)) if match else 99
        _30m_tifs.sort(key=sort_key_f)

        filename = re.search(fname_fragment, _15m_tif).group(0) + '_S3.json'
        verbose_out("Constructed S3 asset filename:  " + filename, 5)
        return filename, _30m_tifs, _15m_tif, qa_tif, mtl_txt

    @classmethod
    def fetch_s3(cls, tile, date):
        """Fetches AWS S3 assets; currently only 'C1S3' assets.

        Doesn't fetch much; instead it constructs a VRT-based tarball.
        """
        query_results = cls.query_s3(tile, date)
        if query_results is None:
            return
        (filename, _30m_tifs, _15m_tif, qa_tif, mtl_txt) = query_results
        # construct VSI paths; sample (split into lines):
        # /vsis3_streaming/landsat-pds/c1/L8/013/030
        #   /LC08_L1TP_013030_20171128_20171207_01_T1
        #   /LC08_L1TP_013030_20171128_20171207_01_T1_B10.TIF
        # see also:  http://www.gdal.org/gdal_virtual_file_systems.html
        vsi_prefix = '/vsis3_streaming/{}/'.format(cls._bucket_name)
        asset_content = {
            # can/should add metadata/versioning info here
            '30m-bands': [vsi_prefix + t for t in _30m_tifs],
            '15m-band': vsi_prefix + _15m_tif,
            'qa-band': vsi_prefix + qa_tif,
            'mtl': cls._s3_url + mtl_txt,
        }

        with utils.make_temp_dir(prefix='fetch',
                                 dir=cls.Repository.path('stage')) as tmp_dir:
            tmp_fp = tmp_dir + '/' + filename
            with open(tmp_fp, 'w') as tfo:
                json.dump(asset_content, tfo)
            shutil.copy(tmp_fp, cls.Repository.path('stage'))

    @classmethod
    def query_service(cls, asset, tile, date, pcover=90.0):
        """As superclass with optional argument:

        Finds assets matching the arguments, where pcover is maximum
        permitted cloud cover %.
        """
        available = []

        if asset in ['DN', 'SR']:
            verbose_out('Landsat "{}" assets are no longer fetchable'.format(
                    asset), 6)
            return available

        path = tile[:3]
        row = tile[3:]
        fdate = date.strftime('%Y-%m-%d')
        cls.load_ee_search_keys()
        api_key = cls.ee_login()
        available = []
        from usgs import api
        for dataset in cls._ee_datasets.keys():
            response = api.search(
                dataset, 'EE',
                start_date=fdate, end_date=fdate,
                where={
                    cls._ee_datasets[dataset]['WRS Path']: path,
                    cls._ee_datasets[dataset]['WRS Row']: row,
                },
                api_key=api_key
            )['data']

            for result in response['results']:
                metadata = requests.get(result['metadataUrl']).text
                xml = ElementTree.fromstring(metadata)
                # Indexing an Element instance returns it's children
                scene_cloud_cover = xml.find(
                    ".//{http://earthexplorer.usgs.gov/eemetadata.xsd}metadataField[@name='Scene Cloud Cover']"
                )[0].text
                land_cloud_cover = xml.find(
                    ".//{http://earthexplorer.usgs.gov/eemetadata.xsd}metadataField[@name='Land Cloud Cover']"
                )[0].text

                if float(scene_cloud_cover) < pcover:
                    available.append({
                        'basename': result['displayId'] + '.tar.gz',
                        'sceneID': result['entityId'],
                        'dataset': dataset,
                        'sceneCloudCover': float(scene_cloud_cover),
                        'landCloudCover': float(land_cloud_cover),
                    })

        return available

    @classmethod
    def fetch(cls, asset, tile, date):
        # If the user wants to use AWS S3 landsat data, don't fetch
        # standard C1 assets, which come from conventional USGS data sources.
        data_src = cls.Repository.get_setting('source')
        if data_src not in ('s3', 'usgs'):
            raise ValueError("Data source '{}' is not known"
                             " (expected 's3' or 'usgs')".format(data_src))
        if (data_src, asset) == ('s3', 'C1S3'):
            cls.fetch_s3(tile, date)
            return
        if (data_src, asset) in [('usgs', 'C1S3'), ('s3', 'C1')]:
            return
        # else proceed as usual:

        fdate = date.strftime('%Y-%m-%d')
        response = cls.query_service(asset, tile, date)
        if len(response) > 0:
            verbose_out('Fetching %s %s %s' % (asset, tile, fdate), 1)
            if len(response) != 1:
                raise Exception('Single date, single location, '
                                'returned more than one result')
            result = response[0]
            utils.verbose_out(str(response), 4)
            sceneID = result['sceneID']
            stage_dir = cls.Repository.path('stage')
            sceneIDs = [str(sceneID)]

            api_key = cls.ee_login()
            from usgs import api
            url = api.download(
                result['dataset'], 'EE', sceneIDs, 'STANDARD', api_key
            )['data'][0]
            with utils.make_temp_dir(prefix='dwnld', dir=stage_dir) as dldir:
                homura.download(url, dldir)

                granules = os.listdir(dldir)
                if len(granules) == 0:
                    raise Exception(
                        'Download appears to have not produced a file: {}'
                        .format(str(granules))
                    )
                os.rename(
                    os.path.join(dldir, granules[0]),
                    os.path.join(stage_dir, granules[0]),
                )


def unitless_bands(*bands):
    return [{'name': b, 'units': Data._unitless} for b in bands]


class landsatData(Data):
    name = 'Landsat'
    version = '1.0.1'

    Asset = landsatAsset

    _lt5_startdate = date(1984, 3, 1)
    _lc8_startdate = date(2013, 5, 30)

    # Group products belong to ('Standard' if not specified)
    _productgroups = {
        'Index': ['bi', 'evi', 'lswi', 'msavi2', 'ndsi', 'ndvi', 'ndwi',
                  'satvi', 'vari'],
        'Tillage': ['ndti', 'crc', 'sti', 'isti'],
        'LC8SR': ['ndvi8sr'],
        'ACOLITE': [
            'rhow', 'oc2chl', 'oc3chl', 'fai', 'spm655', 'turbidity',
            'acoflags',
            # 'rhoam',  # Dropped for the moment due to issues in ACOLITE
        ],
    }
    __toastring = 'toa: use top of the atmosphere reflectance'
    __visible_bands_union = [color for color in Asset._sensors['LC8']['colors'] if 'LWIR' not in color]

    # note C1 products are also C1S3 products; they're added in below
    # TODO don't use manual tables of repeated information in the first place
    _products = {
        #'Standard':
        'rad': {
            'assets': ['DN', 'C1'],
            'description': 'Surface-leaving radiance',
            'arguments': [__toastring],
            'startdate': _lt5_startdate,
            'latency': 1,
            # units given by https://landsat.usgs.gov/landsat-8-l8-data-users-handbook-section-5
            'bands': [{'name': n, 'units': 'W/m^2/sr/um'} for n in __visible_bands_union],
        },
        'ref': {
            'assets': ['DN', 'C1'],
            'description': 'Surface reflectance',
            'arguments': [__toastring],
            'startdate': _lt5_startdate,
            'latency': 1,
            'bands': unitless_bands(*__visible_bands_union)
        },
        'temp': {
            'assets': ['DN', 'C1'],
            'description': 'Brightness (apparent) temperature',
            'toa': True,
            'startdate': _lt5_startdate,
            'latency': 1,
            # units given by https://landsat.usgs.gov/landsat-8-l8-data-users-handbook-section-5
            'bands': [{'name': n, 'units': 'degree Kelvin'} for n in ['LWIR', 'LWIR2']],
        },
        'acca': {
            'assets': ['DN', 'C1'],
            'description': 'Automated Cloud Cover Assessment',
            'arguments': [
                'X: erosion kernel diameter in pixels (default: 5)',
                'Y: dilation kernel diameter in pixels (default: 10)',
                'Z: cloud height in meters (default: 4000)'
            ],
            'nargs': '*',
            'toa': True,
            'startdate': _lt5_startdate,
            'latency': 1,
            # percentage, so unitless, per landsat docs:
            # https://landsat.usgs.gov/how-percentage-cloud-cover-calculated
            'bands': unitless_bands('finalmask', 'cloudmask', 'ambclouds', 'pass1'),
        },
        'fmask': {
            'assets': ['DN', 'C1'],
            'description': 'Fmask cloud cover',
            'nargs': '*',
            'toa': True,
            'startdate': _lt5_startdate,
            'latency': 1,
            'bands': unitless_bands('finalmask', 'cloudmask',
                                    'PCP', 'clearskywater', 'clearskyland'),
        },
        'cloudmask': {
            'assets': ['C1'],
            'description': 'Cloud (and shadow) mask product based on cloud bits of the quality band',
            'toa': True,
            'startdate': _lt5_startdate,
            'latency': 1,
            'bands': unitless_bands('cloudmask'),
        },
        'tcap': {
            'assets': ['DN', 'C1'],
            'description': 'Tassled cap transformation',
            'toa': True,
            'startdate': _lt5_startdate,
            'latency': 1,
            'bands': unitless_bands('Brightness', 'Greenness', 'Wetness', 'TCT4', 'TCT5', 'TCT6'),
        },
        'dn': {
            'assets': ['DN', 'C1'],
            'description': 'Raw digital numbers',
            'toa': True,
            'startdate': _lt5_startdate,
            'latency': 1,
            'bands': [{'name': n, 'units': 'W/m^2/sr/um'} for n in __visible_bands_union],
        },
        'volref': {
            'assets': ['DN', 'C1'],
            'description': 'Volumetric water reflectance - valid for water only',
            'arguments': [__toastring],
            'startdate': _lt5_startdate,
            'latency': 1,
            # reflectance is unitless therefore volref should be unitless
            'bands': unitless_bands(*__visible_bands_union),
        },
        'wtemp': {
            'assets': ['DN', 'C1'],
            'description': 'Water temperature (atmospherically correct) - valid for water only',
            # It's not really TOA, but the product code will take care of atm correction itself
            'toa': True,
            'startdate': _lt5_startdate,
            'latency': 1,
            'bands': [{'name': n, 'units': 'degree Kelvin'} for n in ['LWIR', 'LWIR2']],
        },
        'bqa': {
            'assets': ['DN', 'C1'],
            # TODO prior description was too long; is this a good-enough short replacement?
            'description': 'The quality band extracted into separate layers.',
            # 'description': ('The bit-packed information in the QA bands is translation of binary strings. '
            # 'As a simple example, the integer value "1" translates to the binary value "0001." The binary value '
            # '"0001" has 4 bits, written right to left as bits 0 ("1"), 1 ("0"), 2 ("0"), and 3 ("0"). '
            # 'Each of the bits 0-3 represents a yes/no indication of a physical value.'),
            'toa': True,
            'startdate': _lc8_startdate,
            'latency': 1,
            'bands': unitless_bands('allgood', 'notfilled', 'notdropped', 'notterrain',
                                    'notsnow', 'notcirrus', 'notcloud'),
        },
        'bqashadow': {
            'assets': ['DN', 'C1'],
            'description': 'LC8 QA + Shadow Smear',
            'arguments': [
                'X: erosion kernel diameter in pixels (default: 5)',
                'Y: dilation kernel diameter in pixels (default: 10)',
                'Z: cloud height in meters (default: 4000)'
            ],
            'nargs': '*',
            'toa': True,
            'startdate': _lc8_startdate,
            'latency': 1,
            'bands': unitless_bands('bqashadow'),
        },
        #'Indices': {
        'bi': {
            'assets': ['DN', 'C1'],
            'description': 'Brightness Index',
            'arguments': [__toastring],
            'startdate': _lt5_startdate,
            'latency': 1,
            'bands': unitless_bands('bi'),
        },
        'evi': {
            'assets': ['DN', 'C1'],
            'description': 'Enhanced Vegetation Index',
            'arguments': [__toastring],
            'startdate': _lt5_startdate,
            'latency': 1,
            'bands': unitless_bands('evi'),
        },
        'lswi': {
            'assets': ['DN', 'C1'],
            'description': 'Land Surface Water Index',
            'arguments': [__toastring],
            'startdate': _lt5_startdate,
            'latency': 1,
            'bands': unitless_bands('lswi'),
        },
        'msavi2': {
            'assets': ['DN', 'C1'],
            'description': 'Modified Soil-Adjusted Vegetation Index (revised)',
            'arguments': [__toastring],
            'startdate': _lt5_startdate,
            'latency': 1,
            'bands': unitless_bands('msavi2'),
        },
        'ndsi': {
            'assets': ['DN', 'C1'],
            'description': 'Normalized Difference Snow Index',
            'arguments': [__toastring],
            'startdate': _lt5_startdate,
            'latency': 1,
            'bands': unitless_bands('ndsi'),
        },
        'ndvi': {
            'assets': ['DN', 'C1'],
            'description': 'Normalized Difference Vegetation Index',
            'arguments': [__toastring],
            'startdate': _lt5_startdate,
            'latency': 1,
            'bands': unitless_bands('ndvi'),
        },
        'ndwi': {
            'assets': ['DN', 'C1'],
            'description': 'Normalized Difference Water Index',
            'arguments': [__toastring],
            'startdate': _lt5_startdate,
            'latency': 1,
            'bands': unitless_bands('ndwi'),
        },
        'satvi': {
            'assets': ['DN', 'C1'],
            'description': 'Soil-Adjusted Total Vegetation Index',
            'arguments': [__toastring],
            'startdate': _lt5_startdate,
            'latency': 1,
            'bands': unitless_bands('satvi'),
        },
        'vari': {
            'assets': ['DN', 'C1'],
            'description': 'Visible Atmospherically Resistant Index',
            'arguments': [__toastring],
            'startdate': _lt5_startdate,
            'latency': 1,
            'bands': unitless_bands('vari'),
        },
        #'Tillage Indices': {
        'ndti': {
            'assets': ['DN', 'C1'],
            'description': 'Normalized Difference Tillage Index',
            'arguments': [__toastring],
            'startdate': _lt5_startdate,
            'latency': 1,
            'bands': unitless_bands('ndti'),
        },
        'crc': {
            'assets': ['DN', 'C1'],
            'description': 'Crop Residue Cover',
            'arguments': [__toastring],
            'startdate': _lt5_startdate,
            'latency': 1,
            'bands': unitless_bands('crc'),
        },
        'sti': {
            'assets': ['DN', 'C1'],
            'description': 'Standard Tillage Index',
            'arguments': [__toastring],
            'startdate': _lt5_startdate,
            'latency': 1,
            'bands': unitless_bands('sti'),
        },
        'isti': {
            'assets': ['DN', 'C1'],
            'description': 'Inverse Standard Tillage Index',
            'arguments': [__toastring],
            'startdate': _lt5_startdate,
            'latency': 1,
            'bands': unitless_bands('isti'),
        },
        # NEW!!!
        'ndvi8sr': {
            'assets': ['SR'],
            'description': 'Normalized Difference Vegetation from LC8SR',
            'startdate': _lc8_startdate,
            'latency': 1,
            'bands': unitless_bands('ndvi8sr'),
        },
        'landmask': {
            'assets': ['SR'],
            'description': 'Land mask from LC8SR',
            'startdate': _lc8_startdate,
            'latency': 1,
            'bands': unitless_bands('landmask'),
        },
    }

    gips.atmosphere.add_acolite_product_dicts(_products, 'DN', 'C1')

    for pname, pdict in _products.items():
        if 'C1' in pdict['assets']:
            pdict['assets'].append('C1S3')

    for product, product_info in _products.iteritems():
        product_info['startdate'] = min(
            [landsatAsset._assets[asset]['startdate']
                for asset in product_info['assets']]
        )

        if 'C1' in product_info['assets']:
            product_info['latency'] = landsatAsset._assets['C1']['latency']
        else:
            product_info['latency'] = float("inf")

    def _process_indices(self, image, metadata, sensor, indices, coreg_shift=None):
        """Process the given indices and add their files to the inventory.

        Image is a GeoImage suitable for generating the indices.
        Metadata is passed in to the gippy Indices() call.  Sensor is
        used to generate index filenames and saving info about the
        product to self. Indices is a dict of desired keys; keys and
        values are the same as requested products in process(). Coreg_shift
        is a dict with keys `x` and `y` used to make affine
        transformation for `-coreg` products.
        """
        gippy_input = {} # map prod types to temp output filenames for feeding to gippy
        tempfps_to_ptypes = {} # map temp output filenames to prod types, for AddFile
        for prod_type, pt_split in indices.items():
            temp_fp = self.temp_product_filename(sensor, prod_type)
            gippy_input[pt_split[0]] = temp_fp
            tempfps_to_ptypes[temp_fp] = prod_type

        prodout = Indices(image, gippy_input, metadata)

        if coreg_shift:
            for key, val in prodout.iteritems():
                self._time_report("coregistering index")
                img = gippy.GeoImage(val, True)
                affine = img.Affine()
                affine[0] += coreg_shift.get('x', 0.0)
                affine[3] += coreg_shift.get('y', 0.0)
                img.SetAffine(affine)
                img.Process()
                img = None

        for temp_fp in prodout.values():
            archived_fp = self.archive_temp_path(temp_fp)
            self.AddFile(sensor, tempfps_to_ptypes[temp_fp], archived_fp)


    @Data.proc_temp_dir_manager
    def process(self, products=None, overwrite=False, **kwargs):
        """ Make sure all products have been processed """
        products = super(landsatData, self).process(products, overwrite, **kwargs)
        if len(products) == 0:
            verbose_out("Skipping processing; no products requested.", 5)
            return
        if len(self.assets) == 0:
            verbose_out("Skipping processing; no assets found.", 5)
            return

        start = datetime.now()

        if set(self.assets.keys()) == set(['C1', 'DN']):
            if 'C1' in self.assets: # prefer C1
                asset = 'C1'
            elif 'DN' in self.assets:
                asset = 'DN'
            else:
                raise ValueError(
                    'No valid asset found for C1 nor DN for {} {}'.format(
                        self.basename))
        else:
            if len(self.assets) > 1:
                # TODO document the reason why not
                raise ValueError("Cannot create products from"
                                 " this combination of assets:  {}".format(assets))
            asset = self.assets.keys()[0]

        # TODO: De-hack this
        # Better approach, but needs some thought, is to loop over assets
        # Ian, you are right. I just don't have enough time to do it.

        if asset == 'SR':

            datafiles = self.assets['SR'].datafiles()

            imgpaths = dict()

            for datafile in datafiles:

                key = datafile.partition('_')[2].split('.')[0]
                path = os.path.join('/vsitar/' + self.assets['SR'].filename, datafile)

                imgpaths[key] = path

            # print imgpaths

            sensor = 'LC8SR'

            for key, val in products.requested.items():
                fname = self.temp_product_filename(sensor, key)

                if val[0] == "ndvi8sr":
                    img = gippy.GeoImage([imgpaths['sr_band4'], imgpaths['sr_band5']])

                    missing = float(img[0].NoDataValue())

                    red = img[0].Read().astype('float32')
                    nir = img[1].Read().astype('float32')

                    wvalid = numpy.where((red != missing) & (nir != missing) & (red + nir != 0.0))

                    red[wvalid] *= 1.E-4
                    nir[wvalid] *= 1.E-4

                    # TODO: change this so that these pixels become missing
                    red[(red != missing) & (red < 0.0)] = 0.0
                    red[red > 1.0] = 1.0
                    nir[(nir != missing) & (nir < 0.0)] = 0.0
                    nir[nir > 1.0] = 1.0

                    ndvi = missing + numpy.zeros_like(red)
                    ndvi[wvalid] = ((nir[wvalid] - red[wvalid]) /
                                    (nir[wvalid] + red[wvalid]))

                    verbose_out("writing " + fname, 2)
                    imgout = gippy.GeoImage(fname, img, gippy.GDT_Float32, 1)
                    imgout.SetNoData(-9999.)
                    imgout.SetOffset(0.0)
                    imgout.SetGain(1.0)
                    imgout.SetBandName('NDVI', 1)
                    imgout[0].Write(ndvi)

                if val[0] == "landmask":
                    img = gippy.GeoImage([imgpaths['cfmask'], imgpaths['cfmask_conf']])

                    cfmask = img[0].Read()
                    # array([  0,   1,   2,   3,   4, 255], dtype=uint8)
                    # 0 means clear! but I want 1 to mean clear

                    cfmask[cfmask > 0] = 2
                    cfmask[cfmask == 0] = 1
                    cfmask[cfmask == 2] = 0

                    verbose_out("writing " + fname, 2)
                    imgout = gippy.GeoImage(fname, img, gippy.GDT_Byte, 1)
                    imgout.SetBandName('Land mask', 1)
                    imgout[0].Write(cfmask)

                archive_fp = self.archive_temp_path(fname)
                self.AddFile(sensor, key, archive_fp)

        elif asset in ('DN', 'C1', 'C1S3'):

            # This block contains everything that existed in the first generation Landsat driver

            # Add the sensor for this date to the basename
            self.basename = self.basename + '_' + self.sensors[asset]

            # Read the assets
            with utils.error_handler('Error reading ' + basename(self.assets[asset].filename)):
                img = self._readraw(asset)

            meta = self.assets[asset].meta['bands']
            visbands = self.assets[asset].visbands
            lwbands = self.assets[asset].lwbands
            md = self.meta_dict()

            product_is_coreg = [(v and 'coreg' in v) for v in products.requested.values()]
            coreg = all(product_is_coreg)
            if not coreg and any(product_is_coreg):
                # Disallow coreg and non-coreg products in same processing
                # call both to avoid having to check each if each product
                # needs to be shifted as well as a hint to users who will
                # likely only do this as an accident anyway.
                raise ValueError("Mixing coreg and non-coreg products is not allowed")
            if coreg:
                if not glob.glob(os.path.join(self.path, "*coreg_args.txt")):
                    # run arop and store coefficients
                    with utils.make_temp_dir() as tmpdir:
                        s2_export = self.sentinel2_coreg_export(tmpdir)
                        self.run_arop(s2_export)
                coreg_xshift, coreg_yshift = self.parse_coreg_coefficients()

            # running atmosphere if any products require it
            toa = True
            for val in products.requested.values():
                toa = toa and (self._products[val[0]].get('toa', False) or 'toa' in val)
            if not toa:
                start = datetime.now()

                if not settings().REPOS[self.Repository.name.lower()]['6S']:
                    raise Exception('6S is required for atmospheric correction')
                with utils.error_handler('Problem running 6S atmospheric model'):
                    wvlens = [(meta[b]['wvlen1'], meta[b]['wvlen2']) for b in visbands]
                    geo = self.metadata['geometry']
                    atm6s = SIXS(visbands, wvlens, geo, self.metadata['datetime'],
                                 sensor=self.sensor_set[0])
                    md["AOD Source"] = str(atm6s.aod[0])
                    md["AOD Value"] = str(atm6s.aod[1])

            # Break down by group
            groups = products.groups()
            # ^--- has the info about what products the user requested

            # create non-atmospherically corrected apparent reflectance and temperature image
            reflimg = gippy.GeoImage(img)
            theta = numpy.pi * self.metadata['geometry']['solarzenith'] / 180.0
            sundist = (1.0 - 0.016728 * numpy.cos(numpy.pi * 0.9856 * (float(self.day) - 4.0) / 180.0))
            for col in self.assets[asset].visbands:
                reflimg[col] = img[col] * (1.0 /
                        ((meta[col]['E'] * numpy.cos(theta)) / (numpy.pi * sundist * sundist)))
            for col in self.assets[asset].lwbands:
                reflimg[col] = (((img[col].pow(-1)) * meta[col]['K1'] + 1).log().pow(-1)
                        ) * meta[col]['K2'] - 273.15

            # This is landsat, so always just one sensor for a given date
            sensor = self.sensors[asset]

            # Process standard products (this is in the 'DN' block)
            for key, val in groups['Standard'].items():
                start = datetime.now()
                # TODO - update if no atmos desired for others
                toa = self._products[val[0]].get('toa', False) or 'toa' in val
                # Create product
                with utils.error_handler(
                        'Error creating product {} for {}'
                        .format(key, basename(self.assets[asset].filename)),
                        continuable=True):
                    fname = self.temp_product_filename(sensor, key)
                    if val[0] == 'acca':
                        s_azim = self.metadata['geometry']['solarazimuth']
                        s_elev = 90 - self.metadata['geometry']['solarzenith']
                        erosion, dilation, cloudheight = 5, 10, 4000
                        if len(val) >= 4:
                            erosion, dilation, cloudheight = [int(v) for v in val[1:4]]
                        resset = set(
                            [(reflimg[band].Resolution().x(),
                              reflimg[band].Resolution().y())
                             for band in (self.assets[asset].visbands +
                                          self.assets[asset].lwbands)]
                        )
                        if len(resset) > 1:
                            raise Exception(
                                'ACCA requires all bands to have the same '
                                'spatial resolution.  Found:\n\t' + str(resset)
                            )
                        imgout = ACCA(reflimg, fname, s_elev, s_azim, erosion, dilation, cloudheight)
                    elif val[0] == 'fmask':
                        tolerance, dilation = 3, 5
                        if len(val) >= 3:
                            tolerance, dilation = [int(v) for v in val[1:3]]
                        imgout = Fmask(reflimg, fname, tolerance, dilation)

                    elif val[0] == 'cloudmask':
                        qaimg = self._readqa(asset)
                        npqa = qaimg.Read()  # read image file into numpy array
                        # https://landsat.usgs.gov/collectionqualityband
                        # cloudmaskmask = (cloud and (cc_med or cc_high)) or csc_med or csc_high
                        # cloud iff bit 4
                        # (cc_med or cc_high) iff bit 6
                        # (csc_med or csc_high) iff bit 8

                        # GIPPY 1.0 note: rewrite this whole product after
                        # adding get_bit method to GeoRaster

                        def get_bit(np_array, i):
                            """Return an array with the ith bit extracted from each cell."""
                            return (np_array >> i) & 0b1

                        np_cloudmask = numpy.logical_not(
                            get_bit(npqa, 4) &
                            get_bit(npqa, 6) |
                            get_bit(npqa, 8)
                        )

                        erosion_width = 10
                        elem = numpy.ones((erosion_width,) * 2, dtype='uint8')
                        np_cloudmask_eroded = binary_erosion(
                            np_cloudmask, structure=elem,
                        ).astype('uint8')
                        np_cloudmask_eroded *= (npqa != 1)
                        #

                        imgout = gippy.GeoImage(fname, img, gippy.GDT_Byte, 1)
                        verbose_out("writing " + fname, 2)
                        imgout.SetBandName(
                            self._products[val[0]]['bands'][0]['name'], 1
                        )
                        imgout.SetMeta('GIPS_LANDSAT_VERSION', self.version)
                        imgout.SetMeta('GIPS_C1_ERODED_PIXELS', str(erosion_width))

                        ####################
                        # GIPPY1.0 note: replace this block with
                        # imgout[0].set_nodata(0.)
                        # imout[0].write_raw(np_cloudmask_eroded)
                        imgout[0].Write(
                            np_cloudmask_eroded
                        )
                        imgout = None
                        imgout = gippy.GeoImage(fname, True)
                        imgout[0].SetNoData(0.)
                        ####################
                    elif val[0] == 'rad':
                        imgout = gippy.GeoImage(fname, img, gippy.GDT_Int16, len(visbands))
                        for i in range(0, imgout.NumBands()):
                            imgout.SetBandName(visbands[i], i + 1)
                        imgout.SetNoData(-32768)
                        imgout.SetGain(0.1)
                        if toa:
                            for col in visbands:
                                img[col].Process(imgout[col])
                        else:
                            for col in visbands:
                                ((img[col] - atm6s.results[col][1]) / atm6s.results[col][0]
                                        ).Process(imgout[col])
                        # Mask out any pixel for which any band is nodata
                        #imgout.ApplyMask(img.DataMask())
                    elif val[0] == 'ref':
                        imgout = gippy.GeoImage(fname, img, gippy.GDT_Int16, len(visbands))
                        for i in range(0, imgout.NumBands()):
                            imgout.SetBandName(visbands[i], i + 1)
                        imgout.SetNoData(-32768)
                        imgout.SetGain(0.0001)
                        if toa:
                            for c in visbands:
                                reflimg[c].Process(imgout[c])
                        else:
                            for c in visbands:
                                (((img[c] - atm6s.results[c][1]) / atm6s.results[c][0])
                                        * (1.0 / atm6s.results[c][2])).Process(imgout[c])
                        # Mask out any pixel for which any band is nodata
                        #imgout.ApplyMask(img.DataMask())
                    elif val[0] == 'tcap':
                        tmpimg = gippy.GeoImage(reflimg)
                        tmpimg.PruneBands(['BLUE', 'GREEN', 'RED', 'NIR', 'SWIR1', 'SWIR2'])
                        arr = numpy.array(self.Asset._sensors[self.sensor_set[0]]['tcap']).astype('float32')
                        imgout = LinearTransform(tmpimg, fname, arr)
                        imgout.SetMeta('AREA_OR_POINT', 'Point')
                        outbands = ['Brightness', 'Greenness', 'Wetness', 'TCT4', 'TCT5', 'TCT6']
                        for i in range(0, imgout.NumBands()):
                            imgout.SetBandName(outbands[i], i + 1)
                    elif val[0] == 'temp':
                        imgout = gippy.GeoImage(fname, img, gippy.GDT_Int16, len(lwbands))
                        for i in range(0, imgout.NumBands()):
                            imgout.SetBandName(lwbands[i], i + 1)
                        imgout.SetNoData(-32768)
                        imgout.SetGain(0.1)
                        [reflimg[col].Process(imgout[col]) for col in lwbands]
                    elif val[0] == 'dn':
                        rawimg = self._readraw(asset)
                        rawimg.SetGain(1.0)
                        rawimg.SetOffset(0.0)
                        imgout = rawimg.Process(fname)
                        rawimg = None
                    elif val[0] == 'volref':
                        bands = deepcopy(visbands)
                        bands.remove("SWIR1")
                        imgout = gippy.GeoImage(fname, reflimg, gippy.GDT_Int16, len(bands))
                        [imgout.SetBandName(band, i + 1) for i, band in enumerate(bands)]
                        imgout.SetNoData(-32768)
                        imgout.SetGain(0.0001)
                        r = 0.54    # Water-air reflection
                        p = 0.03    # Internal Fresnel reflectance
                        pp = 0.54   # Water-air Fresnel reflectance
                        n = 1.34    # Refractive index of water
                        Q = 1.0     # Downwelled irradiance / upwelled radiance
                        A = ((1 - p) * (1 - pp)) / (n * n)
                        srband = reflimg['SWIR1'].Read()
                        nodatainds = srband == reflimg['SWIR1'].NoDataValue()
                        for band in bands:
                            bimg = reflimg[band].Read()
                            diffimg = bimg - srband
                            diffimg = diffimg / (A + r * Q * diffimg)
                            diffimg[bimg == reflimg[band].NoDataValue()] = imgout[band].NoDataValue()
                            diffimg[nodatainds] = imgout[band].NoDataValue()
                            imgout[band].Write(diffimg)
                    elif val[0] == 'wtemp':
                        raise NotImplementedError('See https://gitlab.com/appliedgeosolutions/gips/issues/155')
                        imgout = gippy.GeoImage(fname, img, gippy.GDT_Int16, len(lwbands))
                        [imgout.SetBandName(lwbands[i], i + 1) for i in range(0, imgout.NumBands())]
                        imgout.SetNoData(-32768)
                        imgout.SetGain(0.1)
                        tmpimg = gippy.GeoImage(img)
                        for col in lwbands:
                            band = tmpimg[col]
                            m = meta[col]
                            lat = self.metadata['geometry']['lat']
                            lon = self.metadata['geometry']['lon']
                            dt = self.metadata['datetime']
                            atmos = MODTRAN(m['bandnum'], m['wvlen1'], m['wvlen2'], dt, lat, lon, True)
                            e = 0.95
                            band = (tmpimg[col] - (atmos.output[1] + (1 - e) * atmos.output[2])
                                    ) / (atmos.output[0] * e)
                            band = (((band.pow(-1)) * meta[col]['K1'] + 1).log().pow(-1)
                                    ) * meta[col]['K2'] - 273.15
                            band.Process(imgout[col])

                    elif val[0] == 'bqa':
                        if 'LC8' not in self.sensor_set:
                            continue
                        imgout = gippy.GeoImage(fname, img, gippy.GDT_Int16, 7)
                        qaimg = self._readqa(asset)
                        qadata = qaimg.Read()
                        notfilled = ~binmask(qadata, 1)
                        notdropped = ~binmask(qadata, 2)
                        notterrain = ~binmask(qadata, 3)
                        notcirrus = ~binmask(qadata, 14) & binmask(qadata, 13)
                        notcloud = ~binmask(qadata, 16) & binmask(qadata, 15)
                        allgood = notfilled * notdropped * notterrain * notcirrus * notcloud
                        imgout[0].Write(allgood.astype('int16'))
                        imgout[1].Write(notfilled.astype('int16'))
                        imgout[2].Write(notdropped.astype('int16'))
                        imgout[3].Write(notterrain.astype('int16'))
                        imgout[4].Write(notsnow.astype('int16'))
                        imgout[5].Write(notcirrus.astype('int16'))
                        imgout[6].Write(notcloud.astype('int16'))

                    elif val[0] == 'bqashadow':
                        if 'LC8' not in self.sensor_set:
                            continue
                        imgout = gippy.GeoImage(fname, img, gippy.GDT_UInt16, 1)
                        imgout[0].SetNoData(0)
                        qaimg = self._readqa(asset)
                        qadata = qaimg.Read()
                        fill = binmask(qadata, 1)
                        dropped = binmask(qadata, 2)
                        terrain = binmask(qadata, 3)
                        cirrus = binmask(qadata, 14)
                        othercloud = binmask(qadata, 16)
                        cloud = (cirrus + othercloud) + 2 * (fill + dropped + terrain)
                        abfn = fname + '-intermediate'
                        abimg = gippy.GeoImage(abfn, img, gippy.GDT_UInt16, 1)
                        abimg[0].SetNoData(2)
                        abimg[0].Write(cloud.astype(numpy.uint16))
                        abimg.Process()
                        abimg = None
                        abimg = gippy.GeoImage(abfn + '.tif')

                        s_azim = self.metadata['geometry']['solarazimuth']
                        s_elev = 90 - self.metadata['geometry']['solarzenith']
                        erosion, dilation, cloudheight = 5, 10, 4000
                        if len(val) >= 4:
                            erosion, dilation, cloudheight = [int(v) for v in val[1:4]]
                        imgout = AddShadowMask(
                            abimg, imgout, 0, s_elev, s_azim, erosion,
                            dilation, cloudheight, {'notes': 'dev-version'}
                        )
                        imgout.Process()
                        abimg = None
                        os.remove(abfn + '.tif')
                    fname = imgout.Filename()
                    imgout.SetMeta(md)

                    if coreg:
                        self._time_report("Setting affine of product")
                        affine = imgout.Affine()
                        affine[0] += coreg_xshift
                        affine[3] += coreg_yshift
                        imgout.SetAffine(affine)
                        imgout.Process()

                    imgout = None
                    archive_fp = self.archive_temp_path(fname)
                    self.AddFile(sensor, key, archive_fp)
                    product_finished_msg = ' -> {}: processed in {}'.format(
                            os.path.basename(archive_fp), datetime.now() - start)
                    utils.verbose_out(product_finished_msg, level=2)

            # Process Indices (this is in the 'DN' block)
            indices0 = dict(groups['Index'], **groups['Tillage'])
            if len(indices0) > 0:
                start = datetime.now()
                indices = {}
                indices_toa = {}
                for key, val in indices0.items():
                    if 'toa' in val:
                        indices_toa[key] = val
                    else:
                        indices[key] = val

                coreg_shift = {}

                if coreg:
                    coreg_shift['x'] = coreg_xshift
                    coreg_shift['y'] = coreg_yshift

                # Run TOA
                if len(indices_toa) > 0:
                    self._process_indices(reflimg, md, sensor, indices_toa, coreg_shift)

                # Run atmospherically corrected
                if len(indices) > 0:
                    for col in visbands:
                        img[col] = ((img[col] - atm6s.results[col][1]) / atm6s.results[col][0]
                                ) * (1.0 / atm6s.results[col][2])
                    self._process_indices(img, md, sensor, indices, coreg_shift)
                verbose_out(' -> %s: processed %s in %s' % (
                        self.basename, indices0.keys(), datetime.now() - start), 1)
            img = None
            # cleanup scene directory by removing (most) extracted files
            with utils.error_handler('Error removing extracted files', continuable=True):
                if settings().REPOS[self.Repository.name.lower()]['extract']:
                    for bname in self.assets[asset].datafiles():
                        if bname[-7:] != 'MTL.txt':
                            files = glob.glob(os.path.join(self.path, bname) + '*')
                            RemoveFiles(files)
                # TODO only wtemp uses MODTRAN; do the dir removal there?
                modtran_path = os.path.join(self.path, 'modtran')
                if os.path.exists(modtran_path):
                    shutil.rmtree(modtran_path)

            if groups['ACOLITE']:
                start = datetime.now()
                # TEMPDIR FOR PROCESSING
                aco_proc_dir = tempfile.mkdtemp(
                    prefix='aco_proc_',
                    dir=os.path.join(self.Repository.path(), 'stage')
                )
                with utils.error_handler(
                        'Error creating ACOLITE products {} for {}'
                        .format(
                            groups['ACOLITE'].keys(),
                            basename(self.assets[asset].filename)
                        ),
                        continuable=True):
                    # amd is 'meta' (common to all products) and product info dicts
                    amd = {
                        'meta': md.copy()
                    }
                    for p in groups['ACOLITE']:
                        amd[p] = {
                            'fname': os.path.join(
                                self.path, self.basename + '_' + p + '.tif'
                            )
                        }
                        amd[p].update(self._products[p])
                        amd[p].pop('assets')
                    prodout = gips.atmosphere.process_acolite(
                            self.assets[asset], aco_proc_dir, amd)
                    endtime = datetime.now()
                    for k, fn in prodout.items():
                        self.AddFile(sensor, k, fn)
                    verbose_out(
                        ' -> {}: processed {} in {}'
                        .format(self.basename, prodout.keys(), endtime - start),
                        1
                    )
                shutil.rmtree(aco_proc_dir)
                ## end ACOLITE

    def filter(self, pclouds=100, sensors=None, **kwargs):
        """Check if Data object passes filter.

        User can't enter pclouds, but can pass in --sensors.  kwargs
        isn't used.
        """
        if pclouds < 100:
            if not all([a.filter(pclouds) for a in self.assets.values()]):
                return False
        if sensors:
            if type(sensors) is str:
                sensors = [sensors]
            sensors = set(sensors)
            # ideally, the data class would be trimmed by
            if not sensors.intersection(self.sensor_set):
                return False
        return True

    def meta(self, asset_type):
        """Read in Landsat metadata file and return it as a dict.

         Also saves it to self.metadata."""
        # test if metadata already read in, if so, return
        if hasattr(self, 'metadata'):
            return self.metadata

        asset_obj = self.assets[asset_type]
        c1s3_content = asset_obj.load_c1s3_json()
        if c1s3_content:
            text = requests.get(c1s3_content['mtl']).text
            qafn = c1s3_content['qa-band'].encode('ascii', 'ignore')
        else:
            datafiles = asset_obj.datafiles()
            # save for later; defaults to None
            qafn = next((f for f in datafiles if '_BQA.TIF' in f), None)
            # locate MTL file and save it to disk if it isn't saved already
            mtlfilename = next(f for f in datafiles if 'MTL.txt' in f)
            if os.path.exists(mtlfilename) and os.stat(mtlfilename).st_size:
                os.remove(mtlfilename)
            if not os.path.exists(mtlfilename):
                mtlfilename = asset_obj.extract([mtlfilename])[0]
            # Read MTL file
            with utils.error_handler(
                            'Error reading metadata file ' + mtlfilename):
                text = open(mtlfilename, 'r').read()
            if len(text) < 10:
                raise IOError('MTL file is too short. {}'.format(mtlfilename))

        sensor = asset_obj.sensor
        smeta = asset_obj._sensors[sensor]

        # Process MTL text - replace old metadata tags with new
        # NOTE This is not comprehensive, there may be others
        text = text.replace('ACQUISITION_DATE', 'DATE_ACQUIRED')
        text = text.replace('SCENE_CENTER_SCAN_TIME', 'SCENE_CENTER_TIME')

        for (ob, nb) in zip(smeta['oldbands'], smeta['bands']):
            text = re.sub(r'\WLMIN_BAND' + ob, 'RADIANCE_MINIMUM_BAND_' + nb, text)
            text = re.sub(r'\WLMAX_BAND' + ob, 'RADIANCE_MAXIMUM_BAND_' + nb, text)
            text = re.sub(r'\WQCALMIN_BAND' + ob, 'QUANTIZE_CAL_MIN_BAND_' + nb, text)
            text = re.sub(r'\WQCALMAX_BAND' + ob, 'QUANTIZE_CAL_MAX_BAND_' + nb, text)
            text = re.sub(r'\WBAND' + ob + '_FILE_NAME', 'FILE_NAME_BAND_' + nb, text)
        for l in ('LAT', 'LON', 'MAPX', 'MAPY'):
            for c in ('UL', 'UR', 'LL', 'LR'):
                text = text.replace('PRODUCT_' + c + '_CORNER_' + l, 'CORNER_' + c + '_' + l + '_PRODUCT')
        text = text.replace('\x00', '')
        # Remove junk
        lines = text.split('\n')
        mtl = dict()
        for l in lines:
            meta = l.replace('\"', "").strip().split('=')
            if len(meta) > 1:
                key = meta[0].strip()
                item = meta[1].strip()
                if key != "GROUP" and key != "END_GROUP":
                    mtl[key] = item

        # Extract useful metadata
        lats = (float(mtl['CORNER_UL_LAT_PRODUCT']), float(mtl['CORNER_UR_LAT_PRODUCT']),
                float(mtl['CORNER_LL_LAT_PRODUCT']), float(mtl['CORNER_LR_LAT_PRODUCT']))
        lons = (float(mtl['CORNER_UL_LON_PRODUCT']), float(mtl['CORNER_UR_LON_PRODUCT']),
                float(mtl['CORNER_LL_LON_PRODUCT']), float(mtl['CORNER_LR_LON_PRODUCT']))
        lat = (min(lats) + max(lats)) / 2.0
        lon = (min(lons) + max(lons)) / 2.0
        dt = datetime.strptime(mtl['DATE_ACQUIRED'] + ' ' + mtl['SCENE_CENTER_TIME'][:-2], '%Y-%m-%d %H:%M:%S.%f')
        clouds = 0.0
        with utils.error_handler('Error reading CLOUD_COVER metadata', continuable=True):
            # CLOUD_COVER isn't trusted for unknown reasons; previously errors were silenced, but
            # now maybe explicit error reports will reveal something.
            clouds = float(mtl['CLOUD_COVER'])

        filenames = []
        gain = []
        offset = []
        dynrange = []
        for i, b in enumerate(smeta['bands']):
            minval = int(float(mtl['QUANTIZE_CAL_MIN_BAND_' + b]))
            maxval = int(float(mtl['QUANTIZE_CAL_MAX_BAND_' + b]))
            minrad = float(mtl['RADIANCE_MINIMUM_BAND_' + b])
            maxrad = float(mtl['RADIANCE_MAXIMUM_BAND_' + b])
            gain.append((maxrad - minrad) / (maxval - minval))
            offset.append(minrad)
            dynrange.append((minval, maxval))
            filenames.append(mtl['FILE_NAME_BAND_' + b].strip('\"'))

        _geometry = {
            'solarzenith': (90.0 - float(mtl['SUN_ELEVATION'])),
            'solarazimuth': float(mtl['SUN_AZIMUTH']),
            'zenith': 0.0,
            'azimuth': 180.0,
            'lat': lat,
            'lon': lon,
        }

        self.metadata = {
            'filenames': filenames,
            'gain': gain,
            'offset': offset,
            'dynrange': dynrange,
            'geometry': _geometry,
            'datetime': dt,
            'clouds': clouds,
            'qafilename': qafn,
        }
        #self.metadata.update(smeta)
        return self.metadata

    @classmethod
    def meta_dict(cls):
        meta = super(landsatData, cls).meta_dict()
        meta['GIPS-landsat Version'] = cls.version
        return meta

    def _readqa(self, asset_type):
        md = self.meta(asset_type)
        if asset_type == 'C1S3':
            return gippy.GeoImage(md['qafilename'])
        if settings().REPOS[self.Repository.name.lower()]['extract']:
            # Extract files
            qadatafile = self.assets[asset_type].extract([md['qafilename']])
        else:
            # Use tar.gz directly using GDAL's virtual filesystem
            qadatafile = os.path.join(
                    '/vsitar/' + self.assets[asset_type].filename,
                    md['qafilename'])
        qaimg = gippy.GeoImage(qadatafile)
        return qaimg

    def _readraw(self, asset_type):
        """ Read in Landsat bands using original tar.gz file """
        start = datetime.now()
        asset_obj = self.assets[asset_type]

        md = self.meta(asset_type)

        data_src = self.Repository.get_setting('source')
        s3_mode = (data_src, asset_type) == ('s3', 'C1S3')
        if s3_mode:
            asset_json = asset_obj.load_c1s3_json()
            # json module insists on returning unicode, which gippy no likey
            ascii_paths = [p.encode('ascii','ignore')
                           for p in asset_json['30m-bands']]
            image = gippy.GeoImage(ascii_paths)
        else:
            if settings().REPOS[self.Repository.name.lower()]['extract']:
                # Extract all files
                datafiles = asset_obj.extract(md['filenames'])
            else:
                # Use tar.gz directly using GDAL's virtual filesystem
                datafiles = [os.path.join('/vsitar/' + asset_obj.filename, f)
                        for f in md['filenames']]
            image = gippy.GeoImage(datafiles)

        image.SetNoData(0)

        # TODO - set appropriate metadata
        #for key,val in meta.iteritems():
        #    image.SetMeta(key,str(val))

        # Geometry used for calculating incident irradiance
        # colors = self.assets['DN']._sensors[self.sensor_set[0]]['colors']

        sensor = asset_obj.sensor
        colors = asset_obj._sensors[sensor]['colors']

        for bi in range(0, len(md['filenames'])):
            image.SetBandName(colors[bi], bi + 1)
            # need to do this or can we index correctly?
            band = image[bi]
            gain = md['gain'][bi]
            band.SetGain(gain)
            band.SetOffset(md['offset'][bi])
            dynrange = md['dynrange'][bi]
            # #band.SetDynamicRange(dynrange[0], dynrange[1])
            # dynrange[0] was used internally to for conversion to radiance
            # from DN in GeoRaster.Read:
            #   img = Gain() * (img-_minDC) + Offset();  # (1)
            # and with the removal of _minDC and _maxDC it is now:
            #   img = Gain() * img + Offset();           # (2)
            # And 1 can be re-written as:
            #   img = Gain() * img - Gain() *
            #                       _minDC + Offset();   # (3)
            #       = Gain() * img + Offset
            #                      - _min * Gain() ;     # (4)
            # So, since the gippy now has line (2), we can add
            # the final term of (4) [as below] to keep that functionality.
            image[bi] = band - dynrange[0] * gain
            # I verified this by example.  With old gippy.GeoRaster:
            #     In [8]: a.min()
            #     Out[8]: -64.927711
            # with new version.
            #     In [20]: ascale.min() - 1*0.01298554277169103
            #     Out[20]: -64.927711800095906

        verbose_out('%s: read in %s' % (image.Basename(), datetime.now() - start), 2)
        return image

    def sentinel2_coreg_export(self, tmpdir):
        """
        Grabs closest (temporally) sentinel2 tiles and stitches them together
        to match this landsat tile's footprint.

        tmpdir is a directory name
        """
        from gips.data.sentinel2 import sentinel2Asset, sentinel2Data
        landsat_shp = landsatRepository.get_setting('tiles')
        spatial_extent = SpatialExtent.factory(sentinel2Data, site=landsat_shp, where="pr = '{}'".format(self.id), pcov=33.0)[0]
        fetch = False

        # If there is no available sentinel2 scene on that day, search before and after
        # until one is found.
        delta = timedelta(1)

        if self.date < sentinel2Asset._assets['L1C']['startdate']:
            date_found = starting_date = date(2017, self.date.month, self.date.day)
        else:
            date_found = starting_date = self.date

        temporal_extent = TemporalExtent(starting_date.strftime("%Y-%j"))
        self._time_report("querying for most recent sentinel2 images")
        inventory = DataInventory(sentinel2Data, spatial_extent, temporal_extent, fetch=fetch)

        while len(inventory) == 0:
            if delta > timedelta(90):
                raise ValueError("No sentinel2 data could be found within 180 days")

            temporal_extent = TemporalExtent((starting_date + delta).strftime("%Y-%j"))
            inventory = DataInventory(sentinel2Data, spatial_extent, temporal_extent, fetch=fetch)

            if len(inventory) != 0:
                date_found = starting_date + delta
                break

            temporal_extent = TemporalExtent((starting_date - delta).strftime("%Y-%j"))
            inventory = DataInventory(sentinel2Data, spatial_extent, temporal_extent, fetch=fetch)

            date_found = starting_date - delta
            delta += timedelta(1)

        geo_images = []
        tiles = inventory[date_found].tiles.keys()
        for tile in tiles:
            asset = inventory[date_found][tile].assets['L1C']
            band_8 = [f for f in asset.datafiles() if f.endswith('B08.jp2')]
            asset.extract(band_8, tmpdir)
            geo_images.append(os.path.join(tmpdir, band_8[0]))

        self._time_report("merge sentinel images to bin")
        merge_args = ["gdal_merge.py", "-o", tmpdir + "/sentinel_mosaic.bin", "-of", "ENVI", "-a_nodata", "0"]
        # only use images that are in the same proj as landsat tile
        merge_args.extend([i for i in geo_images if basename(i)[1:3] == self.utm_zone()])
        subprocess.call(merge_args)

        self._time_report("done with s2 export")
        return tmpdir + '/sentinel_mosaic.bin'

    def run_arop(self, base_band_filename):
        """
        Runs AROP's `ortho` program.

        base_band_filename is the filename of the sentinel2 image you want
        to warp to
        """
        warp_tile = self.id
        warp_date = self.date

        with utils.make_temp_dir() as tmpdir:
            warp_data = landsatData(warp_tile, warp_date, "%Y%j")
            warp_band_filenames = [f for f in warp_data.assets['C1'].datafiles() if f.endswith("B5.TIF")]
            warp_data.assets['C1'].extract(filenames=warp_band_filenames, path=tmpdir)

            warp_bands_bin = []
            for band in warp_band_filenames:
                band_bin = basename(band) + '.bin'
                subprocess.call(["gdal_translate", "-of", "ENVI", os.path.join(tmpdir, band), os.path.join(tmpdir, band_bin)])
                warp_bands_bin.append(band_bin)

            # make parameter file
            with open(os.path.join(os.path.dirname(__file__), 'input_file_tmp.inp'), 'r') as input_template:
                template = input_template.read()

            base_band_img = gippy.GeoImage(base_band_filename)
            warp_base_band_filename = [f for f in warp_bands_bin if f.endswith("B5.bin")][0]
            warp_base_band_img = gippy.GeoImage(os.path.join(tmpdir, warp_base_band_filename))
            base_pixel_size = abs(base_band_img.Resolution().x())
            warp_pixel_size = abs(warp_base_band_img.Resolution().x())
            out_pixel_size = max(base_pixel_size, warp_pixel_size)
            parameters = template.format(
                base_satellite='Sentinel2',
                base_band=base_band_filename,
                base_nsample=base_band_img.XSize(),
                base_nline=base_band_img.YSize(),
                base_pixel_size=base_pixel_size,
                base_upper_left_x=base_band_img.MinXY().x(),
                base_upper_left_y=base_band_img.MaxXY().y(),
                base_utm=self.utm_zone(),
                warp_satellite='Landsat8',
                warp_nbands=len(warp_bands_bin),
                warp_bands=' '.join([os.path.join(tmpdir, band) for band in warp_bands_bin]),
                warp_base_band=os.path.join(tmpdir, warp_base_band_filename),
                warp_data_type=' '.join((['2'] * len(warp_bands_bin))),
                warp_nsample=warp_base_band_img.XSize(),
                warp_nline=warp_base_band_img.YSize(),
                warp_pixel_size=warp_pixel_size,
                warp_upper_left_x=warp_base_band_img.MinXY().x(),
                warp_upper_left_y=warp_base_band_img.MaxXY().y(),
                warp_utm=self.utm_zone(),
                out_bands=' '.join([os.path.join(tmpdir, basename(band) + '_warped.bin') for band in warp_bands_bin]),
                out_base_band=os.path.join(tmpdir, basename(warp_base_band_filename)) + '_warped.bin',
                out_pixel_size=out_pixel_size,
                log_file='{}/cp_log.txt'.format(tmpdir),
            )

            parameter_file = os.path.join(tmpdir, 'parameter_file.inp')
            with open(parameter_file, 'w') as param_file:
                param_file.write(parameters)

            shutil.copyfile(
                os.path.join(os.path.dirname(__file__), 'lndortho.cps_par.ini'),
                os.path.join(tmpdir, 'lndortho.cps_par.ini')
            )

            subprocess.check_call(["ortho", "-r", parameter_file])
            
            with open('{}/cp_log.txt'.format(tmpdir), 'r') as log:
                xcoef_re = re.compile(r"x' += +([\d\-\.]+) +\+ +[\d\-\.]+ +\* +x +\+ +[\d\-\.]+ +\* y")
                ycoef_re = re.compile(r"y' += +([\d\-\.]+) +\+ +[\d\-\.]+ +\* +x +\+ +[\d\-\.]+ +\* y")

                for line in log:
                    x_match = xcoef_re.match(line)
                    if x_match:
                        xcoef = float(x_match.group(1))
                    y_match = ycoef_re.match(line)
                    if y_match:
                        ycoef = float(y_match.group(1))

            x_shift = ((base_band_img.MinXY().x() - warp_base_band_img.MinXY().x()) / out_pixel_size - xcoef) * out_pixel_size
            y_shift = ((base_band_img.MaxXY().y() - warp_base_band_img.MaxXY().y()) / out_pixel_size + ycoef) * out_pixel_size

            with open('{}/{}_{}_coreg_args.txt'.format(self.path, self.id, datetime.strftime(self.date, "%Y%j")), 'w') as coreg_args:
                coreg_args.write("x: {}\n".format(x_shift))
                coreg_args.write("y: {}".format(y_shift))

    def utm_zone(self):
        """
        Parse UTM zone out of `gdalinfo` output.
        """
        if getattr(self, 'utm_zone_number', None):
            return self.utm_zone_number

        asset = self.assets['C1']
        any_band = [band for band in asset.datafiles() if band.endswith("TIF")][0]
        ps = subprocess.Popen(["gdalinfo", "/vsitar/" + asset.filename + "/" + any_band], stdout=subprocess.PIPE)
        ps.wait()
        info = ps.stdout.read()
        utm_zone_re = re.compile(".+UTM[ _][Z|z]one[ _](\d{2})[N|S].+", flags=re.DOTALL)
        self.utm_zone_number = utm_zone_re.match(info).group(1)
        
        return self.utm_zone_number

    def parse_coreg_coefficients(self):
        """
        Parse out coregistration coefficients from asset's `*_coreg_args.txt`
        file.
        """
        date = datetime.strftime(self.date, "%Y%j")
        cp_log = "{}/{}_{}_coreg_args.txt".format(self.path, self.id, date)
        with open(cp_log, 'r') as log:
            xcoef_re = re.compile(r"x: (-?\d+\.?\d*)")
            ycoef_re = re.compile(r"y: (-?\d+\.?\d*)")

            for line in log:
                x_match = xcoef_re.match(line)
                if x_match:
                    xcoef = float(x_match.groups()[0])
                y_match = ycoef_re.match(line)
                if y_match:
                    ycoef = float(y_match.groups()[0])

        return xcoef, ycoef
