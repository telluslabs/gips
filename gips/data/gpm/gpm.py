#!/usr/bin/env python
################################################################################
#    GPM: Global Precipitation Measurement Mission
#
#    AUTHOR: Subit Chakrabarti
#    EMAIL:  chakrabarti.subit@gmail.com
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
import ftplib
import gippy
from gippy.algorithms import Indices
from gips.data.core import Repository, Asset, Data
from gips.utils import VerboseOut, settings
from gips import utils


class gpmRepository(Repository):
    name = 'GPM'
    description = 'Global Precipitation Measurement Mission (GPM)'
    # NASA assets require special authentication
    _host = "arthurhou.pps.eosdis.nasa.gov"
    _tile_attribute = 'tileid'

class gpmAsset(Asset):
    Repository = gpmRepository
    _sensors = {'GPM': {'description': 'Integrated Multi-satellite Retrievals for GPM'}}
    _assets = {
        'IMERG-DAY-FINAL': {
                        'host': "arthurhou.pps.eosdis.nasa.gov",
            'pattern': r'3B-DAY-GIS\.MS\.MRG\.3IMERG\..{8}-S.{6}-E.{6}\..{4}\..{4}\.tif',
            'description': 'Daily Precipitation Rate (mm/hr) at 0.1 degrees - Research Run using the IMERG Algorithm'
                           'developed for the GPM constellation',
            'path': '/gpmdata/',
            'startdate': datetime.date(2014, 3, 12),
            'latency': 1,
        },
        'IMERG-DAY-LATE': {
            'host': "jsimpson.pps.eosdis.nasa.gov",
            'pattern': r'3B-HHR-L\.MS\.MRG\.3IMERG\..{8}-S.{6}-E.{6}\..{4}\..{4}\.1day.tif',
            'description': 'Daily Accumulated Precipitation (in mm) at 23:59 UTC at 0.1 degrees - Production Run '
                           'using the IMERG Algorithm developed for the GPM constellation',
            'path': '/NRTPUB/imerg/gis/',
            'startdate': datetime.date(2014, 3, 12),
            'latency': 1,
        },
        'IMERG-DAY-EARLY': {
            'host': "jsimpson.pps.eosdis.nasa.gov",
            'pattern': r'3B-HHR-L\.MS\.MRG\.3IMERG\..{8}-S.{6}-E.{6}\..{4}\..{4}\.1day.tif',
            'description': 'Daily Accumulated Precipitation (in mm) at 06:59 UTC 0.1 degrees - Production Run '
                           'using the IMERG Algorithm developed for the GPM constellation',
            'path': '/NRTPUB/imerg/gis/',
            'startdate': datetime.date(2014, 3, 12),
            'latency': 1,
        },
        'IMERG-DAY-MID': {
            'host': "jsimpson.pps.eosdis.nasa.gov",
            'pattern': r'3B-HHR-L\.MS\.MRG\.3IMERG\..{8}-S.{6}-E.{6}\..{4}\..{4}\.1day.tif',
            'description': 'Daily Accumulated Precipitation (in mm) at 14:59 0.1 degrees - Production Run '
                           'using the IMERG Algorithm developed for the GPM constellation',
            'path': '/NRTPUB/imerg/gis/',
            'startdate': datetime.date(2014, 3, 12),
            'latency': 1,
        },
        '3B42-DAY-LATE': {
            'host': "trmmopen.pps.eosdis.nasa.gov",
            'pattern': r'3B42RT\..{10}[\.7]*\.1day.tif',
            'description': 'Daily Accumulated Precipitation (in mm) at 0.25 degrees - Production Run using the '
                           '3B42 Algorithm developed for the TRMM constellation',
            'path': '/pub/gis/',
            'startdate': datetime.date(2000, 3, 2),
            'latency': 1,
        },
    }

    def __init__(self, filename):
        """ Inspect a single file and get some metadata """
        super(gpmAsset, self).__init__(filename)

        bname = os.path.basename(filename)
        try:
            indicator = (re.search('(?<=3B-)\w*(?=-{1})', bname)).group(0)
        except AttributeError:
            indicator = (re.search('(?<=3B)\w*(?=\.{1})', bname)).group(0)
            pass

        if indicator == 'DAY':
            self.asset = 'IMERG-DAY-FINAL'
        elif indicator == 'HHR':
            self.asset = 'IMERG-DAY-LATE'
        elif indicator == '42RT':
            self.asset = '3B42-DAY-LATE'

        # Will break in the next millenium
        date_here = (re.search('2[0-9]{7}', bname)).group(0)
        self.date = datetime.datetime.strptime(date_here, "%Y%m%d").date()
        try:
            self._version = (re.search('V[0-9A-Z]*', bname)).group(0)
        except AttributeError:
            self._version = 7 #hard code for 3B42 products
            pass

        self.tile = 'h01v01'

    @classmethod
    def ftp_connect(cls, asset, date):
        """Connect to an FTP server and chdir according to the args.
        Returns the ftplib connection object."""
        utils.verbose_out('Connecting to {}'.format(cls._assets[asset]['host']), 5)
        if asset == 'IMERG-DAY-FINAL':
            conn = ftplib.FTP(cls._assets[asset]['host'])
            conn.login('subitc@ufl.edu', 'subitc@ufl.edu')
            conn.set_pasv(True)
            working_directory = os.path.join(cls._assets[asset]['path'], date.strftime('%Y'), date.strftime('%m'),
                                             date.strftime('%d'), 'gis')
        elif asset == 'IMERG-DAY-LATE' or asset == 'IMERG-DAY-EARLY' or asset == 'IMERG-DAY-MID':
            conn = ftplib.FTP(cls._assets[asset]['host'])
            conn.login('subitc@ufl.edu', 'subitc@ufl.edu')
            conn.set_pasv(True)
            working_directory = os.path.join(cls._assets[asset]['path'], date.strftime('%Y'), date.strftime('%m'))

        elif asset == '3B42-DAY-LATE':
            conn = ftplib.FTP(cls._assets[asset]['host'])
            conn.login()
            conn.set_pasv(True)
            working_directory = os.path.join(cls._assets[asset]['path'], date.strftime('%Y%m'))

        utils.verbose_out('Changing to {}'.format(working_directory), 5)
        conn.cwd(working_directory)
        return conn

    @classmethod
    def query_provider(cls, asset, tile, date):
        """Determine availability of data for the given (asset, tile, date).

        Re-use the given ftp connection if possible; Returns (basename,
        None) on success; (None, None) otherwise."""
        if asset not in cls._assets:
            raise ValueError('{} has no defined asset for {}'.format(cls.Repository.name, asset))
        conn = cls.ftp_connect(asset, date)
        # get the list of filenames for the year, filter down to the specific date
        filenames = [fn for fn in conn.nlst() if date.strftime('%Y%m%d') in fn]
        conn.quit()
        if 0 == len(filenames):
            return None, None
        # choose the one that has the most favorable stability & version values (usually only one)
        compiled_pattern = re.compile(cls._assets[asset]['pattern'])
        for filename in filenames:
            if compiled_pattern.search(filename):
                if asset == 'IMERG-DAY-FINAL':
                    return filename, None
                elif asset == 'IMERG-DAY-LATE':
                    end_timestamp = int(re.search(r'(?<=E)[0-9]{6}', filename).group(0))
                    if end_timestamp > 230000:
                        return filename, None
                    else:
                        continue
                elif asset == 'IMERG-DAY-EARLY':
                    end_timestamp = int(re.search(r'(?<=E)[0-9]{6}', filename).group(0))
                    if end_timestamp == 65959:
                        return filename, None
                    else:
                        continue
                elif asset == 'IMERG-DAY-MID':
                    end_timestamp = int(re.search(r'(?<=E)[0-9]{6}', filename).group(0))
                    if end_timestamp == 145959:
                        return filename, None
                    else:
                        continue
                elif asset == '3B42-DAY-LATE':
                    end_timestamp = int(re.search(r'[0-9]{2}(?=\..)', filename).group(0))
                    if end_timestamp == 21:
                        return filename, None
                    else:
                        continue
        return None, None


    @classmethod
    def fetch(cls, asset, tile, date):
        utils.verbose_out('%s: fetch tile %s for %s' % (asset, tile, date), 3)
        qs_rv = cls.query_service(asset, tile, date)
        if qs_rv is None:
            return []
        asset_fn = qs_rv['basename']
        with utils.error_handler("Error downloading from " + cls._assets[asset]['host'], continuable=True):
            ftp = cls.ftp_connect(asset, date)  # starts chdir'd to the right directory
            stage_dir_fp = cls.Repository.path('stage')
            stage_fp = os.path.join(stage_dir_fp, asset_fn)
            with utils.make_temp_dir(prefix='fetchtmp', dir=stage_dir_fp) as td_name:
                temp_fp = os.path.join(td_name, asset_fn)
                utils.verbose_out("Downloading " + asset_fn, 2)
                with open(temp_fp, "wb") as temp_fo:
                    ftp.retrbinary('RETR ' + asset_fn, temp_fo.write)
                ftp.quit()
                os.rename(temp_fp, stage_fp)
            return [stage_fp]
        return []

