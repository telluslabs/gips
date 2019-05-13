#!/usr/bin/env python
################################################################################
#    GIPS: Geospatial Image Processing System
#
#    Copyright (C) 2017 Applied Geosolutions
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

from __future__ import print_function

import math
import os
import shutil
import sys
import datetime
import shlex
import re
import subprocess
import json
import tempfile
import zipfile
import copy
import glob
from itertools import izip_longest
from xml.etree import ElementTree
import StringIO

from backports.functools_lru_cache import lru_cache

import numpy
import pyproj
import requests
from requests.auth import HTTPBasicAuth
from shapely.wkt import loads as wkt_loads
import geopandas as gpd

import gippy
import gippy.algorithms

from gips.data.core import Repository, Asset, Data
import gips.data.core
from gips import utils
from gips.data.sentinel1.tiles import make_tilegrid



from pdb import set_trace


_asset_types = ('L1',)

class sentinel1Repository(Repository):
    name = 'Sentinel1'
    description = 'Data from the Sentinel 1 satellite(s) from the ESA'

    _tile_attribute = 'Name'

    default_settings = {
        'source': 'esa',
        'extract': False,
    }

    # the default tile ID
    _tile_attribute = "tileid"

    @classmethod
    def validate_setting(cls, key, value):
        if key == 'source' and value not in ('esa', 'gs'):
            raise ValueError("Sentinel-1's 'source' setting is '{}',"
                    " but valid values are 'esa' or 'gs'".format(value))
        return value

    @classmethod
    def vector2tiles(cls, vector, *args, **kwargs):

        # make a tilegrid on the fly and get the list of tiles

        # tilefile is called /archive/sentinel1/stage/tile_{}_{}.shp

        tileshpfile, tilelist = make_tilegrid(vector.Filename(), cls._tile_attribute)

        cls._tilefile_name = tileshpfile

        print('cls._tile_name', tileshpfile)

        return {k: (1,1) for k in tilelist}


    # @classmethod
    # def tile_lat_lon(cls, tileid):
    #     """Returns the coordinates of the given tile ID.

    #     Uses the reference tile vectors provided with the driver.
    #     Returns (x0, x1, y0, y1), which is
    #     (west lon, east lon, south lat, north lat) in degrees.
    #     """
    #     e = utils.open_vector(cls.get_setting('tiles'), cls._tile_attribute)[tileid].Extent()
    #     return e.x0(), e.x1(), e.y0(), e.y1()



