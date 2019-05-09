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

import gippy
import gippy.algorithms

from gips.data.core import Repository, Asset, Data
import gips.data.core
from gips import utils


from pdb import set_trace


_asset_types = ('S1A', 'S1B')

class sentinel1Repository(Repository):
    name = 'Sentinel1'
    description = 'Data from the Sentinel 1 satellite(s) from the ESA'

    _tile_attribute = 'Name'

    default_settings = {
        'source': 'esa',
        'asset-preference': _asset_types,
        'extract': False,
    }

    @classmethod
    def validate_setting(cls, key, value):
        if key == 'source' and value not in ('esa', 'gs'):
            raise ValueError("Sentinel-2's 'source' setting is '{}',"
                    " but valid values are 'esa' or 'gs'".format(value))
        elif key == 'asset-preference':
            warts = set(value) - set(_asset_types)
            if warts:
                raise ValueError("Valid 'asset-preferences' for Sentinel-1"
                        " are {}; invalid values found:  {}".format(
                    _asset_types, warts))
        return value

    # @classmethod
    # def tile_lat_lon(cls, tileid):
    #     """Returns the coordinates of the given tile ID.

    #     Uses the reference tile vectors provided with the driver.
    #     Returns (x0, x1, y0, y1), which is
    #     (west lon, east lon, south lat, north lat) in degrees.
    #     """
    #     e = utils.open_vector(cls.get_setting('tiles'), cls._tile_attribute)[tileid].Extent()
    #     return e.x0(), e.x1(), e.y0(), e.y1()



class sentinel1Asset():
    Repository = sentinel1Repository

    _sensors = {
        'S1A': {
            'description': 'Sentinel-1, Satellite A',

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
    _sensors['S1B'] = copy.deepcopy(_sensors['S1A'])
    _sensors['S1B']['description'] = 'Sentinel-1, Satellite B'

    # _asset_fn_pat_base = '^.*S2._.*MSIL1C_.*.{8}T.{6}_.*R..._.*'

    # S1A_IW_GRDH_1SDV_20180409T002028_20180409T002053_021383_024CFC_A7BE.tif

    _raw_pat_base = "(?P<sensor>S1[AB])_IW_GRDH_1SDV_(?P<pyear>\d{4})(?P<pmon>\d{2})(?P<pday>\d{2})T\w{6}_\w{15}_\w{6}_\w{6}_\w{4}\.tif"

    _asset_pat_base = "(?P<sensor>S1[AB])_IW_GRDH_1SDV_(?P<pyear>\d{4})(?P<pmon>\d{2})(?P<pday>\d{2})_(?P<ptile>\w{3}_\w{3]}).tif"

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

        File naming convention:
        https://sentinels.copernicus.eu/web/sentinel/user-guides/sentinel-2-msi/naming-convention
        """
        super(sentinel1Asset, self).__init__(filename)

        match = re.match(self._asset_pat_base, self.basename)

        self.basename = os.path.basename(filename)

        self.asset = "L1"
        self.sensor = match.group('sensor')
        self.tile = match.group('tile')
        self.date = datetime.date(*[int(i) for i in match.group('year', 'mon', 'day')])
        # self.time = datetime.time(*[int(i) for i in match.group('hour', 'min', 'sec')])
        self._version = int(''.join(
            match.group('pyear', 'pmon', 'pday')
        ))
        self.meta = {} # for caching asset metadata values
        self.tile_meta = None # tile metadata; dict was not good for this

    @classmethod
    def query(cls, tile, date):

        set_trace()







