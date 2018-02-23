#!/usr/bin/env python
# -*- coding: utf-8 -*-
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

import os
import re
import datetime
import shapely
import numpy as np
import xml.etree.ElementTree as ET

from gips.data.core import Repository, Asset, Data
from gips.utils import VerboseOut, settings, open_vector, basename
from gips.inventory import dbinv
from gips import utils
from osgeo import gdal, osr

from shapely.wkt import loads

from pyCMR.pyCMR import CMR


# Order for ucc (Abrams, 1999) is: Band 1 high, normal, low, low2;
# Band 2 h, n, l1, l2; b3 h, n, l1, l2 (3N & 3B the same)
# Construct a dataframe for the UCC values:
ucc = np.matrix(([
                [0.676, 1.688, 2.25, 0.0],
                [0.708, 1.415, 1.89, 0.0],
                [0.423, 0.862, 1.15, 0.0],
                [0.1087, 0.2174, 0.2900, 0.2900],
                [0.0348, 0.0696, 0.0925, 0.4090],
                [0.0313, 0.0625, 0.0830, 0.3900],
                [0.0299, 0.0597, 0.0795, 0.3320],
                [0.0209, 0.0417, 0.0556, 0.2450],
                [0.0159, 0.0318, 0.0424, 0.2650]]))

# Thome et al. is used, which uses spectral irradiance values from MODTRAN
# Ordered b1, b2, b3N, b4, b5...b9
irradiance = [1848, 1549, 1114, 225.4, 86.63, 81.85, 74.85, 66.49, 59.85]


def binmask(arr, bit):
    """ Return boolean array indicating which elements as binary have a 1 in
        a specified bit position. Input is Numpy array.
    """
    return arr & (1 << (bit - 1)) == (1 << (bit - 1))


def get_temporal_string(date):
    start_date_str = date.strftime("%Y-%m-%dT00:00:00Z")
    end_date_str = date.strftime("%Y-%m-%dT23:59:58Z")
    temporal_str = "%s,%s" % (start_date_str, end_date_str)
    return temporal_str


def reproject_spatial_extent_wkt(spatent, target_epsg):
    from osgeo import ogr, osr
    vector = open_vector(spatent.feature[0])

    # create and warp site geometry
    ogrgeom = ogr.CreateGeometryFromWkt(spatent.wkt)
    src = osr.SpatialReference(vector.Projection())
    target = osr.SpatialReference()
    target.ImportFromEPSG(target_epsg)
    transform = osr.CoordinateTransformation(src, target)
    ogrgeom.Transform(transform)

    trans_wkt = ogrgeom.ExportToWkt()
    return trans_wkt


def get_spatial_extent_projection(spatent):
    vector = open_vector(spatent.feature[0])
    return osr.SpatialReference(vector.Projection())


class asterRepository(Repository):
    name = 'Aster'
    description = ('Advanced Spaceborne Thermal Emission and Reflection '
                   'Radiometer (ASTER)')

    # NASA assets require special authentication
    _manager_url = "https://urs.earthdata.nasa.gov"

    @classmethod
    def feature2tile(cls, feature):
        """ convert tile field attributes to tile identifier """
        return feature.GetFieldAsString("name")

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

        # Get only the required driver
        layer.SetAttributeFilter("driver = '{}'".format(cls.name.lower()))

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