class sentinel1Asset(Asset):
    Repository = sentinel1Repository

    _sensors = {
        'S1': {
            'description': 'Sentinel-1, Satellite',

            'band-strings':
                ['01', '02'],

            'polarization':
                ('VV',  'VH'),

            # band location in GHz
            'bandlocs':
                ['5.405', '5.405'],

            'spatial-resolutions':
                [20, 20],
        },
    }

    # _asset_fn_pat_base = '^.*S2._.*MSIL1C_.*.{8}T.{6}_.*R..._.*'

    # S1A_IW_GRDH_1SDV_20180409T002028_20180409T002053_021383_024CFC_A7BE.tif

    _raw_pat_base = "(?P<sensor>S1[AB])_IW_GRDH_1SDV_(?P<pyear>\d{4})(?P<pmon>\d{2})(?P<pday>\d{2})T\w{6}_\w{15}_\w{6}_\w{6}_\w{4}\.tif"

    # _asset_pat_base = "(?P<sensor>S1[AB])_IW_GRDH_1SDV_(?P<pyear>\d{4})(?P<pmon>\d{2})(?P<pday>\d{2})_(?P<ptile>\w{3}_\w{3]}).tif"

    _asset_pat_base = 'S1_IW_GRDH_(?P<year>\d{4})(?P<mon>\d{2})(?P<day>\d{2})_(?P<tile>\w{3}_\w{3}).tif'

    _start_date = datetime.date(2015, 1, 1)

    _assets = {
        'L1': {
            'source': 'esa',
            # 'pattern' is used for searching the repository of locally-managed assets
            'pattern': _asset_pat_base,
            'startdate': _start_date,
            'latency': 3,
        },
    }


    # # default resultant resolution for resampling during to Data().copy()
    # _defaultresolution = (10, 10)

    def __init__(self, filename):
        """Inspect a single file and set some metadata.
        """
        super(sentinel1Asset, self).__init__(filename)

        self.basename = os.path.basename(filename)

        match = re.match(self._asset_pat_base, self.basename)

        self.asset = "L1"
        self.sensor = "S1"

        self.tile = match.group('tile')
        self.date = datetime.date(*[int(i) for i in match.group('year', 'mon', 'day')])
        self._version = int(''.join(
            match.group('year', 'mon', 'day')
        ))
        self.meta = {} # for caching asset metadata values
        self.tile_meta = None # tile metadata; dict was not good for this


    @classmethod
    def query_gs(cls, tile, date):
        raise Exeption('query_gs not implemented')

    @classmethod
    def query_esa(cls, tile, date):
        import gips.data.sentinel1.sentinel_api.sentinel_api as api

        print('query', tile)


        # use username and password for ESA DATA Hub authentication
        username = cls.get_setting('username')
        password = cls.get_setting('password')

        # All historic Sentinel-1 scenes: https://scihub.copernicus.eu/dhus/
        downloader = api.SentinelDownloader(username, password,
            api_url='https://scihub.copernicus.eu/apihub/')


        # get the scene name and use it for caching


        # load geometries from shapefile
        gdf = gpd.read_file(cls.Repository._tilefile_name)
        gdf = gdf[gdf['tileid']==tile]

        # IMPORTANT: this is the name of the tile boundaru
        outfile = os.path.join(cls.Repository.path(), 'stage/tile_{}.shp'.format(tile))
        gdf.to_file(outfile)


        downloader.load_sites(outfile)


        datestr = date.date().isoformat()

        # search for scenes with some restrictions (e.g., minimum overlap 1%)
        downloader.search('S1A*', min_overlap=0.01, start_date=datestr, end_date=datestr,
                  date_type='beginPosition', productType='GRD', sensoroperationalmode='IW')

        # # add another search query (e.g., for Sentinel-1B); both search results will be merged
        downloader.search('S1B*', min_overlap=0.01, start_date=datestr, end_date=datestr,
                  date_type='beginPosition', productType='GRD', sensoroperationalmode='IW')

        if len(downloader.get_scenes()) == 0:
            print('returning None')
            return None
        else:
            basename = 'S1_IW_GRDH_{}_{}.tif'.format(date.date().strftime('%Y%m%d'), tile)
            print('returning', basename)
            return {'basename': basename, 'downloader': downloader, 'url': ''}


    @classmethod
    @lru_cache(maxsize=100) # cache size chosen arbitrarily
    def query_service(cls, asset, tile, date, pclouds=100, **ignored):
        """as superclass, but bifurcate between google and ESA sources."""
        if not cls.available(asset, date):
            return None
        source = cls.get_setting('source')
        if cls._assets[asset]['source'] != source:
            return None
        rv = {'esa': cls.query_esa,
              'gs':  cls.query_gs, }[source](tile, date)
        utils.verbose_out(
            'queried ATD {} {} {}, found '.format(asset, tile, date)
            + ('nothing' if rv is None else rv['basename']), 5)
        if rv is None:
            return None
        rv['a_type'] = asset
        return rv


    @classmethod
    def download(cls, a_type, download_fp, downloader, **kwargs):
        """Download from the configured source for the asset type."""

        from shapely.wkt import loads

        downloaddir, assetfile = os.path.split(download_fp)

        downloader.set_download_dir(downloaddir)

        print(downloaddir)

        # actually retrieve data

        downloader.download_all()

        # cache the downloaded zip


        # geometries are just the boundaries in the shapefile
        # set_geometries could be used
        # geoms = [loads(g) for g in downloader.get_geometries()]
        # gdf = gpd.GeoDataFrame({'geometry':geoms}, geometry='geometry', crs={'epsg:4326'})
        # gdf.to_file('/archive/sentinel1/stage/scene_boundary.shp')

        # the downloaded data is not the asset file

        graph_xml_path = "/gips/gips/data/sentinel1/Basic2Preprocess.xml"


        stagedir = "/archive/sentinel1/stage"


        for scene in downloader.get_scenes():
            name = scene['identifier']
            sourcefile = os.path.join(stagedir, name + '.zip')
            targetfile = os.path.join(stagedir, name + '.tif')

            cmd = "/usr/bin/gpt {} -e -SsourceProduct={} -PtargetProduct={} -Dsnap.dataio.bigtiff.compression.type=LZW".format(
                graph_xml_path, sourcefile, targetfile)
            print(cmd)
            args = shlex.split(cmd)
            p = subprocess.Popen(args)
            p.communicate()
            if p.returncode != 0:
                raise IOError("Expected exit status 0, got {}".format(
                    p.returncode))

        # cache the processed downloaded tif

        set_trace()

        # need the asset file name

        # clip and merge the results and save as an asset

        return True


class sentinel1Data(Data):
    name = 'Sentinel1'
    version = '0.0.1'
    Asset = sentinel1Asset
    inline_archive = True

    # TODO: is this the correct order?
    _productgroups = {'sigma0': ['sigma0']}


    _products = {
        'sigma0': {
            'description': 'Backscatter',
            'assets': _asset_types,
            'bands': ['vv', 'vh']
        },
    }

    @Data.proc_temp_dir_manager
    def process(self, products=None, overwrite=False, **kwargs):
        """Produce data products and save them to files."""

        pass





