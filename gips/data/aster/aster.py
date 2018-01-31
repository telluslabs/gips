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

import os
import sys
import re
import datetime
import shapely
import urllib
import urllib2

import math
import numpy as np
import requests

import xml.etree.ElementTree as ET

import gippy
from gippy.algorithms import Indices
from gips.data.core import Repository, Asset, Data
from gips.utils import VerboseOut, settings, open_vector
from gips import utils

from shapely.wkt import loads

from pyCMR.pyCMR import CMR


def binmask(arr, bit):
    """ Return boolean array indicating which elements as binary have a 1 in
        a specified bit position. Input is Numpy array.
    """
    return arr & (1 << (bit - 1)) == (1 << (bit - 1))


def get_temporal_string(date):
    start_date_str = date.strftime("%Y-%m-%dT00:00:00Z")
    end_date_str =  date.strftime("%Y-%m-%dT23:59:58Z")
    temporal_str = "%s,%s" % (start_date_str, end_date_str)
    return temporal_str


def reproject_spatial_extent_wkt(spatent, target_epsg):
    from osgeo import ogr, osr
    vector = open_vector(spatent.feature[0])
    shp = ogr.Open(vector.Filename())
    if vector.LayerName() == '':
        layer = shp.GetLayer(0)
    else:
        layer = shp.GetLayer(vector.LayerName())
    # create and warp site geometry
    ogrgeom = ogr.CreateGeometryFromWkt(spatent.wkt)
    src = osr.SpatialReference(vector.Projection())
    target = osr.SpatialReference()
    target.ImportFromEPSG(target_epsg)
    transform = osr.CoordinateTransformation(src, target)
    ogrgeom.Transform(transform)

    trans_wkt = ogrgeom.ExportToWkt()
    return trans_wkt


class asterRepository(Repository):
    name = 'Aster'
    description = ('Advanced Spaceborne Thermal Emission and Reflection '
                    'Radiometer (ASTER)')

    # NASA assets require special authentication
    _manager_url = "https://urs.earthdata.nasa.gov"

    @classmethod
    def feature2tile(cls, feature):
        """ convert tile field attributes to tile identifier """
        print("feature2tile is happening")
        fldindex_h = feature.GetFieldIndex("h")
        fldindex_v = feature.GetFieldIndex("v")
        h = str(int(feature.GetField(fldindex_h))).zfill(2)
        v = str(int(feature.GetField(fldindex_v))).zfill(2)
        return "h%sv%s" % (h, v)

    @classmethod
    def vector2tiles(cls, vector, pcov=0.0, ptile=0.0, tilelist=None):
        """ Return matching tiles and coverage % for provided vector """
        from osgeo import ogr, osr

        # open tiles vector
        print("Tiles setting:", cls.get_setting('tiles'))
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