class asterAsset(Asset):
    Repository = asterRepository

    _sensors = {
        'L1T': {"description": "L1T Sensor"},
    }

    _assets = {
        'L1T': {
            'pattern': 'AST_L1T_\d{17}_\d{14}_\d+\.hdf',
            'url': 'https://e4ftl01.cr.usgs.gov/ASTER_L1T/ASTT/AST_L1T.003/',
        }
    }

    # Should this be specified on a per asset basis? (in which case retrieve from asset)
    _defaultresolution = [926.625433138333392, 926.625433139166944]

    def __init__(self, filename):
        """ Inspect a single file and get some metadata """
        super(asterAsset, self).__init__(filename)

        bname = os.path.basename(filename)
        parts = bname.split('_')

        self.asset = parts[1]

        year = parts[2][7:11]
        month = parts[2][3:5]
        dom = parts[2][5:7]
        self.date = datetime.datetime.strptime(year + month + dom, "%Y%m%d")
        self.tile = os.path.splitext(bname)[0]

    @classmethod
    def get_url(cls, asset, date, tilename):
        year = date.year
        month = str(date.month).zfill(2)
        day = str(date.day).zfill(2)
        url = "%s%d.%s.%s/%s.hdf" % (
                cls._assets[asset]['url'], year, month, day, tilename
        )
        return url

    @classmethod
    def query_service(cls, asset, feature, date):
        """Find out from the aster servers what assets are available.

        Uses the given (asset, feature, date) tuple as a search key, and
        returns a list of dicts:  {'basename': base-filename, 'url': url}

        Assuming "feature" is WKT (for now)
        Date is in format YYYY-MM-DD
        """
        mainurl = 'http://e4ftl01.cr.usgs.gov/'
        # Date format is yyyy-MM-ddTHH:mm:ssZ
        date = datetime.datetime.strptime(date, "%Y-%m-%d")
        temporal_str = get_temporal_string(date)

        # Authenticate with Earthdata login
        # TODO: Don't use this file
        cmr = CMR('cmr.cfg')

        # Create geometry search string
        shape = shapely.wkt.loads(feature)
        poly_string = ""
        point_array = np.asarray(shape.exterior.coords)

        # Check if shape is counter-clockwise
        if point_array[0][0] < point_array[1][0]:
            point_array = point_array[::-1]

        for pair in point_array:
            poly_string += "%f,%f," % (pair[0], pair[1])
        poly_string = poly_string[:-1]

        # MODIS warning, might still be relevant
        if datetime.datetime.today().date().weekday() == 2:
            err_msg = ("Error downloading on a Wednesday;"
                       " possible planned ASTER provider downtime: " + mainurl)
        else:
            err_msg = "Error downloading: "

        # Use cmr to get results with given geometry and time
        with utils.error_handler(err_msg):
            # TODO: Make this work for other assets
            results = cmr.searchGranule(
                limit=1000,
                short_name="AST_L1T",
                polygon=poly_string,
                day_night_flag="day",
                temporal=temporal_str
            )
            if len(results) == 0:
                return []
        available = []

        for item in results:  # Should be 1
            # Extract URL and file name from search results
            basename = item['Granule']['DataGranule']['ProducerGranuleId']
            url = ""
            for url_dict in item['Granule']['OnlineAccessURLs']['OnlineAccessURL']:
                if url_dict['MimeType'] == 'application/x-hdfeos':
                    url = url_dict['URL']
                    break
            available.append({'basename': basename, 'url': url})

        if len(available) == 0:
            err_msg = 'Unable to find remote match at {}'.format(mainurl)
            utils.verbose_out(err_msg, 4)

        return available

    def get_geometry_name(self):
        return os.path.splitext(os.path.basename(self.filename))[0]

    def get_geometry(self):
        """Get the geometry of the asset

        Uses the query service to get the geometry of an asset
        """

        bname = os.path.basename(self.filename)
        url = self.get_url(self.asset, self.date, bname) + ".xml"

        xmlfile = self.Repository.managed_request(url, verbosity=2)
        data = xmlfile.read()
        xmlfile.close()

        tree = ET.fromstring(data)
        points = tree.findall(
            'GranuleURMetaData/SpatialDomainContainer/HorizontalSpatialDomainContainer/GPolygon/Boundary/Point'
        )

        # Put in counter-clockwise order
        points.reverse()

        wkt = "POLYGON (("
        for point in points:
            wkt += "%s %s," % (point[0].text, point[1].text)

        # Repeat for the last point
        point = points[0]
        wkt += "%s %s))" % (point[0].text, point[1].text)
        return wkt

    @classmethod
    def fetch(cls, asset, tile, date):
        retrieved_filenames = []
        year = date.year
        month = str(date.month).zfill(2)
        day = str(date.day).zfill(2)
        url = "%s%d.%s.%s/%s.hdf" % (
                cls._assets[asset]['url'], year, month, day, tile
        )
        outpath = os.path.join(cls.Repository.path('stage'), tile + ".hdf")

        with utils.error_handler(
                "Asset fetch error ({})".format(asset), continuable=True):
            response = cls.Repository.managed_request(url)
            if response is None:
                return retrieved_filenames  # give up now as the rest
            with open(outpath, 'wb') as fd:
                fd.write(response.read())

            utils.verbose_out('Retrieved %s' % tile, 2)
            retrieved_filenames.append(outpath)

        return retrieved_filenames