class gpmData(Data):
    """ A tile of data (all assets and products) """
    name = 'GPM'
    version = '1.0.0'
    Asset = gpmAsset

    _projection = 'GEOGCS["WGS 84",DATUM["WGS_1984",SPHEROID["WGS 84",6378137,298.2572326660159,' \
                  'AUTHORITY["EPSG","7030"]], AUTHORITY["EPSG","6326"]],PRIMEM["Greenwich",0],' \
                  'UNIT["degree",0.0174532925199433],AUTHORITY["EPSG","4326"]]'

    _products = {
        'pratefinal': {
            'description': 'Final Precipitation Rate Averaged over 1 Day in mm/hr',
            # the list of asset types associated with this product
            'assets': ['IMERG-DAY-FINAL'],
            'startdate': datetime.date(2014, 3, 12),
            'sensor': 'GPM',
            '_geotransform': (-179.9499969, 0.10000000149011612, 0.0, 89.9499969, 0.0, -0.10000000149011612),
        },
        'paccnrtgpmlate': {
            'description': 'NRT Precipitation Accumulated over 1 Day ending at 23:59 UTC in mm - GPM (and friends) Archive',
            # the list of asset types associated with this product
            'assets': ['IMERG-DAY-LATE'],
            'startdate': datetime.date(2014, 3, 12),
            'sensor': 'GPM',
            '_geotransform': (-179.9499969, 0.10000000149011612, 0.0, 89.9499969, 0.0, -0.10000000149011612),
        },
        'paccnrtgpmmid': {
            'description': 'NRT Precipitation Accumulated over 1 Day ending at 14:59 UTC in mm - GPM (and friends) Archive',
            # the list of asset types associated with this product
            'assets': ['IMERG-DAY-MID'],
            'startdate': datetime.date(2014, 3, 12),
            'sensor': 'GPM',
            '_geotransform': (-179.9499969, 0.10000000149011612, 0.0, 89.9499969, 0.0, -0.10000000149011612),
        },
        'paccnrtgpmearly': {
            'description': 'NRT Precipitation Accumulated over 1 Day ending at 06:59 UTC in mm - GPM (and friends) Archive',
            # the list of asset types associated with this product
            'assets': ['IMERG-DAY-EARLY'],
            'startdate': datetime.date(2014, 3, 12),
            'sensor': 'GPM',
            '_geotransform': (-179.9499969, 0.10000000149011612, 0.0, 89.9499969, 0.0, -0.10000000149011612),
        },
        'paccnrttrmm': {
            'description': 'NRT Precipitation Accumulated over 1 Day in mm - TRMM (and friends) Archive',
            # the list of asset types associated with this product
            'assets': ['3B42-DAY-LATE'],
            'startdate': datetime.date(2000, 3, 1),
            'sensor': 'GPM',
            '_geotransform': (-179.875, 0.25, 0.0, 59.875, 0.0, -0.25),
        },
    }

    def asset_check(self, prod_type):
        """Is an asset available for the current scene and product?

        Returns the last found asset, or else None, its version, the
        complete lists of missing and available assets, and lastly, an array
        of pseudo-filepath strings suitable for consumption by gdal/gippy.
        """
        # return values
        asset = None
        missingassets = []
        availassets = []
        allsds = []

        for asset in self._products[prod_type]['assets']:
            # many asset types won't be found for the current scene
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

        return asset, missingassets, availassets, allsds

    @Data.proc_temp_dir_manager
    def process(self, *args, **kwargs):
        """Produce requested products."""
        products = super(gpmData, self).process(*args, **kwargs)
        if len(products) == 0:
            return
        # example products.requested:
        # {'temp8tn': ['temp8tn'], 'clouds': ['clouds'], . . . }
        # key is only used once far below, and val is only used for val[0].
        for key, val in products.requested.items():
            start = datetime.datetime.now()
            prod_type = val[0]
            asset, missingassets, availassets, allsds = \
                self.asset_check(prod_type)

            if not availassets:
                # some products aren't available for every day but this is trying every day
                VerboseOut('There are no available assets (%s) on %s for tile %s'
                           % (str(missingassets), str(self.date), str(self.id),), 5)
                continue

            sensor = self._products[prod_type]['sensor']
            fname = self.temp_product_filename(sensor, prod_type)  # moved to archive at end of loop

            img = gippy.GeoImage(allsds)

            imgdata = img.Read()
            imgout = gippy.GeoImage(fname, img.XSize(), img.YSize(), 1, gippy.GDT_Float32)
            del img
            imgout.SetNoData(29999.0)
            imgout.SetOffset(0.0)
            imgout.SetGain(0.1)
            imgout.SetBandName('PrecipitationRate', 1)
            imgout.SetProjection(self._projection)
            imgout.SetAffine(np.array(self._products[prod_type]['_geotransform']))
            imgout[0].Write(imgdata)
            # add product to inventory
            archive_fp = self.archive_temp_path(fname)
            self.AddFile(sensor, key, archive_fp)
            del imgout  # to cover for GDAL's internal problems
            utils.verbose_out(' -> {}: processed in {}'.format(
                os.path.basename(fname), datetime.datetime.now() - start), level=1)