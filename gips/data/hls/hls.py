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

import os
import re
import datetime

import requests
from backports.functools_lru_cache import lru_cache
import gippy

from gips.data.core import Repository, Data
import gips.data.core
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

    @classmethod
    def get_setting(cls, key):
        if key == 'tiles':
            return sentinel2.sentinel2Repository.get_setting('tiles')
        return super(hlsRepository, cls).get_setting(key)


class hlsAsset(gips.data.core.CloudCoverAsset):
    Repository = hlsRepository

    _sensors = {
        'L30': {
            'description': 'Landsat-8 OLI harmonized surface reflectance',
            'colors': landsat.landsatAsset._sensors['LC8']['colors'],
        },
        'S30': {
            'description': 'Sentinel-2 MSI harmonized surface reflectance',
            'colors': sentinel2.sentinel2Asset._sensors['S2A']['colors'],
            #'no-data-value': -1000, 'gain': 0.0001
            # for raster bands:  30m, int16
            # QA band:  30m, uint8, ndv=255, gain=n/a
        }
    }

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
        """Instantiate an HLS asset.  From the docs:

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

    def cloud_cover(self):
        return float(gippy.GeoImage(self.filename).Meta('cloud_coverage'))

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
    def query_provider(cls, asset, tile, date, **ignored):
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
    def download(cls, url, download_fp, pclouds=100.0, **ignored):
        utils.http_download(url, download_fp)
        return cls(download_fp).filter(pclouds)

    def load_image(self):
        """Load this asset into a GeoImage and return it."""
        subdatasets = self.datafiles()
        image = gippy.GeoImage(subdatasets)
        colors = self.sensor_spec('colors')
        [image.SetBandName(name, i) for (i, name) in enumerate(colors, 1)]
        return image


class hlsData(gips.data.core.CloudCoverData):
    version = '1.0.0'
    Asset = hlsAsset

    _productgroups = {}
    _products = {}
    gips.data.core.add_gippy_index_products(
        _products, _productgroups, _ordered_asset_types)

    @classmethod
    def normalize_tile_string(cls, tile_string):
        return sentinel2.sentinel2Data.normalize_tile_string(tile_string)

    @classmethod
    def add_filter_args(cls, parser):
        """Add custom filtering options for landsat."""
        help_str = ('cloud percentage threshold; assets with cloud cover'
                    ' percentages higher than this value will be filtered out')
        parser.add_argument('--pclouds', help=help_str,
                            type=cls.natural_percentage, default=100)

    def prep_meta(self, additional=None):
        meta = super(hlsData, self).prep_meta(
            self.current_asset().filename, additional)
        return meta

    def current_asset(self):
        """Pick the currently-preferred asset type."""
        return next(self.assets[at]
                    for at in _ordered_asset_types if at in self.assets)

    @Data.proc_temp_dir_manager
    def process(self, products=None, overwrite=False, **kwargs):
        """Hope you like index products."""
        # TODO another place that can be DRY'd out; several drivers process similarly
        products = self.needed_products(products, overwrite)
        if len(products) == 0:
            verbose_out('No new processing required.', 5)
            return

        indices = products.groups()['Index']
        metadata = self.prep_meta()
        a_obj = self.current_asset()

        # indices' values are the keys, split by hyphen, eg {ndvi-toa':
        # ['ndvi', 'toa']} (technically it's useless here, as no argumentated
        # products are supported; doing it for consistency).
        gippy_input = {} # gippy wants p-types mapped to output filenames
        tempfps_to_ptypes = {} # AddFile needs a map of p-types to filenames
        for prod_type, pt_split in indices.items():
            temp_fp = self.temp_product_filename(a_obj.sensor, prod_type)
            gippy_input[pt_split[0]] = temp_fp
            tempfps_to_ptypes[temp_fp] = prod_type

        prodout = gippy.algorithms.Indices(
            a_obj.load_image(), gippy_input, metadata)

        for temp_fp in prodout.values():
            archived_fp = self.archive_temp_path(temp_fp)
            self.AddFile(a_obj.sensor, tempfps_to_ptypes[temp_fp], archived_fp)
