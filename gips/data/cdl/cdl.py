#!/usr/bin/env python
################################################################################
#    GIPS: Geospatial Image Processing System
#
#    AUTHOR: Matthew Hanson
#    EMAIL:  matt.a.hanson@gmail.com
#
#    Copyright (C) 2014-2018 Applied Geosolutions
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

import os
import re
import datetime
from csv import DictReader
import glob
import shutil
from xml.etree import ElementTree
from zipfile import ZipFile

from backports.functools_lru_cache import lru_cache
from dbfread import DBF
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

import gips
from gips.data.core import Repository, Asset, Data
from gips import utils
from gips.utils import verbose_out
from gippy import GeoImage
from osgeo import gdal

import imghdr

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# make the compiler spell-check the one sensor, product, and asset type in the driver
_cdl = 'cdl'
_cdlmkii = 'cdlmkii'


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
            'pattern': r'^(?P<tile>[A-Z]{2})_(?P<date>\d{4})_' + _cdl + '_' + _cdl + r'\.tif$',
            'startdate': datetime.date(1997, 1, 1),
            'latency': 365, # released in february for the previous year
                            # which we interpret as january that year
        },
        _cdlmkii: {
            'pattern': r'^(?P<tile>[A-Z]{2})_(?P<date>\d{4})_' + _cdl + '_' + _cdlmkii + r'\.zip$',
            'description': '',
            'startdate': datetime.date(1997, 1, 1),
            'latency': 365, # see previous for explanation for this crazy value
        },
    }

    def __init__(self, filename):
        """Use the given filename to set metadata."""
        super(cdlAsset, self).__init__(filename)
        self.tile, date_str = self.parse_asset_fp().group('tile', 'date')
        self.date = datetime.datetime.strptime(date_str, self.Repository._datedir).date()
        if re.match(self._assets[_cdl]['pattern'], os.path.basename(filename)):
            self.asset = _cdl
        else:
            self.asset = _cdlmkii
        self.sensor = _cdl
        self.products[self.asset] = filename  # magically it is also a product

    @classmethod
    @lru_cache(maxsize=100) # cache size chosen arbitrarily
    def query_service(cls, asset, tile, date):
        if asset == _cdlmkii:
            return None
        url = "https://nassgeodata.gmu.edu/axis2/services/CDLService/GetCDLFile"
        tile_vector = utils.open_vector(cls.Repository.get_setting('tiles'), 'STATE_ABBR')[tile]
        params = {
            'year': date.year,
            'fips': tile_vector['STATE_FIPS']
        }
        xml = requests.get(url, params=params, verify=False)
        if xml.status_code != 200:
            return None
        root = ElementTree.fromstring(xml.text)
        file_url = root.find('./returnURL').text
        return {'url': file_url,
                'basename': "{}_{}_cdl_cdl.tif".format(tile, date.year)}

    @classmethod
    def fetch(cls, asset, tile, date):
        # The nassgeodata site is known to have an invalid certificate.
        # We don't want to clutter up the output with SSL warnings.

        if asset == _cdlmkii:
            verbose_out("Fetching not supported for cdlmkii", 2)
            return []
        verbose_out("Fetching tile for {} on {}".format(tile, date.year), 2)
        query_rv = cls.query_service(asset, tile, date)
        if query_rv is None:
            verbose_out("No CDL data for {} on {}".format(tile, date.year), 2)
            return []
        file_response = requests.get(
            query_rv['url'], verify=False, stream=True)
        with utils.make_temp_dir(
                prefix='fetch', dir=cls.Repository.path('stage')) as tmp_dir:
            fname = "{}_{}_cdl_cdl.tif".format(tile, date.year)
            tmp_fname = tmp_dir + '/' + fname
            with open(tmp_fname, 'w') as asset:
                asset.write(file_response.content)
            imgout = GeoImage(tmp_fname, True)
            imgout.set_nodata(0)
            imgout.add_meta('GIPS_Version', gips.__version__)
            imgout = None
            shutil.copy(tmp_fname, cls.Repository.path('stage'))


class cdlData(Data):
    """ A tile (CONUS State) of CDL """
    name = 'CDL'
    version = '0.9.0'
    Asset = cdlAsset
    _products = {
        _cdl: {
            'description': 'Crop Data Layer',
            'assets': [_cdl, _cdlmkii],
            'bands': [{'name': _cdl, 'units': 'none'}],
            # presently 'startdate' & 'latency' are permitted to be unspecified
            # by DH gips.utils.get_data_variables
        }
    }

    @Data.proc_temp_dir_manager
    def process(self, products, overwrite=False, **kwargs):
        for asset_type, asset in self.assets.iteritems():
            if asset_type != _cdlmkii:  # with older cdl products, the asset is the product
                continue

            fname = self.temp_product_filename(_cdl, _cdlmkii)
            fname_without_ext, _ = os.path.splitext(fname)

            with ZipFile(asset.filename, 'r') as zipfile:
                for member in zipfile.infolist():
                    member_ext = member.filename.split('.', 1)[1]
                    extracted = zipfile.extract(member, fname_without_ext)
                    os.rename(extracted, fname_without_ext + '.' + member_ext)

            image = GeoImage(fname, True)
            image[0].set_nodata(0)
            image = None

            image = gdal.Open(fname, gdal.GA_Update)
            dbf = DBF(fname + '.vat.dbf')
            for i, record in enumerate(dbf):
                image.add_meta(str("CLASS_NAME_%s" % record['CLASS_NAME']), str(i))
            image = None

            archive_fp = self.archive_temp_path(fname)
            self.AddFile(_cdl, _cdl, archive_fp)

    def legend(self):
        """Open the legend file, keeping it memoized for future calls."""
        if getattr(self, "_legend", None) is None:
            if self.assets.keys()[0] == _cdlmkii:
                self._legend = [''] * 256
                im = gdal.Open(os.path.splitext(self.assets[_cdlmkii].filename)[0] + '.tif')
                for key, val in im.GetMetadata().iteritems():
                    if key[0:10] == 'CLASS_NAME':
                        self._legend[int(val)] = key[11:]
            else:
                legend_fp = os.path.join(cdlRepository.get_setting('repository'), 'CDL_Legend.csv')
                self._legend = [row['ClassName'].lower() for row in DictReader(open(legend_fp))]
        return self._legend

    def get_code(self, cropname):
        """Retrieve CDL code for the given crop name (lower case)."""
        return self.legend().index(cropname)

    def get_cropname(self, code):
        """Retrieve name associated with given crop code."""
        return self.legend()[code]
