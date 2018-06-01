import datetime
import re
import os

from gips.data.core import Repository, Asset, Data
from gips import utils
from gips.utils import settings

import homura


class srtmRepository(Repository):
    name = 'SRTM'
    description = 'SRTM elevation data'
    _tile_attribute = 'id'


class srtmAsset(Asset):
    Repository = srtmRepository

    _sensors = {
        'srtm': {'description': ''},
    }

    _assets = {
        'srtm': {
            'pattern': r'^n(?P<north>\d{2})_w(?P<west>\d{3})_1arc_v3_bil.zip$',
            'startdate': datetime.date(2000, 2, 1),
            'latency': 0,
        },
    }

    def __init__(self, filename):
        super(srtmAsset, self).__init__(filename)

        fname = os.path.basename(filename)
        pattern_re = re.compile(self._assets['srtm']['pattern'])
        match = pattern_re.match(fname)

        if not match:
            msg = "No matching SRTM asset type for '{}'".format(fname)
            raise RuntimeError(msg, filename)

        self.tile = "N{}W{}".format(match.group('north'), match.group('west'))

    @classmethod
    def ee_login(cls):
        if not hasattr(cls, '_ee_key'):
            username = settings().REPOS['srtm']['username']
            password = settings().REPOS['srtm']['password']
            from usgs import api
            cls._ee_key = api.login(username, password)['data']
        return cls._ee_key

    @classmethod
    def query_service(cls, asset, tile, date):
        utils.verbose_out("Querying tile %s" % tile, 3)

        api_key = cls.ee_login()
        print api_key
        from usgs import api
        response = api.search(
            'SRTM_V3_SRTMGL1', 'EE',
            api_key=api_key
        )['data']

        result = [r for r in response if r['displayId'].split('.')[0] == tile]
        if len(result) > 0:
            return {
                'display_id': result[0]['displayId'],
                'download_url': result[0]['downloadUrl'],
            }
        return None

    @classmethod
    def fetch(cls, asset, tile, date):
        print "FETCHING"
        qs_rv = cls.query_service(asset, tile, date)
        if qs_rv is None:
            return []
        url = qs_rv.pop('download_url')

        stage_dir = cls.Repository.path('stage')

        with utils.make_temp_dir(prefix='dwnld', dir=stage_dir) as dldir:
            homura.download(url, dldir)
            granules = os.listdir(dldir)
            if len(granules) == 0:
                raise Exception("Download didn't seem to"
                                " produce a file: {}".format(str(granules)))
            os.rename(os.path.join(dldir, granules[0]),
                      os.path.join(stage_dir, granules[0]))


class srtmData(Data):
    Asset = srtmAsset

    _products = {
        'srtm': {
            'description': '',
            'assets': ['srtm'],
        },
    }
