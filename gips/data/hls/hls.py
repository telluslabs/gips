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

import re

import requests
from backports.functools_lru_cache import lru_cache

from gips.data.core import Repository, Asset, Data
from gips.utils import verbose_out

# User guide & other docs here:  https://hls.gsfc.nasa.gov/documents/

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
        r'\.(?P<year>\d\d\d\d)(?P<doy>\d\d\d)\.v(?P<version>...)\.hdf$')

    _assets = {
        'L30': {
            'pattern': _asset_fn_pat_base.format('L30'),
            'startdate': None, # TODO
            'latency': 7,
        },
        'S30': {
            'pattern': _asset_fn_pat_base.format('S30'),
            'startdate': None, # TODO
            'latency': 7,
        }
    }

    def __init__(self):
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
        super(hlsAsset, self).__init__(filename)

    _hls_version = '1.4'
    _url_base = 'https://hls.gsfc.nasa.gov/data/v' + _hls_version

    @classmethod
    @lru_cache(maxsize=1)
    def check_hls_version(cls):
        """Once per runtime, confirm 1.4 is still usable."""
        r = requests.head(_url_base)
        if r.status_code == 200:
            verbose_out('HLS URL base `{}` confirmed valid'.format(_url_base), 5)
        else:
            raise requests.HTTPError('HLS URL base `{}` returned status code'
                ' {}; HLS version may have changed'.format(
                    _url_base, r.status_code))

    @classmethod
    def query_provider(cls, asset, tile, date, pclouds=100, **ignored):
        cls.check_hls_version()
        # build the full URL & basename of the file
        basename = 'HLS.{}.T{}.{}.v{}.hdf'.format(
            asset, tile, date.strftime('%Y%j'), cls._hls_version)
        zbcr = '/'.join(tile[0:2], *(tile[2:])) # eg '19/T/C/H'
        url = 'https://hls.gsfc.nasa.gov/data/{}/{}/{}/{}'.format(
                asset, date.year, zbcr, basename)
        if requests.head(url).status_code == 200: # so do they have it?
            return basename, url
        return None, None

    @classmethod
    def fetch(cls, asset, tile, date, pclouds=100, **ignored):
        # each asset has an hdr alongside; not sure if want
        verbose_out('DOING NOTHING HURRR')


class hlsData(Data):
    version = '1.0.0'
    Asset = hlsAsset

    _productgroups = {} # TODO

    _products = {} # TODO

    @classmethod
    def normalize_tile_string(cls, tile_string):
        # TODO probably copy sentinel-2
        return tile_string

    @classmethod
    def add_filter_args(cls, parser):
        # TODO probably copy sentinel-2
        pass

    def filter(self, pclouds=100, **kwargs):
        # TODO confirm this use of sentinel-2 version
        return all([asset.filter(pclouds, **kwargs) for asset in self.assets.values()])

    def prep_meta(self, additional=None):
        # TODO confirm this use of sentinel-2 version
        meta = super(sentinel2Data, self).prep_meta(
            self.current_asset().filename, additional)
        return meta

    @Data.proc_temp_dir_manager
    def process(self, products=None, overwrite=False, **kwargs):
        # TODO for now just gippy indices
        raise NotImplementedError()
