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
import re
import datetime
from csv import DictReader
import glob
from itertools import ifilter
from xml.etree import ElementTree
from zipfile import ZipFile

from dbfread import DBF
import requests

from gips.data.core import Repository, Asset, Data
from gips import utils
from gippy import GeoImage, GeoImages
from osgeo import gdal

import imghdr

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
            'pattern': r'^(?P<tile>[A-Z]{2})_(?P<date>\d{4})_' + _cdl + '_' + _cdl + '\.tif$'
        },
        _cdlmkii: {
            'pattern': r'^(?P<tile>[A-Z]{2})_(?P<date>\d{4})_' + _cdl + '_' + _cdlmkii + '\.zip$',
            'description': '',
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
    def fetch(cls, asset, tile, date):
        # The nassgeodata site is known to have an invalid certificate.
        # We don't want to clutter up the output with SSL warnings.
        import urllib3; urllib3.disable_warnings()

        if asset == _cdl:
            utils.verbose_out("Fetching tile for {} on {}".format(tile, date.year), 2)
            crop_scape_service = "https://nassgeodata.gmu.edu/CropScapeService"
            wcs_url = "{}/wms_cdl_{}.cgi".format(crop_scape_service, tile.lower())

            coverage_parameters = {
                'service': 'wcs',
                'version': '1.1.0',
                'request': 'describecoverage',
                'coverage': "cdl_{}_{}".format(date.year, tile.lower()),
            }
            coverage_xml = requests.get(wcs_url, params=coverage_parameters, verify=False)
            root = ElementTree.fromstring(coverage_xml.text)
            ns = {'ows': 'http://www.opengis.net/ows/1.1', 'wcs': 'http://www.opengis.net/wcs/1.1'}
            lower_corner = root.find(
                ".//ows:BoundingBox[@crs='urn:ogc:def:crs:EPSG::102004']/ows:LowerCorner",
                ns
            ).text
            upper_corner = root.find(
                ".//ows:BoundingBox[@crs='urn:ogc:def:crs:EPSG::102004']/ows:UpperCorner",
                ns
            ).text

            # The CropScapeService's WCS serves coverages that are a max of
            # 2048x2048 pixels. Since this is smaller than almost every state,
            # images must be fetched in small parts and then mosaicked
            # together.
            coord_step = 30 * 2048  # cov must be max 2048x2048
            init_x, init_y = [int(coord) for coord in lower_corner.split(" ")]
            max_x, max_y = [int(coord) + coord_step for coord in upper_corner.split(" ")]
            chip_number = 0
            asset_name = "{}_{}_cdl_cdl.tif".format(tile, date.year)

            prev_x = init_x
            for cur_x in range(init_x, max_x, coord_step):
                prev_y = init_y
                for cur_y in range(init_y, max_y, coord_step):
                    bbox = "{},{},{},{}".format(prev_x, prev_y, cur_x, cur_y)
                    feature_parameters = {
                        'service': 'wcs',
                        'version': '1.0.0',
                        'request': 'getcoverage',
                        'coverage': "cdl_{}_{}".format(date.year, tile.lower()),
                        'crs': 'epsg:102004',
                        'bbox': bbox,
                        'resx': '30',
                        'resy': '30',
                        'format': 'gtiff',
                    }
                    r = requests.get(wcs_url, params=feature_parameters, stream=True, verify=False)

                    with open("{}/{}_{}".format(
                              cls.Repository.path('stage'),
                              chip_number,
                              asset_name),
                              'w') as asset_file:
                        asset_file.write(r.content)

                    prev_y = cur_y
                    chip_number += 1
                prev_x = cur_x
                chip_number += 1

            chips = glob.glob("{}/*_{}".format(cls.Repository.path('stage'), asset_name))

            # Iterating over a grid of 2048x2048 squares, as above, occasionally
            # produces a request that is outside of the coverage area. In this
            # case, the WCS returns an XML error response, so we need to filter
            # those out before mosaicking.
            def is_valid_image(chip):
                try:
                    GeoImage(chip)
                except RuntimeError:
                    os.unlink(chip)
                    return False
                return True
            chips = list(ifilter(is_valid_image, chips))

            tile_vector = utils.open_vector(cls.Repository.get_setting('tiles'), 'STATE_ABBR')[tile]
            utils.mosaic(GeoImages(chips), os.path.join(cls.Repository.path('stage'), asset_name), tile_vector)
            for chip in chips:
                os.unlink(chip)
        else:
            utils.verbose_out("Fetching not supported for cdlmkii", 2)


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
            image[0].SetNoData(0)
            image = None

            image = gdal.Open(fname, gdal.GA_Update)
            dbf = DBF(fname + '.vat.dbf')
            for i, record in enumerate(dbf):
                image.SetMetadataItem(str("CLASS_NAME_%s" % record['CLASS_NAME']), str(i))
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