class asterAsset(Asset):
    Repository = asterRepository

    _sensors = {
    }

    _assets = {
        'L1T': {
            'pattern': '\d{4}\.\d{2}\.\d{2}/.{47}.hdf',
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

        year = parts[2][7:10]
        month = parts[2][3:5]
        dom = parts[2][5:7]
        self.date = datetime.datetime.strptime(year + month + dom, "%Y%m%d")


    @classmethod
    def query_service(cls, asset, feature, date):
        """Find out from the aster servers what assets are available.

        Uses the given (asset, feature, date) tuple as a search key, and
        returns a list of dicts:  {'basename': base-filename, 'url': url}

        Assuming "feature" is WKT (for now)
        Date is in format YYYY-MM-DD
        """
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
        print("Pointarr", point_array)

        # Check if shape is counter-clockwise
        if point_array[0][0] < point_array[1][0]:
            point_array = point_array[::-1]
            print("Reversed", point_array)

        for pair in point_array:
            poly_string += "%f,%f," % (pair[0], pair[1])
        poly_string = poly_string[:-1]

        # MODIS warning, might still be relevant
        if datetime.datetime.today().date().weekday() == 2:
            err_msg = ("Error downloading on a Wednesday;"
                       " possible planned MODIS provider downtime: " + mainurl)
        else:
            err_msg = "Error downloading: "

        # Use cmr to get results with given geometry and time
        with utils.error_handler(err_msg):
            # TODO: Make this work for other assets
            results = cmr.searchGranule(
                limit=1000,
                short_name="AST_L1T",
                polygon=poly_string,
                temporal=temporal_str
            )
            if len(results) == 0:
                return []
        available = []

        mainurl = 'http://e4ftl01.cr.usgs.gov/'
        for item in results: # Should be 1
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

        #TODO: Retrieve geometries

        return available


    def get_geometry(self):
        """Get the geometry of the asset

        Uses the query service to get the geometry of an asset
        """

        bname = os.path.basename(self.filename)
        year = self.date.year
        month = str(self.date.month).zfill(2)
        day = str(self.date.day).zfill(2)
        url = "%s%d.%s.%s/%s.xml" % (
                self._assets[self.asset]['url'], year, month, day, bname
        )

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
        available_assets = cls.query_service(asset, tile, date)
        retrieved_filenames = []
        # TODO does aster ever have more than one asset per (a,t,d)?  If not, unloop this method.
        for asset_info in available_assets:
            basename = asset_info['basename']
            url = asset_info['url']
            outpath = os.path.join(cls.Repository.path('stage'), basename)

            with utils.error_handler(
                    "Asset fetch error ({})".format(asset_info), continuable=True):
                response = cls.Repository.managed_request(url)
                if response is None:
                    return retrieved_filenames # give up now as the rest
                with open(outpath, 'wb') as fd:
                    fd.write(response.read())

                utils.verbose_out('Retrieved %s' % basename, 2)
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
        'tempProduct': {
            'description': 'A placeholder product',
            'assets': ['L1T'],
            'bands': [{'name': 'temp', 'units': 'none' }],
            'category': 'Temporary Stuff',
            'startdate': datetime.date(2000,1,1),
            'latency': 1,
        }
    }

    @Data.proc_temp_dir_manager
    def process(self, *args, **kwargs):
        """Produce requested products."""
        products = super(asterData, self).process(*args, **kwargs)
        if len(products) == 0:
            return

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
            response  = []
        for p in products:
            assets = cls.products2assets([p])

            # Add stuff here?
            for a in assets:
                asset_date = cls.Asset.dates(a, None, textent.datebounds, textent.daybounds)
                wkt = reproject_spatial_extent_wkt(spatent, 4326)
                results = cls.Asset.query_service(a, wkt, asset_date[0].strftime("%F"))
                print(results)

                # Calculate coverage

                # Add to spatent

                print("Asset_dates:", asset_date)
                for t in spatent.tiles:
                    #asset_dates = cls.Asset.dates(a, t, textent.datebounds, textent.daybounds)
                    for d in asset_dates:
                        # if we don't have it already, or if 'update' flag
                        local_assets = cls.Asset.discover(t, d, a)
                        if force or len(local_assets) == 0 or update:
                            date_str = d.strftime("%F")
                            msg_prefix = (
                                'query_service for {}, {}, {}'
                                .format(a, t, date_str)
                            )
                            with utils.error_handler(msg_prefix, continuable=False):
                                resp = cls.Asset.query_service(a, t, d)
                                if len(resp) == 0:
                                    continue
                                elif len(resp) > 1:
                                    raise Exception('should only be one asset')
                                aobj = cls.Asset(resp[0]['basename'])

                                if (force or len(local_assets) == 0 or
                                    (len(local_assets) == 1 and
                                     local_assets[0].updated(aobj))
                                ):
                                    rec = {
                                        'product': p,
                                        'sensor': aobj.sensor,
                                        'tile': t,
                                        'asset': a,
                                        'date': d
                                    }

                                    ## Insert geometry into the database
                                    #dbinv.update_or_add_geometry(
                                    #    cls.name.lower(),
                                    #    aobj.get_geometry(),
                                    #    aobj.get_geometry_name()
                                    #)
                                    # Update remote assets
                                    update_or_add_asset(
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
                                        if (p,t,d) in response:
                                            response[(p,t,d)].append(rec)
                                        else:
                                            response[(p,t,d)] = [rec]
                                    else:
                                        response.append(rec)
            return response

    @classmethod
    def fetch(cls, products, spatent, textent, update=False):
        print("asterData.fetch", products, spatent, textent)
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