class asterData(Data):
    """ A tile of data (all assets and products) """
    name = 'Aster'
    version = '1.0.0'
    Asset = asterAsset
    _productgroups = {
    }
    _products = {
        'ref': {
            'description': 'TOA reflectance',
            'assets': ['L1T'],
            'sensor': 'L1T',
            'bands': [{'name': 'temp', 'units': 'none'}],
            'category': 'Temporary Stuff',
            'startdate': datetime.date(2000, 3, 4),
            'latency': 1,
        }
    }

    def asset_check(self, prod_type):
        """Is an asset available for the current scene and product?

        Returns the last found asset, or else None, its version, the
        complete lists of missing and available assets, and lastly, an array
        of pseudo-filepath strings suitable for consumption by gdal/gippy.
        """
        # return values
        asset = None
        version = None
        missingassets = []
        availassets = []
        allsds = []

        for asset in self._products[prod_type]['assets']:
            # many asset types won't be found for the current scene
            if asset not in self.assets:
                missingassets.append(asset)
                continue
            try:
                sds = self.assets[asset].datafiles()
            except Exception as e:
                utils.report_error(e, 'Error reading datafiles for ' + asset)
                missingassets.append(asset)
            else:
                availassets.append(asset)
                allsds.extend(sds)
                #version = int(re.findall('M.*\.(\d{3})\.\d{13}\.hdf', sds[0])[0])
                version = 1  # What is this?

        return asset, version, missingassets, availassets, allsds

    def ParseAndAddFiles(self, filenames=None):
        """Parse and Add filenames to existing filenames.

        If no filenames are provided, a list from find_files() is used
        instead."""
        if filenames is None:
            filenames = self.find_files()  # find *product* files actually
        datedir = self.Repository._datedir
        for f in filenames:
            bname = basename(f)
            parts = bname.split('_')
            if len(parts) < 3 or len(parts) > 8:
                # Skip this file
                VerboseOut('Unrecognizable file: %s' % f, 3)
                continue
            with utils.error_handler('Unrecognizable file ' + f, continuable=True):
                # only admit product files matching a single date
                if self.date is None:
                    # First time through
                    print("Parts[5]", parts[5])
                    self.date = datetime.datetime.strptime(parts[5], datedir).date()
                    print(self.date)
                else:
                    date = datetime.datetime.strptime(parts[5], datedir).date()
                    if date != self.date:
                        raise Exception('Mismatched dates: %s' % ' '.join(filenames))
                sensor = parts[1]
                product = parts[7]
                self.AddFile(sensor, product, f, add_to_db=False)

    @Data.proc_temp_dir_manager
    def process(self, *args, **kwargs):
        """Produce requested products."""
        products = super(asterData, self).process(*args, **kwargs)
        if len(products) == 0:
            return
        # These are the bands used by gippy
        desired_sds_keys = [
            'ImageData2',
            'ImageData3N',
        ]

        # example products.requested:
        # {'temp8tn': ['temp8tn'], 'clouds': ['clouds'], . . . }
        # key is only used once far below, and val is only used for val[0].
        for key, val in products.requested.items():
            prod_type = val[0]
            start = datetime.datetime.now()
            asset, version, missingassets, availassets, allsds = \
                self.asset_check(prod_type)

            if not availassets:
                # some products aren't available for every day but this is trying every day
                VerboseOut('There are no available assets (%s) on %s for tile %s'
                           % (str(missingassets), str(self.date), str(self.id), ), 5)
                continue
            meta = self.meta_dict()
            meta['AVAILABLE_ASSETS'] = ' '.join(availassets)

            sensor = self._products[prod_type]['sensor']
            fname = self.temp_product_filename(sensor, prod_type)  # moved to archive at end of loop

            # Get the sds' that gippy cares about
            desired_sds = [s for s in allsds if s.split(':')[-1] in desired_sds_keys]

            # Make ref
            asset_fn = desired_sds[0].split('"')[1]
            dn_image = gdal.Open(asset_fn)
            aster_sds = dn_image.GetSubDatasets()
            dn_meta = dn_image.GetMetadata()

            # Correct for meta bug in GDAL 1
            if (int(gdal.VersionInfo()) < 2000000):
                meta_list = dn_image.GetMetadata_List()
                dn_meta.update(dict([i.replace('=', '.').split(',') for i in meta_list if i.startswith('GAIN')]))

            day = self.date.timetuple()
            doy = day.tm_yday
            # Calculate Earth-Sun Distance
            esd = 1.0 - 0.01672 * np.cos(np.radians(0.9856 * (doy - 4)))

            # Need SZA--calculate by grabbing solar elevation info
            sza = [np.float(x) for x in dn_meta['SOLARDIRECTION'].split(', ')][1]
            # Query gain data for each  band, needed for UCC
            # Getting meta from first sds because of gdal v1 bug
            gain_02 = dn_meta['GAIN.2'].strip()
            gain_03n = dn_meta['GAIN.3'].strip()

            # Define UL, LR, UTM zone
            ul = [np.float(x) for x in dn_meta['UPPERLEFTM'].split(', ')]
            lr = [np.float(x) for x in dn_meta['LOWERRIGHTM'].split(', ')]
            utm = np.int(dn_meta['UTMZONENUMBER'])
            n_s = np.float(dn_meta['NORTHBOUNDINGCOORDINATE'])

            # Create UTM zone code numbers
            utm_n = [i+32600 for i in range(60)]
            utm_s = [i+32700 for i in range(60)]

            # Define UTM zone based on North or South
            # Unused?
            if n_s < 0:
                utm_zone = utm_s[utm]
            else:
                utm_zone = utm_n[utm]

            del utm_n, utm_s, utm, dn_meta

            # Loop through all ASTER L1T SDS (bands)
            for i in range(len(aster_sds)):

                # Maintain original dataset name
                gname = str(aster_sds[i])
                aster_sd = gname.split(',')[0]

                vnir = re.search("(VNIR.*)", aster_sd)
                swir = re.search("(SWIR.*)", aster_sd)
                if vnir or swir:
                    # Generate output name for tif
                    aster_sd2 = aster_sd.split('(')[1]
                    aster_sd3 = aster_sd2[1:-1]
                    band = aster_sd3.split(':')[-1]

                    # Open SDS and create array
                    band_ds = gdal.Open(aster_sd3, gdal.GA_ReadOnly)
                    sds = band_ds.ReadAsArray().astype(np.uint16)

                    del aster_sd, aster_sd2, aster_sd3

                    # Define extent and provide offset for UTM South zones
                    if n_s < 0:
                        ul_y = ul[0] + 10000000
                        ul_x = ul[1]

                        lr_y = lr[0] + 10000000
                        lr_x = lr[1]

                    # Define extent for UTM North zones
                    else:
                        ul_y = ul[0]
                        ul_x = ul[1]

                        lr_y = lr[0]
                        lr_x = lr[1]

                    # Query raster dimensions and calculate raster x and y resolution
                    ncol, nrow = sds.shape
                    y_res = -1 * round((max(ul_y, lr_y)-min(ul_y, lr_y))/ncol)
                    x_res = round((max(ul_x, lr_x)-min(ul_x, lr_x))/nrow)

                    # Define UL x and y coordinates based on spatial resolution
                    ul_yy = ul_y - (y_res/2)
                    ul_xx = ul_x - (x_res/2)

                    if band == 'ImageData2':
                        bn = -1 + 2
                        # Query for gain specified in file metadata (by band)
                        if gain_02 == 'HGH':
                            ucc1 = ucc[bn, 0]
                        elif gain_02 == 'NOR':
                            ucc1 = ucc[bn, 1]
                        else:
                            ucc1 = ucc[bn, 2]

                    if band == 'ImageData3N':
                        bn = -1 + 3
                        # Query for gain specified in file metadata (by band)
                        if gain_03n == 'HGH':
                            ucc1 = ucc[bn, 0]
                        elif gain_03n == 'NOR':
                            ucc1 = ucc[bn, 1]
                        else:
                            ucc1 = ucc[bn, 2]

                    #Set irradiance value for specific band
                    irradiance1 = irradiance[bn]

                    # Convert from DN to Radiance
                    rad = (sds-1.)*ucc1

                    # Convert from Radiance to TOA Reflectance
                    ref = (np.pi * rad * (esd * esd)) / (irradiance1 * np.sin(np.pi * sza / 180.))

                    return
                    # Make NDVI
                    if prod_type == "ndvi":
                        # Do stuff here
                        pass

            # add product to inventory
            archive_fp = self.archive_temp_path(fname)
            self.AddFile(sensor, key, archive_fp)
            del dn_image  # to cover for GDAL's internal problems
            utils.verbose_out(' -> {}: processed in {}'.format(
                os.path.basename(fname), datetime.datetime.now() - start), level=1)

    @classmethod
    def findTiles(cls, asset, spatent, textent):
        return

    @classmethod
    def query_service(cls, products, spatent, textent, update=False, force=False, grouped=False):
        """
        Returns a list (or dict) of asset files that are available for
        download, given the arguments provided.
        These constraints include specific products, tiles, and temporal
        extent.
        Additionally, the return value is either grouped into a dict mapping
        (prod, tile, date) --> url
        or simply a list of URLs, based on the 'grouped' parameter.
        """
        if grouped:
            response = {}
        else:
            response = []
        tiles = {}
        for p in products:
            assets = cls.products2assets([p])

            # Add stuff here?
            for a in assets:
                asset_dates = cls.Asset.dates(a, None, textent.datebounds, textent.daybounds)
                wkt = reproject_spatial_extent_wkt(spatent, 4326)
                geom_shape = loads(wkt)

                for d in asset_dates:
                    results = cls.Asset.query_service(a, wkt, d.strftime("%F"))

                    geom_shape = loads(wkt)

                    # Add resultst to geometry table
                    for r in results:
                        aobj = cls.Asset(r['basename'])
                        aobj_geom = aobj.get_geometry()
                        tile_name = aobj.get_geometry_name()
                        dbinv.update_or_add_geometry(
                            cls.name.lower(),
                            aobj_geom,
                            tile_name
                        )

                        # Calculate coverage
                        tile_shape = loads(aobj_geom)
                        area = geom_shape.intersection(tile_shape).area
                        tile_coverage = (area / geom_shape.area, area / tile_shape.area)
                        if (tile_coverage[0] < (spatent.pcov / 100.0)) or (tile_coverage[1] < (spatent.ptile / 100.0)):
                            continue
                        tiles[tile_name] = tile_coverage
                        # Add to spatent
                        # if we don't have it already, or if 'update' flag
                        local_assets = cls.Asset.discover(tile_name, d, a)
                        if force or len(local_assets) == 0 or update:
                            date_str = d.strftime("%F")
                            msg_prefix = (
                                'query_service for {}, {}, {}'
                                .format(a, tile_name, date_str)
                            )

                            with utils.error_handler(msg_prefix, continuable=False):
                                #resp = cls.Asset.query_service(a, t, d)
                                #if len(resp) == 0:
                                #    continue
                                #elif len(resp) > 1:
                                #    raise Exception('should only be one asset')
                                aobj = cls.Asset(tile_name)

                                if force or len(local_assets) == 0 or (
                                     len(local_assets) == 1 and
                                     local_assets[0].updated(aobj)
                                    ):
                                    rec = {
                                        'product': p,
                                        'sensor': aobj.sensor,
                                        'tile': tile_name,
                                        'asset': a,
                                        'date': d
                                    }

                                    # Update remote assets
                                    dbinv.update_or_add_asset(
                                        cls.name.lower(),
                                        a,
                                        aobj.get_geometry_name(),
                                        d,
                                        aobj.sensor,
                                        aobj.get_geometry_name(),
                                        "remote"
                                    )

                                    # useful to datahandler to have this
                                    # grouped by (p,t,d) there is a fair bit of
                                    # duplicated info this way, but oh well
                                    if grouped:
                                        if (p, tile_name, d) in response:
                                            response[(p, tile_name, d)].append(rec)
                                        else:
                                            response[(p, tile_name, d)] = [rec]
                                    else:
                                        response.append(rec)
            spatent.set_tiles(tiles)
            return response

    @classmethod
    def fetch(cls, products, spatent, textent, update=False):
        available_assets = cls.query_service(
            products, spatent, textent, update
        )
        fetched = []
        for asset_info in available_assets:
            asset = asset_info['asset']
            tile = asset_info['tile']
            date = asset_info['date']
            msg_prefix = (
                'Problem fetching asset for {}, {}, {}'
                .format(asset, tile, str(date))
            )
            with utils.error_handler(msg_prefix, continuable=True):
                filenames = cls.Asset.fetch(asset, tile, date)
                # fetched may contain both fetched things and unfetchable things
                if len(filenames) == 1:
                    fetched.append((asset, tile, date))

        return fetched
