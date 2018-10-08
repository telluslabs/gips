#!/usr/bin/env python
################################################################################
#    SMAP: Soil Moisture Active Passive
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

import gippy
from gippy.algorithms import Indices
from gips.data.core import Repository, Asset, Data
from gips.utils import VerboseOut, settings
from gips import utils


class smapRepository(Repository):
    name = 'SMAP'
    description = 'Soil Moisture Active Passive (SMAP)'

    # NASA assets require special authentication
    _manager_url = "https://urs.earthdata.nasa.gov"


class smapAsset(Asset):
    Repository = smapRepository
    _sensors = {'RAD': {'description': 'Soil Moisture Active Passive Radiometer'}}
    _assets = {
        'SM_P_E': {
            'url': 'https://n5eil01u.ecs.nsidc.org/SMAP/SPL3SMP_E.002/',
            'pattern': r'^SMAP\_.{2}\_SM\_P\_E\_.{8}\_.{8}\_.{3}\.h5$',
            'description': 'Passive Enhanced Radiometer Based SM at 9KM',
            'startdate': datetime.date(2015, 3, 31),
            'latency': 3,
        },
        'SM_P': {
            'url': 'https://n5eil01u.ecs.nsidc.org/SMAP/SPL3SMP.005/',
            'pattern': r'^SMAP\_.{2}\_SM\_P\_.{8}\_.{8}\_.{3}\.h5$',
            'description': 'Passive Original Radiometer Based SM at 36KM',
            'startdate': datetime.date(2015, 3, 31),
            'latency': 3,
        },
    }

    def __init__(self, filename):
        """ Inspect a single file and get some metadata """
        super(smapAsset, self).__init__(filename)

        bname = os.path.basename(filename)
        self.asset = (re.search('(?<=^SMAP_L3_)\w*(?=_[0-9]{8})',bname)).group(0)
        date_here = (re.search('[0-9]{8}',bname)).group(0)
        self.date = datetime.datetime.strptime(date_here, "%Y%m%d").date()
        self._version = (re.search('R[0-9]*',bname)).group(0)

    @classmethod
    def query_provider(cls, asset, date):
        """Find out from the SMAP servers what assets are available.

        Uses the given (asset, date) tuple as a search key, andcat
        returns a tuple:  base-filename, url
        """
        year, month, day = date.timetuple()[:3]
        mainurl = "%s/%s.%02d.%02d" % (cls._assets[asset]['url'], str(year), month, day)

        pattern = r'^SMAP\_.{2}\_%s\_%s\_.{6}\_.{3}\.h5$' % (asset, str(year + month + day))
        cpattern = re.compile(pattern)
        err_msg = "Error downloading: " + mainurl
        with utils.error_handler(err_msg):
            response = cls.Repository.managed_request(mainurl, verbosity=2)
            if response is None:
                return None, None

        for item in response.readlines():
            # screen-scrape the content of the page and extract the full name of the needed file
            # (this step is needed because part of the filename, the creation timestamp, is
            # effectively random).
            if cpattern.search(item):
                if 'xml' in item:
                    continue
                basename = cpattern.findall(item)[0]
                url = ''.join([mainurl, '/', basename])
                return basename, url
        utils.verbose_out('Unable to find remote match for '
                          '{} at {}'.format(pattern, mainurl), 4)
        return None, None

    @classmethod
    def query_service(cls, asset, date):
        """Query the data provider for files matching the arguments.

        """
        if not cls.available(asset, date):
            return None
        utils.verbose_out('querying ATD {} {}'.format(asset, date), 5)
        bn, url = cls.query_provider(asset, date)
        utils.verbose_out('queried ATD {} {}, found {} at {}'.format(
            asset, date, bn, url), 5)
        if (bn, url) == (None, None):
            return None
        return {'basename': bn, 'url': url}

    @classmethod
    def fetch(cls, asset, tile, date):
        qs_rv = cls.query_service(asset, tile, date)
        if qs_rv is None:
            return []
        basename, url = qs_rv['basename'], qs_rv['url']
        with utils.error_handler(
                "Asset fetch error ({})".format(url), continuable=True):
            response = cls.Repository.managed_request(url)
            if response is None:
                return []
            outpath = os.path.join(cls.Repository.path('stage'), basename)
            with open(outpath, 'wb') as fd:
                fd.write(response.read())
            utils.verbose_out('Retrieved ' + basename, 2)
            return [outpath]
        return []

class smapData(Data):
    """ A tile of data (all assets and products) """
    name = 'SMAP'
    version = '1.0.0'
    Asset = smapAsset

    _geotransform = (0.0, 1.0, 0.0, 0.0, 0.0, 1.0)
    _projection = 'GEOGCS["WGS 84",DATUM["WGS_1984",SPHEROID["WGS 84",6378137,298.257223563,AUTHORITY["EPSG","7030"]],' \
                  'AUTHORITY["EPSG","6326"]],PRIMEM["Greenwich",0,AUTHORITY["EPSG","8901"]],UNIT["degree",' \
                  '0.0174532925199433,AUTHORITY["EPSG","9122"]],AUTHORITY["EPSG","4326"]]'


    _products = {
        'smp': {
            'description': 'SMAP SM AM Acquisiton posted on native grid ',
            # the list of asset types associated with this product
            'assets': ['SM_P'],  # , 'MYD08'],
        },
        'smpe': {
            'description': 'SMAP SM AM Acquisiton posted on enhanced 9km grid',
            # the list of asset types associated with this product
            'assets': ['SM_P_E'],  # , 'MYD08'],
        }
    }

    @Data.proc_temp_dir_manager
    def process(self, *args, **kwargs):
        """Produce requested products."""