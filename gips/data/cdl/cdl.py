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

import os
import datetime
from csv import DictReader

from gips.data.core import Repository, Asset, Data

# make the compiler spell-check the one sensor, product, and asset type in the driver
_cdl = 'cdl'

class cdlRepository(Repository):
    name = 'CDL'
    description = 'Crop Data Layer'
    _datedir = '%Y'
    _defaultresolution = [30.0, 30.0]
    _tile_attribute = 'STATE_ABBR'


class cdlAsset(Asset):
    Repository = cdlRepository

    _sensors = {_cdl: {'description': 'Crop Data Layer'}}
    _assets = {
        _cdl: {
            # CDL assets are named just like products: tile_date_sensor_asset-product.tif
            'pattern': r'^(?P<tile>[A-Z]{2})_(?P<date>\d{4})_' + _cdl + '_' + _cdl + '\.tif$'
        }
    }

    def __init__(self, filename):
        """Use the given filename to set metadata."""
        super(cdlAsset, self).__init__(filename)
        self.tile, date_str = self.parse_asset_fp().group('tile', 'date')
        self.date = datetime.datetime.strptime(date_str, self.Repository._datedir).date()
        self.asset = _cdl
        self.sensor = _cdl
        self.products[_cdl] = filename # magically it is also a product


class cdlData(Data):
    """ A tile (CONUS State) of CDL """
    name = 'CDL'
    version = '0.9.0'
    Asset = cdlAsset
    _products = {
        _cdl: {
            'description': 'Crop Data Layer',
            'assets': [_cdl],
            'bands': [{'name': _cdl, 'units': 'none'}],
            # presently 'startdate' & 'latency' are permitted to be unspecified
            # by DH gips.utils.get_data_variables
        }
    }

    _legend = None

    @classmethod
    def legend(cls):
        """Open the legend file, keeping it memoized for future calls."""
        if cls._legend is None:
            legend_fp = os.path.join(cdlRepository.get_setting('repository'), 'CDL_Legend.csv')
            cls._legend = [row['ClassName'].lower() for row in DictReader(open(legend_fp))]
        return cls._legend

    @classmethod
    def get_code(cls, cropname):
        """Retrieve CDL code for the given crop name (lower case)."""
        return cls.legend().index(cropname)

    @classmethod
    def get_cropname(cls, code):
        """Retrieve name associated with given crop code."""
        return cls.legend()[code]
