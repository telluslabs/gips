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

from __future__ import print_function

import os
import sys
import re
import datetime

import urllib
import urllib2

import math
import numpy as np
import requests

import gippy
from gippy.algorithms import Indices
from gips.data.core import Repository, Asset, Data
from gips.utils import VerboseOut, settings
from gips import utils

from pdb import set_trace


def binmask(arr, bit):
    """ Return boolean array indicating which elements as binary have a 1 in
        a specified bit position. Input is Numpy array.
    """
    return arr & (1 << (bit - 1)) == (1 << (bit - 1))


class modisRepository(Repository):
    name = 'Modis'
    description = 'MODIS Aqua and Terra'

    @classmethod
    def feature2tile(cls, feature):
        """ convert tile field attributes to tile identifier """
        fldindex_h = feature.GetFieldIndex("h")
        fldindex_v = feature.GetFieldIndex("v")
        h = str(int(feature.GetField(fldindex_h))).zfill(2)
        v = str(int(feature.GetField(fldindex_v))).zfill(2)
        return "h%sv%s" % (h, v)


class modisAsset(Asset):
    Repository = modisRepository

    _sensors = {
        'MOD': {'description': 'Terra'},
        'MYD': {'description': 'Aqua'},
        'MCD': {'description': 'Aqua/Terra Combined'},
        'MOD-MYD': {'description': 'Aqua/Terra together'}
    }

    # modis data used to be free for all, now you have to log in, hence no assets skip auth.
    _skip_auth = []

    _asset_re_tail = '\.A.{7}\.h.{2}v.{2}\..{3}\..{13}\.hdf$'

    _assets = {
        'MCD43A4': {
            'pattern': '^MCD43A4' + _asset_re_tail,
            'url': 'https://e4ftl01.cr.usgs.gov/MOTA/MCD43A4.006',
            'startdate': datetime.date(2000, 2, 18),
            'latency': -15
        },
        'MCD43A2': {
            'pattern': '^MCD43A2' + _asset_re_tail,
            'url': 'https://e4ftl01.cr.usgs.gov/MOTA/MCD43A2.006',
            'startdate': datetime.date(2000, 2, 18),
            'latency': -15
        },
        'MOD09Q1': {
            'pattern': '^MOD09Q1' + _asset_re_tail,
            'url': 'https://e4ftl01.cr.usgs.gov/MOLT/MOD09Q1.006/',
            'startdate': datetime.date(2000, 2, 18),
            'latency': -7,
        },
        'MOD10A1': {
            'pattern': '^MOD10A1' + _asset_re_tail,
            'url': 'https://n5eil01u.ecs.nsidc.org/MOST/MOD10A1.005/',
            'startdate': datetime.date(2000, 2, 24),
            'latency': -3
        },
        'MYD10A1': {
            'pattern': '^MYD10A1' + _asset_re_tail,
            'url': 'https://n5eil01u.ecs.nsidc.org/MOSA/MYD10A1.005/',
            'startdate': datetime.date(2002, 7, 4),
            'latency': -3
        },
        'MOD11A1': {
            'pattern': '^MOD11A1' + _asset_re_tail,
            'url': 'https://e4ftl01.cr.usgs.gov/MOLT/MOD11A1.006',
            'startdate': datetime.date(2000, 3, 5),
            'latency': -1
        },
        'MYD11A1': {
            'pattern': '^MYD11A1' + _asset_re_tail,
            'url': 'https://e4ftl01.cr.usgs.gov/MOLA/MYD11A1.006',
            'startdate': datetime.date(2002, 7, 8),
            'latency': -1
        },
        'MOD11A2': {
            'pattern': '^MOD11A2' + _asset_re_tail,
            'url': 'https://e4ftl01.cr.usgs.gov/MOLT/MOD11A2.006',
            'startdate': datetime.date(2000, 3, 5),
            'latency': -7
        },
        'MYD11A2': {
            'pattern': '^MYD11A2' + _asset_re_tail,
            'url': 'https://e4ftl01.cr.usgs.gov/MOLA/MYD11A2.006',
            'startdate': datetime.date(2002, 7, 4),
            'latency': -7
        },
        'MOD10A2': {
            'pattern': '^MOD10A2' + _asset_re_tail,
            'url': 'https://n5eil01u.ecs.nsidc.org/MOST/MOD10A2.006/',
            'startdate': datetime.date(2000, 2, 24),
            'latency': -3
        },
        'MYD10A2': {
            'pattern': '^MYD10A2' + _asset_re_tail,
            'url': 'https://n5eil01u.ecs.nsidc.org/MOSA/MYD10A2.006/',
            'startdate': datetime.date(2002, 7, 4),
            'latency': -3
        },
        'MCD12Q1': {
            'pattern': '^MCD12Q1' + _asset_re_tail,
            'url': 'https://e4ftl01.cr.usgs.gov/MOTA/MCD12Q1.051',
            'startdate': datetime.date(2002, 7, 4),
            'latency': -3
        },

    }

    # Should this be specified on a per asset basis? (in which case retrieve from asset)
    _defaultresolution = [926.625433138333392, 926.625433139166944]

    def __init__(self, filename):
        """ Inspect a single file and get some metadata """
        super(modisAsset, self).__init__(filename)

        bname = os.path.basename(filename)
        parts = bname.split('.')

        self.asset = parts[0]
        self.tile = parts[2]
        self.sensor = parts[0][:3]

        year = parts[1][1:5]
        doy = parts[1][5:8]
        self.date = datetime.datetime.strptime(year + doy, "%Y%j").date()

        collection = int(parts[3])
        file_version = int(parts[4])
        self.version = float('{}.{}'.format(collection, file_version))


    @classmethod
    def query_service(cls, asset, tile, date):
        """Find out from the modis servers what assets are available.

        Uses the given (asset, tile, date) tuple as a search key, and
        returns a list of dicts:  {'basename': base-filename, 'url': url}
        """
        year, month, day = date.timetuple()[:3]

        if asset == "MCD12Q1" and (month, day) != (1, 1):
            utils.verbose_out("Cannot fetch MCD12Q1:  Land cover data"
                              " are only available for Jan. 1", 1, stream=sys.stderr)
            return []

        # if it's going to fail, let's find out early:
        http_query = {'timeout': 30}
        if asset not in cls._skip_auth:
            username = cls.Repository.get_setting('username')
            password = cls.Repository.get_setting('password')
            http_query['auth'] = (username, password)

        mainurl = "%s/%s.%02d.%02d" % (cls._assets[asset]['url'], str(year), month, day)
        pattern = '(%s.A%s%s.%s.\d{3}.\d{13}.hdf)' % (asset, str(year), str(date.timetuple()[7]).zfill(3), tile)
        cpattern = re.compile(pattern)

        if datetime.datetime.today().date().weekday() == 2:
            err_msg = "Error downloading on a Wednesday; possible planned MODIS provider downtime: " + mainurl
        else:
            err_msg = "Error downloading: " + mainurl
        with utils.error_handler(err_msg):
            listing = requests.get(mainurl, **http_query)
            if listing.status_code != requests.codes.ok:
                err_msg = '{} gave bad response code: {}'.format(mainurl, listing.status_code)
                utils.verbose_out(err_msg, 1, stream=sys.stderr)
                # return [] # TODO possibly do nothing here, as empty list case is handled below

        available = []
        for item in listing.iter_lines():
            # screen-scrape the content of the page and extract the full name of the needed file
            # (this step is needed because part of the filename, the creation timestamp, is
            # effectively random).
            if cpattern.search(item):
                if 'xml' in item:
                    continue
                basename = cpattern.findall(item)[0]
                url = ''.join([mainurl, '/', basename])
                available.append({'basename': basename, 'url': url})

        if len(available) == 0:
            utils.verbose_out(
                'Unable to find remote match for {} at {}'
                .format(pattern, mainurl),
                4,
                sys.stderr
            )
        return available


    @classmethod
    def fetch(cls, asset, tile, date):
        available_assets = cls.query_service(asset, tile, date)
        retrieved_filenames = []
        for asset_info in available_assets:
            basename = asset_info['basename']
            url = asset_info['url']
            outpath = os.path.join(cls.Repository.path('stage'), basename)

            with utils.error_handler(
                    "Asset fetch error ({})".format(asset_info),
                    continuable=True
            ):
                # tinkering:
                # chunk size & stream=True in req
                # cookies / cache auth

                # was if mainurl[0:3] == 'ftp':
                if url.startswith('ftp'):
                    connection = urllib2.urlopen(url)
                    with open(outpath, 'wb') as fd:
                        fd.write(connection.read())

                else:  # http
                    kw = {'timeout': 10}
                    if asset not in cls._skip_auth:
                        username = cls.Repository.get_setting('username')
                        password = cls.Repository.get_setting('password')
                        kw['auth'] = (username, password)
                    response = requests.get(url, **kw)

                    if response.status_code != requests.codes.ok:
                        utils.verbose_out(
                            'Download failed({}): code={} reason="{}" url="{}"'
                            .format(basename, response.status_code,
                                    response.reason, url),
                            2,
                            sys.stderr
                        )
                        return retrieved_filenames  # might as well stop b/c the rest will probably fail too

                    with open(outpath, 'wb') as fd:
                        for chunk in response.iter_content():
                            fd.write(chunk)
                utils.verbose_out('Retrieved %s' % basename, 2)
                retrieved_filenames.append(outpath)

        return retrieved_filenames


    def updated(self, newasset):
        '''
        Compare the version for this to that of newasset.
        Return true if newasset version is greater.
        '''
        return (self.sensor == newasset.sensor and
                self.tile == newasset.tile and
                self.date == newasset.date and
                self.version < newasset.version)


