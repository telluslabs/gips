#!/usr/bin/env python
################################################################################
#    GIPS: Geospatial Image Processing System
#
#    Copyright (C) 2018 Applied Geosolutions
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

import requests
from backports.functools_lru_cache import lru_cache

from gips.data.core import Repository, Asset, Data
from gips import utils
from gips.utils import verbose_out

from gips.data.sentinel2 import sentinel2
from gips.data.landsat import landsat

# User guide & other docs here:  https://hls.gsfc.nasa.gov/documents/

_hls_version = '1.4'
_url_base = 'https://hls.gsfc.nasa.gov/data/v' + _hls_version
_ordered_asset_types = 'S30', 'L30' # for now assume sentinel-2 is preferred

class hlsRepository(Repository):
    name = 'hls'
    description = 'harmonized Landsat & Sentinel-2 data provided by NASA'
    _tile_attribute = 'Name'


class hlsAsset(Asset):
    Repository = hlsRepository

    _sensors = {
        'L30': {
            'description': 'Landsat-8 OLI harmonized surface reflectance',
        },
        'S30': {
            'description': 'Sentinel-2 MSI harmonized surface reflectance',
        }
    }

    # TODO not sure if want '^' at beginning?  is <atype> really needed?
    # literal for asset type is subbed in below
    _asset_fn_pat_base = (r'^HLS\.(?P<atype>{})\.T(?P<tile>\d\d[A-Z]{{3}})'
        r'\.(?P<date>\d{{7}})\.v(?P<version>...)\.hdf$')

    _assets = {
        'L30': {
            'pattern': _asset_fn_pat_base.format('L30'),
            'startdate': landsat.landsatAsset._assets['C1']['startdate'],
            'latency': 7,
        },
        'S30': {
            'pattern': _asset_fn_pat_base.format('S30'),
            'startdate': sentinel2.sentinel2Asset._assets['L1C']['startdate'],
            'latency': 7,
        }
    }

    def __init__(self, filename):
        """
        All the spectral measurements and QA data from a given sensor on
        a day for a tile are saved in a single HDF, named with the
        following naming convention:
            HLS.<HLS_Product>.T<Tile_ID>.<year><doy>.v<version_number>.hdf
        where:
            - <HLS_Product> is the HLS product type (S10, S30 or L30) [3 symbols]
            - <Tile_ID> is the MGRS Tile ID [5 digits]
            - <Year> is the sensing time year [4 digits]
            - <Doy> is the sensing time day of year [3 digits]
            - <Version_number> is the HLS version number (e.g., 1.2) [3 digits]
        """
        # TODO some of this is boilerplate and can be DRYed with other drivers
        super(hlsAsset, self).__init__(filename)
        self.basename = os.path.basename(filename)
        match = None
        for a_type, a_properties in self._assets.items():
            match = re.match(a_properties['pattern'], self.basename)
            if match is not None:
                break
        if match is None:
            raise IOError('Unparseable asset filename `{}`'.format(
                self.basename))

        self.asset, self.tile = match.group('atype', 'tile')
        self.sensor = self.asset
        self.date = datetime.datetime.strptime(
            match.group('date'), self.Repository._datedir).date()
        self._version = float(match.group('version'))

    @classmethod
    @lru_cache(maxsize=1)
    def check_hls_version(cls):
        """Once per runtime, confirm 1.4 is still usable."""
        r = requests.head(_url_base + '/')
        if r.status_code == 200:
            verbose_out('HLS URL base `{}` confirmed valid'.format(_url_base), 5)
        else:
            raise requests.HTTPError('HLS URL base `{}` returned status code'
                ' {}; HLS version may have changed'.format(
                    _url_base, r.status_code))

    @classmethod
    def query_provider(cls, asset, tile, date, pclouds=100, **ignored):
        # TODO handle pclouds
        cls.check_hls_version()
        # build the full URL & basename of the file
        basename = 'HLS.{}.T{}.{}.v{}.hdf'.format(
            asset, tile, date.strftime('%Y%j'), _hls_version)
        zbcr = '/'.join([tile[0:2]] + list(tile[2:])) # '19TCH' -> '19/T/C/H'
        url = '/'.join([_url_base, asset, str(date.year), zbcr, basename])
        if requests.head(url).status_code == 200: # so do they have it?
            return basename, url
        return None, None

    @classmethod
    def download(cls, url, download_fp, **ignored):
        utils.http_download(url, download_fp)


class hlsData(Data):
    version = '1.0.0'
    Asset = hlsAsset

    _productgroups = {} # TODO

    _products = {}
    # TODO DRY out (see sentinel-2)
    # TODO does L30 support all these?
    # TODO does S30 support all these?
    # add index products to _products
    _products.update(
        (p, {'description': d,
             'assets': _ordered_asset_types,
             'bands': [{'name': p, 'units': Data._unitless}]}
         ) for p, d in [
            # duplicated in modis and landsat; may be worth it to DRY out
            ('ndvi',   'Normalized Difference Vegetation Index'),
            # ('evi',    'Enhanced Vegetation Index'),
            # ('lswi',   'Land Surface Water Index'),
            # ('ndsi',   'Normalized Difference Snow Index'),
            # ('bi',     'Brightness Index'),
            # ('satvi',  'Soil-Adjusted Total Vegetation Index'),
            # ('msavi2', 'Modified Soil-adjusted Vegetation Index'),
            # ('vari',   'Visible Atmospherically Resistant Index'),
            # ('brgt',   'VIS and NIR reflectance, weighted by solar energy distribution.'),
            # # index products related to tillage
            # ('ndti',   'Normalized Difference Tillage Index'),
            # ('crc',    'Crop Residue Cover (uses BLUE)'),
            # ('crcm',   'Crop Residue Cover, Modified (uses GREEN)'),
            # ('isti',   'Inverse Standard Tillage Index'),
            # ('sti',    'Standard Tillage Index'),
        ]
    )

    @classmethod
    def normalize_tile_string(cls, tile_string):
        return sentinel2.sentinel2Data.normalize_tile_string(tile_string)

    # TODO copy sentinel-2 to implement pclouds
    #@classmethod
    #def add_filter_args(cls, parser):
        #pass
    #def filter(self, pclouds=100, **kwargs):
        #return all([asset.filter(pclouds, **kwargs) for asset in self.assets.values()])

    def prep_meta(self, additional=None):
        # TODO confirm this use of sentinel-2 version
        meta = super(sentinel2Data, self).prep_meta(
            self.current_asset().filename, additional)
        return meta

    @Data.proc_temp_dir_manager
    def process(self, products=None, overwrite=False, **kwargs):
        # TODO for now just gippy indices
        raise NotImplementedError()
