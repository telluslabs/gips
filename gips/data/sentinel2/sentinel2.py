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
#import sys
#import re
#import datetime

#import urllib
#import urllib2

#import math
#import numpy as np
#import requests

#import gippy
#from gippy.algorithms import Indices
#from gips.data.core import Repository, Asset, Data
#from gips.utils import VerboseOut, settings
#from gips import utils

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
        raise NotImplemented()

    @classmethod
    def fetch(cls, asset, tile, date):
        raise NotImplemented()

    def updated(self, newasset):
        '''
        Compare the version for this to that of newasset.
        Return true if newasset version is greater.
        '''
        return (self.sensor == newasset.sensor and
                self.tile == newasset.tile and
                self.date == newasset.date and
                self.version < newasset.version)
