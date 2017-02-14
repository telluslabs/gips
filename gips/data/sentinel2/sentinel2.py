#!/usr/bin/env python
################################################################################
#    GIPS: Geospatial Image Processing System
#
#    Copyright (C) 2017 Applied Geosolutions
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

#import os
import sys
#import re
import datetime
import shlex
import subprocess

#import urllib
#import urllib2

#import math
#import numpy as np
#import requests

#import gippy
#from gippy.algorithms import Indices
from gips.data.core import Repository, Asset, Data
from gips import utils

class sentinel2Repository(Repository):
    name = 'Sentinel-2'
    description = 'Data from the Sentinel 2 satellite(s) from the ESA'
    # when looking at the tiles shapefile, what's the key to fetch a feature's tile ID?
    _tile_attribute = 'Name'


class sentinel2Asset(Asset):
    Repository = sentinel2Repository

    _sensors = {
        'MSI': {'description': 'Multispectral Instrument'},
    }

    # example url:
    # https://scihub.copernicus.eu/dhus/search?q=filename:S2?_MSIL1C_20170202T??????_N????_R???_T19TCH_*.SAFE

    _assets = {
        'L1C': {
            #                      sense datetime              tile
            #                     (YYYYMMDDTHHMMSS)            (MGRS)
            'pattern': 'S2?_MSIL1C_????????T??????_N????_R???_T?????_*.SAFE',
            'url': 'https://scihub.copernicus.eu/dhus/search?q=filename:',
            'startdate': datetime.date(2016, 12, 06),
            'latency': 3 # TODO actually seems to be 3,7,3,7..., but this value seems to be unused?
                         # only needed by Asset.end_date and Asset.available, but those are never called?
        },

    }

    _defaultresolution = None # [number, number] TODO get this value from science nerds, needed for core.py calls

    # TODO here down
    def __init__(self, filename):
        """ Inspect a single file and get some metadata """
        super(sentinel2Asset, self).__init__(filename)
        raise NotImplementedError()

    @classmethod
    def fetch(cls, asset, tile, date):
        """Fetch the asset corresponding to the given asset type, tile, and date."""
        # set up fetch params
        year, month, day = date.timetuple()[:3]
        username = cls.Repository.get_setting('username')
        password = cls.Repository.get_setting('password')

        # search for the asset's URL with wget call (using a suprocess call to wget instead of a
        # more conventional call to a lib because available libs are perceived to be inferior).
        search_url = cls._assets[asset]['url'] + (
                #          year mon day                    tile
                'S2?_MSIL1C_{}{:02}{:02}T??????_N????_R???_T{}_*.SAFE'.format(year, month, day, tile))
        search_cmd = (
                'wget --no-verbose --no-check-certificate --user="{}" --password="{}" --timeout 30'
                ' --output-document=/dev/stdout "{}"').format(username, password, search_url)
        with utils.error_handler("Error retrieving '{}'".format(search_url)):
            args = shlex.split(search_cmd)
            p = subprocess.Popen(args, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
            (stdout_data, stderr_data) = p.communicate()
            if p.returncode != 0:
                verbose_out(stderr_data, stream=sys.stderr)
                raise IOError("Expected wget exit status 0, got {}".format(p.returncode))

        print("=== GOT OUTPUT ===")
        print(stdout_data)
        print("==================")

        raise NotImplementedError('fetch is in-progress')

    def updated(self, newasset):
        '''
        Compare the version for this to that of newasset.
        Return true if newasset version is greater.
        '''
        return (self.sensor == newasset.sensor and
                self.tile == newasset.tile and
                self.date == newasset.date and
                self.version < newasset.version)


class sentinel2Data(Data):
    name = 'Sentinel-2'
    version = '0.1.0'
    Asset = sentinel2Asset

    _productgroups = {
        "Placeholder Products": ['placeholder'],
    }
    _products = {
        # placeholder product standing in for the real thing so fetch can work
        'placeholder': {
            'description': 'Placeholder Product',
            'assets': ['L1C'],
        },
    }


    def process(self, *args, **kwargs):
        raise NotImplementedError()