class modisData(Data):
    """ A tile of data (all assets and products) """
    name = 'Modis'
    version = '1.0.0'
    Asset = modisAsset
    _productgroups = {
        "Nadir BRDF-Adjusted 16-day": ['indices', 'quality'],
        "Terra/Aqua Daily": ['snow', 'temp', 'obstime', 'fsnow'],
        "Terra 8-day": ['ndvi8', 'temp8tn', 'temp8td'],
    }
    _products = {
        # MCD Products
        'indices': {
            'description': 'Land indices',
            'assets': ['MCD43A4'],
            'sensor': 'MCD',
            'bands': ['ndvi', 'lswi', 'vari', 'brgt', 'satvi', 'evi'],
            'startdate': datetime.date(2000, 2, 18),
            'latency': 15
        },
        'quality': {
            'description': 'MCD Product Quality',
            'assets': ['MCD43A2'],
            'sensor': 'MCD',
            'bands': ['quality'],
            'startdate': datetime.date(2000, 2, 18),
            'latency': 15
        },
        'landcover': {
            'description': 'MCD Annual Land Cover',
            'assets': ['MCD12Q1'],
            'sensor': 'MCD',
            'bands': ['landcover'],
            'startdate': datetime.date(2002, 7, 4),
            'latency': 3
        },
        # Daily
        'fsnow': {
            'description': 'Fractional snow cover data',
            'assets': ['MOD10A1', 'MYD10A1'],
            'sensor': 'MCD',
            'bands': ['fractional-snow-cover'],
            'startdate': datetime.date(2000, 2, 24),
            'latency': 3
        },
        'snow': {
            'description': 'Snow and ice cover data',
            'assets': ['MOD10A1', 'MYD10A1'],
            'sensor': 'MCD',
            'bands': ['snow-cover', 'fractional-snow-cover'],
            'startdate': datetime.date(2000, 2, 24),
            'latency': 3
        },
        'temp': {
            'description': 'Surface temperature data',
            'assets': ['MOD11A1', 'MYD11A1'],
            'sensor': 'MOD-MYD',
            'bands': [
                'temperature-daytime-terra',
                'temperature-nighttime-terra',
                'temperature-daytime-aqua',
                'temperature-nighttime-aqua',
                'temperature-best-quality',
            ],
            'startdate': datetime.date(2000, 3, 5),
            'latency': 1
        },
        'obstime': {
            'description': 'MODIS Terra/Aqua overpass time',
            'assets': ['MOD11A1', 'MYD11A1'],
            'sensor': 'MOD-MYD',
            'bands': [
                'observation-time-daytime-terra',
                'observation-time-nighttime-terra',
                'observation-time-daytime-aqua',
                'observation-time-nighttime-aqua'
            ],
            'startdate': datetime.date(2000, 3, 5),
            'latency': 1
        },
        # Misc
        'ndvi8': {
            'description': 'Normalized Difference Vegetation Index: 250m',
            'assets': ['MOD09Q1'],
            'sensor': 'MOD',
            'bands': ['red', 'nir'],
            'startdate': datetime.date(2000, 2, 18),
            'latency': 7,
        },
        'temp8td': {
            'description': 'Surface temperature: 1km',
            'assets': ['MOD11A2'],
            'sensor': 'MOD',
            'bands': ['temp8td'],
            'startdate': datetime.date(2000, 3, 5),
            'latency': 7
        },
        'temp8tn': {
            'description': 'Surface temperature: 1km',
            'assets': ['MOD11A2'],
            'sensor': 'MOD',
            'bands': ['temp8tn'],
            'startdate': datetime.date(2000, 3, 5),
            'latency': 7
        },
        'clouds': {
            'description': 'Cloud Mask',
            'assets': ['MOD10A1'],
            'sensor': 'MOD',
            'bands': ['cloud-cover'],
            'startdate': datetime.date(2000, 2, 24),
            'latency': 3
        }
    }

    @Data.proc_temp_dir_manager
    def process(self, *args, **kwargs):
        """Produce requested products."""
        products = super(modisData, self).process(*args, **kwargs)
        if len(products) == 0:
            return

        bname = os.path.join(self.path, self.basename)

        # example products.requested: {'temp8tn': ['temp8tn'], 'clouds': ['clouds'], . . . }
        # Note that val[0] is the only usage of val in this method.
        for key, val in products.requested.items():
            start = datetime.datetime.now()

            # Check for asset availability
            assets = self._products[val[0]]['assets']
            missingassets = []
            availassets = []
            allsds = []

            versions = {}

            for asset in assets:
                # many asset types won't be found for the current date/spatial constraint
                if asset not in self.assets:
                    missingassets.append(asset)
                    continue
                try:
                    sds = self.assets[asset].datafiles()
                except Exception as e:
                    utils.report_error(e, 'Error reading datafiles for ' + asset)
                    missingassets.append(asset)
                else:
                    availassets.append(asset)
                    allsds.extend(sds)
                    versions[asset] = int(re.findall('M.*\.(\d{3})\.\d{13}\.hdf', sds[0])[0])

            if not availassets:
                # some products aren't available for every day but this is trying every day
                VerboseOut('There are no available assets (%s) on %s for tile %s'
                           % (str(missingassets), str(self.date), str(self.id), ), 5)
                continue

            meta = self.meta_dict()
            meta['AVAILABLE_ASSETS'] = ' '.join(availassets)

            prod_type = val[0]
            sensor = self._products[prod_type]['sensor']
            fname = self.temp_product_filename(sensor, prod_type) # moved to archive at end of loop

            if val[0] == "landcover":
                os.symlink(allsds[0], fname)
                imgout = gippy.GeoImage(fname)

            if val[0] == "refl":
                # NOTE this code is unreachable (no refl entry in _products)
                if versions[asset] != 6:
                    raise Exception('product version not supported')
                sensor = 'MCD'
                fname = '%s_%s_%s.tif' % (bname, sensor, key)
                img = gippy.GeoImage(sds[7:])
                nodata = img[0].NoDataValue()
                gain = img[0].Gain()
                offset = img[0].Offset()
                imgout = gippy.GeoImage(fname, img, gippy.GDT_Int16, 6)
                imgout.SetNoData(nodata)
                imgout.SetOffset(offset)
                imgout.SetGain(gain)
                for i in range(6):
                    data = img[i].Read()
                    imgout[i].Write(data)
                del img

            if val[0] == "quality":
                if versions[asset] != 6:
                    raise Exception('product version not supported')
                os.symlink(allsds[0], fname)
                imgout = gippy.GeoImage(fname)

            # LAND VEGETATION INDICES PRODUCT
            # now with QC layer!
            if val[0] == "indices":
                VERSION = "2.0"
                meta['VERSION'] = VERSION
                refl = gippy.GeoImage(allsds)
                missing = 32767

                if versions[asset] == 6:
                    redimg = refl[7].Read()
                    nirimg = refl[8].Read()
                    bluimg = refl[9].Read()
                    grnimg = refl[10].Read()
                    mirimg = refl[11].Read()
                    swrimg = refl[12].Read()  # swir1, formerly swir2
                    redqcimg = refl[0].Read()
                    nirqcimg = refl[1].Read()
                    bluqcimg = refl[2].Read()
                    grnqcimg = refl[3].Read()
                    mirqcimg = refl[4].Read()
                    swrqcimg = refl[5].Read()
                else:
                    raise Exception('product version not supported')

                redimg[redimg < 0.0] = 0.0
                nirimg[nirimg < 0.0] = 0.0
                bluimg[bluimg < 0.0] = 0.0
                grnimg[grnimg < 0.0] = 0.0
                mirimg[mirimg < 0.0] = 0.0
                swrimg[swrimg < 0.0] = 0.0

                redimg[(redimg != missing) & (redimg > 1.0)] = 1.0
                nirimg[(nirimg != missing) & (nirimg > 1.0)] = 1.0
                bluimg[(bluimg != missing) & (bluimg > 1.0)] = 1.0
                grnimg[(grnimg != missing) & (grnimg > 1.0)] = 1.0
                mirimg[(mirimg != missing) & (mirimg > 1.0)] = 1.0
                swrimg[(swrimg != missing) & (swrimg > 1.0)] = 1.0

                # red, nir
                ndvi = missing + np.zeros_like(redimg)
                wg = np.where((redimg != missing) & (nirimg != missing) & (redimg + nirimg != 0.0))
                ndvi[wg] = (nirimg[wg] - redimg[wg]) / (nirimg[wg] + redimg[wg])

                # nir, mir
                lswi = missing + np.zeros_like(redimg)
                wg = np.where((nirimg != missing) & (mirimg != missing) & (nirimg + mirimg != 0.0))
                lswi[wg] = (nirimg[wg] - mirimg[wg]) / (nirimg[wg] + mirimg[wg])

                # blu, grn, red
                vari = missing + np.zeros_like(redimg)
                wg = np.where((grnimg != missing) & (redimg != missing) & (bluimg != missing) & (grnimg + redimg - bluimg != 0.0))
                vari[wg] = (grnimg[wg] - redimg[wg]) / (grnimg[wg] + redimg[wg] - bluimg[wg])

                # blu, grn, red, nir
                brgt = missing + np.zeros_like(redimg)
                wg = np.where(
                    (nirimg != missing) & (redimg != missing) &
                    (bluimg != missing) & (grnimg != missing)
                )
                brgt[wg] = (
                    0.3 * bluimg[wg] + 0.3 * redimg[wg] + 0.1 * nirimg[wg] +
                    0.3 * grnimg[wg]
                )

                # red, mir, swr
                satvi = missing + np.zeros_like(redimg)
                wg = np.where(
                    (redimg != missing) & (mirimg != missing) &
                    (swrimg != missing) & ((mirimg + redimg + 0.5) != 0.0)
                )
                satvi[wg] = (
                    ((mirimg[wg] - redimg[wg]) /
                     (mirimg[wg] + redimg[wg] + 0.5)) * 1.5
                ) - (swrimg[wg] / 2.0)

                # blu, red, nir
                evi = missing + np.zeros_like(redimg)
                wg = np.where(
                    (bluimg != missing) & (redimg != missing) &
                    (nirimg != missing) &
                    (nirimg + 6.0 * redimg - 7.5 * bluimg + 1.0 != 0.0)
                )
                evi[wg] = (
                    (2.5 * (nirimg[wg] - redimg[wg])) /
                    (nirimg[wg] + 6.0 * redimg[wg] - 7.5 * bluimg[wg] + 1.0)
                )

                qc = np.ones_like(redimg)  # mark as poor if all are not missing and not all are good
                w0 = np.where(
                    (redqcimg == 0) & (nirqcimg == 0) & (bluqcimg == 0) &
                    (grnqcimg == 0) & (mirqcimg == 0) & (swrqcimg == 0)
                )
                w255 = np.where(
                    (redqcimg == 255) | (nirqcimg == 255) | (bluqcimg == 255) |
                    (grnqcimg == 255) | (mirqcimg == 255) | (swrqcimg == 255)
                )
                qc[w0] = 0  # mark as good if they are all good
                qc[w255] = missing  # mark as missing if any are missing

                # create output gippy image
                print("writing", fname)
                imgout = gippy.GeoImage(fname, refl, gippy.GDT_Int16, 7)
                del refl

                imgout.SetNoData(missing)
                imgout.SetOffset(0.0)
                imgout.SetGain(0.0001)
                imgout[6].SetGain(1.0)

                imgout[0].Write(ndvi)
                imgout[1].Write(lswi)
                imgout[2].Write(vari)
                imgout[3].Write(brgt)
                imgout[4].Write(satvi)
                imgout[5].Write(evi)
                imgout[6].Write(qc)

                imgout.SetBandName('NDVI', 1)
                imgout.SetBandName('LSWI', 2)
                imgout.SetBandName('VARI', 3)
                imgout.SetBandName('BRGT', 4)
                imgout.SetBandName('SATVI', 5)
                imgout.SetBandName('EVI', 6)
                imgout.SetBandName('QC', 7)

            # CLOUD MASK PRODUCT
            if val[0] == "clouds":
                VERSION = "1.0"
                meta['VERSION'] = VERSION

                img = gippy.GeoImage(allsds)

                data = img[0].Read()
                clouds = np.zeros_like(data)

                clouds[data == 0] = 127
                clouds[data == 1] = 127
                clouds[data == 11] = 127
                clouds[data == 25] = 0
                clouds[data == 37] = 0
                clouds[data == 39] = 0
                clouds[data == 50] = 1
                clouds[data == 100] = 0
                clouds[data == 200] = 0
                clouds[data == 254] = 127
                clouds[data == 255] = 127

                # create output gippy image
                imgout = gippy.GeoImage(fname, img, gippy.GDT_Byte, 1)
                del img
                imgout.SetNoData(127)
                imgout.SetOffset(0.0)
                imgout.SetGain(1.0)
                imgout.SetBandName('Cloud Cover', 1)
                imgout[0].Write(clouds)

            # SNOW/ICE COVER PRODUCT - FRACTIONAL masked with binary
            if val[0] == "fsnow":
                VERSION = "1.0"
                meta['VERSION'] = VERSION

                if not missingassets:
                    availbands = [0, 1]
                    snowsds = [allsds[0], allsds[3], allsds[4], allsds[7]]
                elif missingassets[0] == 'MYD10A1':
                    availbands = [0]
                    snowsds = [allsds[0], allsds[3]]
                elif missingassets[0] == 'MOD10A1':
                    availbands = [1]
                    snowsds = [allsds[0], allsds[3]]
                else:
                    raise

                img = gippy.GeoImage(snowsds)

                # there are two snow bands
                for iband, band in enumerate(availbands):

                    # get the data values for both bands
                    cover = img[2 * iband].Read()
                    frac = img[2 * iband + 1].Read()

                    # check out frac
                    wbad1 = np.where((frac == 200) | (frac == 201) | (frac == 211) |
                                     (frac == 250) | (frac == 254) | (frac == 255))
                    wsurface1 = np.where((frac == 225) | (frac == 237) | (frac == 239))
                    wvalid1 = np.where((frac >= 0) & (frac <= 100))

                    nbad1 = len(wbad1[0])
                    nsurface1 = len(wsurface1[0])
                    nvalid1 = len(wvalid1[0])
                    assert nbad1 + nsurface1 + nvalid1 == frac.size, "frac contains invalid values"

                    # check out cover
                    wbad2 = np.where((cover == 0) | (cover == 1) | (cover == 11) |
                                     (cover == 50) | (cover == 254) | (cover == 255))
                    wsurface2 = np.where((cover == 25) | (cover == 37) | (cover == 39))
                    wvalid2 = np.where((cover == 100) | (cover == 200))

                    nbad2 = len(wbad2[0])
                    nsurface2 = len(wsurface2[0])
                    nvalid2 = len(wvalid2[0])
                    assert nbad2 + nsurface2 + nvalid2 == cover.size, "cover contains invalid values"

                    # assign output data here
                    coverout = np.zeros_like(cover, dtype=np.uint8)
                    fracout = np.zeros_like(frac, dtype=np.uint8)

                    fracout[wvalid1] = frac[wvalid1]
                    fracout[wsurface1] = 0
                    fracout[wbad1] = 127
                    coverout[wvalid2] = 100
                    coverout[wsurface2] = 0
                    coverout[wbad2] = 127

                    if len(availbands) == 2:
                        if iband == 0:
                            fracout1 = np.copy(fracout)
                            coverout1 = np.copy(coverout)
                        else:
                            # both the current and previous are valid
                            w = np.where((fracout != 127) & (fracout1 != 127))
                            fracout[w] = np.mean(np.array([fracout[w], fracout1[w]]), axis=0).astype('uint8')

                            # the current is not valid but previous is valid
                            w = np.where((fracout == 127) & (fracout1 != 127))
                            fracout[w] = fracout1[w]

                            # both the current and previous are valid
                            w = np.where((coverout != 127) & (coverout1 != 127))
                            coverout[w] = np.mean(np.array([coverout[w], coverout1[w]]), axis=0).astype('uint8')

                            # the current is not valid but previous is valid
                            w = np.where((coverout == 127) & (coverout1 != 127))
                            coverout[w] = coverout1[w]

                fracmissingcoverclear = np.sum((fracout == 127) & (coverout == 0))
                fracmissingcoversnow = np.sum((fracout == 127) & (coverout == 100))
                fracclearcovermissing = np.sum((fracout == 0) & (coverout == 127))
                fracclearcoversnow = np.sum((fracout == 0) & (coverout == 100))
                fracsnowcovermissing = np.sum((fracout > 0) & (fracout <= 100) & (coverout == 127))
                fracsnowcoverclear = np.sum((fracout > 0) & (fracout <= 100) & (coverout == 0))
                # fracmostlycoverclear = np.sum((fracout > 50) & (fracout <= 100) & (coverout == 0))
                totsnowfrac = int(0.01 * np.sum(fracout[fracout <= 100]))
                totsnowcover = int(0.01 * np.sum(coverout[coverout <= 100]))
                numvalidfrac = np.sum(fracout != 127)
                numvalidcover = np.sum(coverout != 127)

                # mask fractional product with binary
                mask = np.where((coverout == 0) | (coverout == 50))
                fracout[mask] = 0

                if totsnowcover == 0 or totsnowfrac == 0:
                    print("no snow or ice: skipping", str(self.date), str(self.id), str(missingassets))

                meta['FRACMISSINGCOVERCLEAR'] = fracmissingcoverclear
                meta['FRACMISSINGCOVERSNOW'] = fracmissingcoversnow
                meta['FRACCLEARCOVERMISSING'] = fracclearcovermissing
                meta['FRACCLEARCOVERSNOW'] = fracclearcoversnow
                meta['FRACSNOWCOVERMISSING'] = fracsnowcovermissing
                meta['FRACSNOWCOVERCLEAR'] = fracsnowcoverclear
                meta['FRACMOSTLYCOVERCLEAR'] = np.sum((fracout > 50) & (fracout <= 100) & (coverout == 0))
                meta['TOTSNOWFRAC'] = totsnowfrac
                meta['TOTSNOWCOVER'] = totsnowcover
                meta['NUMVALIDFRAC'] = numvalidfrac
                meta['NUMVALIDCOVER'] = numvalidcover

                # create output gippy image
                imgout = gippy.GeoImage(fname, img, gippy.GDT_Byte, 1)
                del img
                imgout.SetNoData(127)
                imgout.SetOffset(0.0)
                imgout.SetGain(1.0)
                # imgout.SetBandName('Snow Cover', 1)
                imgout.SetBandName('Fractional Snow Cover', 1)

                # imgout[0].Write(coverout)
                imgout[0].Write(fracout)

            ###################################################################
            # SNOW/ICE COVER PRODUCT
            if val[0] == "snow":
                VERSION = "1.0"
                meta['VERSION'] = VERSION

                if not missingassets:
                    availbands = [0, 1]
                    snowsds = [allsds[0], allsds[3], allsds[4], allsds[7]]
                elif missingassets[0] == 'MYD10A1':
                    availbands = [0]
                    snowsds = [allsds[0], allsds[3]]
                elif missingassets[0] == 'MOD10A1':
                    availbands = [1]
                    snowsds = [allsds[0], allsds[3]]
                else:
                    raise

                img = gippy.GeoImage(snowsds)

                # there are two snow bands
                for iband, band in enumerate(availbands):

                    # get the data values for both bands
                    cover = img[2 * iband].Read()
                    frac = img[2 * iband + 1].Read()

                    # check out frac
                    wbad1 = np.where((frac == 200) | (frac == 201) | (frac == 211) |
                                     (frac == 250) | (frac == 254) | (frac == 255))
                    wsurface1 = np.where((frac == 225) | (frac == 237) | (frac == 239))
                    wvalid1 = np.where((frac >= 0) & (frac <= 100))

                    nbad1 = len(wbad1[0])
                    nsurface1 = len(wsurface1[0])
                    nvalid1 = len(wvalid1[0])
                    assert nbad1 + nsurface1 + nvalid1 == frac.size, "frac contains invalid values"

                    # check out cover
                    wbad2 = np.where((cover == 0) | (cover == 1) | (cover == 11) |
                                     (cover == 50) | (cover == 254) | (cover == 255))
                    wsurface2 = np.where((cover == 25) | (cover == 37) | (cover == 39))
                    wvalid2 = np.where((cover == 100) | (cover == 200))

                    nbad2 = len(wbad2[0])
                    nsurface2 = len(wsurface2[0])
                    nvalid2 = len(wvalid2[0])
                    assert nbad2 + nsurface2 + nvalid2 == cover.size, "cover contains invalid values"

                    # assign output data here
                    coverout = np.zeros_like(cover, dtype=np.uint8)
                    fracout = np.zeros_like(frac, dtype=np.uint8)

                    fracout[wvalid1] = frac[wvalid1]
                    fracout[wsurface1] = 0
                    fracout[wbad1] = 127
                    coverout[wvalid2] = 100
                    coverout[wsurface2] = 0
                    coverout[wbad2] = 127

                    if len(availbands) == 2:
                        if iband == 0:
                            fracout1 = np.copy(fracout)
                            coverout1 = np.copy(coverout)
                        else:
                            # both the current and previous are valid
                            w = np.where((fracout != 127) & (fracout1 != 127))
                            fracout[w] = np.mean(np.array([fracout[w], fracout1[w]]), axis=0).astype('uint8')

                            # the current is not valid but previous is valid
                            w = np.where((fracout == 127) & (fracout1 != 127))
                            fracout[w] = fracout1[w]

                            # both the current and previous are valid
                            w = np.where((coverout != 127) & (coverout1 != 127))
                            coverout[w] = np.mean(np.array([coverout[w], coverout1[w]]), axis=0).astype('uint8')

                            # the current is not valid but previous is valid
                            w = np.where((coverout == 127) & (coverout1 != 127))
                            coverout[w] = coverout1[w]

                fracmissingcoverclear = np.sum((fracout == 127) & (coverout == 0))
                fracmissingcoversnow = np.sum((fracout == 127) & (coverout == 100))
                fracclearcovermissing = np.sum((fracout == 0) & (coverout == 127))
                fracclearcoversnow = np.sum((fracout == 0) & (coverout == 100))
                fracsnowcovermissing = np.sum((fracout > 0) & (fracout <= 100) & (coverout == 127))
                fracsnowcoverclear = np.sum((fracout > 0) & (fracout <= 100) & (coverout == 0))
                # fracmostlycoverclear = np.sum((fracout > 50) & (fracout <= 100) & (coverout == 0))
                totsnowfrac = int(0.01 * np.sum(fracout[fracout <= 100]))
                totsnowcover = int(0.01 * np.sum(coverout[coverout <= 100]))
                numvalidfrac = np.sum(fracout != 127)
                numvalidcover = np.sum(coverout != 127)

                if totsnowcover == 0 or totsnowfrac == 0:
                    print("no snow or ice: skipping", str(self.date), str(self.id), str(missingassets))

                meta['FRACMISSINGCOVERCLEAR'] = fracmissingcoverclear
                meta['FRACMISSINGCOVERSNOW'] = fracmissingcoversnow
                meta['FRACCLEARCOVERMISSING'] = fracclearcovermissing
                meta['FRACCLEARCOVERSNOW'] = fracclearcoversnow
                meta['FRACSNOWCOVERMISSING'] = fracsnowcovermissing
                meta['FRACSNOWCOVERCLEAR'] = fracsnowcoverclear
                meta['FRACMOSTLYCOVERCLEAR'] = np.sum((fracout > 50) & (fracout <= 100) & (coverout == 0))
                meta['TOTSNOWFRAC'] = totsnowfrac
                meta['TOTSNOWCOVER'] = totsnowcover
                meta['NUMVALIDFRAC'] = numvalidfrac
                meta['NUMVALIDCOVER'] = numvalidcover

                # create output gippy image
                imgout = gippy.GeoImage(fname, img, gippy.GDT_Byte, 2)
                del img
                imgout.SetNoData(127)
                imgout.SetOffset(0.0)
                imgout.SetGain(1.0)
                imgout.SetBandName('Snow Cover', 1)
                imgout.SetBandName('Fractional Snow Cover', 2)

                imgout[0].Write(coverout)
                imgout[1].Write(fracout)

            ###################################################################
            # TEMPERATURE PRODUCT (DAILY)
            if val[0] == "temp":
                VERSION = "1.1"
                meta['VERSION'] = VERSION

                if not missingassets:
                    availbands = [0, 1, 2, 3]
                    tempsds = [allsds[0], allsds[4], allsds[12], allsds[16]]
                    qcsds = [allsds[1], allsds[5], allsds[13], allsds[17]]
                    hoursds = [allsds[2], allsds[6], allsds[14], allsds[18]]
                elif missingassets[0] == 'MYD11A1':
                    availbands = [0, 1]
                    tempsds = [allsds[0], allsds[4]]
                    qcsds = [allsds[1], allsds[5]]
                    hoursds = [allsds[2], allsds[6]]
                elif missingassets[0] == 'MOD11A1':
                    availbands = [2, 3]
                    tempsds = [allsds[0], allsds[4]]
                    qcsds = [allsds[1], allsds[5]]
                    hoursds = [allsds[2], allsds[6]]
                else:
                    raise

                tempbands = gippy.GeoImage(tempsds)
                qcbands = gippy.GeoImage(qcsds)
                hourbands = gippy.GeoImage(hoursds)

                imgout = gippy.GeoImage(fname, tempbands, gippy.GDT_UInt16, 5)
                imgout.SetNoData(65535)
                imgout.SetGain(0.02)

                # there are four temperature bands
                for iband, band in enumerate(availbands):
                    # get meta name template info
                    basename = tempbands[iband].Basename()
                    platform = self.Asset._sensors[basename[:3]]['description']

                    if basename.find('daytime'):
                        dayornight = 'day'
                    elif basename.find('nighttime'):
                        dayornight = 'night'
                    else:
                        raise Exception('%s appears to be an invalid MODIS temperature project' % basename)

                    qc = qcbands[iband].Read()

                    # first two bits are 10 or 11
                    newmaskbad = binmask(qc, 2)
                    # first two bits are 00 or 01
                    newmaskgood = ~binmask(qc, 2)
                    # first two bits are 00
                    newmaskbest = ~binmask(qc, 1) & ~binmask(qc, 2)

                    if iband == 0:
                        bestmask = np.zeros_like(qc, dtype='uint16')

                    bestmask += (math.pow(2, band) * newmaskbest).astype('uint16')

                    numbad = np.sum(newmaskbad)
                    # fracbad = np.sum(newmaskbad) / float(newmaskbad.size)

                    numgood = np.sum(newmaskgood)
                    # fracgood = np.sum(newmaskgood) / float(newmaskgood.size)
                    assert numgood == qc.size - numbad

                    numbest = np.sum(newmaskbest)
                    # fracbest = np.sum(newmaskbest) / float(newmaskbest.size)

                    metaname = "NUMBAD_%s_%s" % (dayornight, platform)
                    metaname = metaname.upper()
                    # print "metaname", metaname
                    meta[metaname] = str(numbad)

                    metaname = "NUMGOOD_%s_%s" % (dayornight, platform)
                    metaname = metaname.upper()
                    # print "metaname", metaname
                    meta[metaname] = str(numgood)

                    metaname = "NUMBEST_%s_%s" % (dayornight, platform)
                    metaname = metaname.upper()
                    # print "metaname", metaname
                    meta[metaname] = str(numbest)

                    # overpass time
                    hournodatavalue = hourbands[iband].NoDataValue()
                    hour = hourbands[iband].Read()
                    hour = hour[hour != hournodatavalue]
                    hourmean = 0
                    with utils.error_handler("Couldn't compute hour mean for " + fname,
                                             continuable=True):
                        hourmean = hour.mean()

                    metaname = "MEANOVERPASSTIME_%s_%s" % (dayornight, platform)
                    metaname = metaname.upper()
                    meta[metaname] = str(hourmean)

                    tempbands[iband].Process(imgout[band])

                imgout[4].SetGain(1.0)
                imgout[4].Write(bestmask)
                imgout.SetBandName('Temperature Daytime Terra', 1)
                imgout.SetBandName('Temperature Nighttime Terra', 2)
                imgout.SetBandName('Temperature Daytime Aqua', 3)
                imgout.SetBandName('Temperature Nighttime Aqua', 4)
                imgout.SetBandName('Temperature Best Quality', 5)
                del tempbands
                del qcbands
                del hourbands

            ###################################################################
            # OBSERVATION TIME PRODUCT (DAILY)
            if val[0] == "obstime":
                VERSION = "1"
                meta['VERSION'] = VERSION

                if not missingassets:
                    availbands = [0, 1, 2, 3]
                    hoursds = [allsds[2], allsds[6], allsds[14], allsds[18]]
                elif missingassets[0] == 'MYD11A1':
                    availbands = [0, 1]
                    hoursds = [allsds[2], allsds[6]]
                elif missingassets[0] == 'MOD11A1':
                    availbands = [2, 3]
                    hoursds = [allsds[2], allsds[6]]
                else:
                    raise

                hourbands = gippy.GeoImage(hoursds)

                imgout = gippy.GeoImage(fname, hourbands, gippy.GDT_Byte, 4)
                imgout.SetNoData(0)
                imgout.SetGain(0.1)

                # there are four temperature bands
                for iband, band in enumerate(availbands):
                    # get meta name template info
                    basename = hourbands[iband].Basename()
                    platform = self.Asset._sensors[basename[:3]]['description']

                    if basename.find('daytime'):
                        dayornight = 'day'
                    elif basename.find('nighttime'):
                        dayornight = 'night'
                    else:
                        raise Exception('%s appears to be an invalid MODIS temperature project' % basename)

                    hourbands[iband].Process(imgout[band])

                imgout.SetBandName('Observation Time Daytime Terra', 1)
                imgout.SetBandName('Observation Time Nighttime Terra', 2)
                imgout.SetBandName('Observation Time Daytime Aqua', 3)
                imgout.SetBandName('Observation Time Nighttime Aqua', 4)
                del hourbands

            ###################################################################
            # NDVI (8-day) - Terra only
            if val[0] == "ndvi8":
                # NOTE this code is unreachable currently; see _products above.
                VERSION = "1.0"
                meta['VERSION'] = VERSION

                refl = gippy.GeoImage(allsds)
                refl.SetBandName("RED", 1)
                refl.SetBandName("NIR", 2)
                refl.SetNoData(-28762)

                fouts = dict(Indices(refl, {'ndvi': fname}, meta))
                imgout = gippy.GeoImage(fouts['ndvi'])
                del refl

            # TEMPERATURE PRODUCT (8-day) - Terra only

            if val[0] == "temp8td":
                os.symlink(allsds[0], fname)
                imgout = gippy.GeoImage(fname)

            if val[0] == "temp8tn":
                os.symlink(allsds[4], fname)
                imgout = gippy.GeoImage(fname)

            # set metadata
            meta = {k: str(v) for k, v in meta.iteritems()}
            imgout.SetMeta(meta)

            # add product to inventory
            archive_fp = self.archive_temp_path(fname)
            self.AddFile(sensor, key, archive_fp)
            del imgout  # to cover for GDAL's internal problems
            utils.verbose_out(' -> {}: processed in {}'.format(
                os.path.basename(fname), datetime.datetime.now() - start), level=1)
