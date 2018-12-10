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

from backports.functools_lru_cache import lru_cache

from gips.data.core import Repository, Asset, Data


class hlsRepository(Repository):
    name = 'hls'
    description = 'harmonized Landsat & Sentinel-2 data provided by NASA'
    _tile_attribute = 'Name'


class hlsAsset(Asset):
    Repository = hlsRepository

    _sensors = {} # TODO

    _assets = {} # TODO

    def __init__(self):
        super(hlsAsset, self).__init__(filename)

    @classmethod
    @lru_cache(maxsize=100) # cache size chosen arbitrarily
    def query_service(cls, asset, tile, date, pclouds=100, **ignored):
        # TODO query_provider instead?
        raise NotImplementedError()

    @classmethod
    def fetch(cls, asset, tile, date, pclouds=100, **ignored):
        raise NotImplementedError()


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
