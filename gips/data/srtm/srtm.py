import datetime
import re
import os
import subprocess

from gips.data.core import Repository, Asset, Data
from gips import utils
from gips.utils import settings


class srtmRepository(Repository):
    name = 'SRTM'
    description = 'SRTM elevation data'
    _tile_attribute = 'id'


class srtmAsset(Asset):
    Repository = srtmRepository

    _sensors = {
        'srtm': {'description': 'Shuttle Radar Topography Mission'},
    }

    _assets = {
        'SRTMGL1': {
            'pattern': r'^(?P<tile>[NS]\d{2}[WE]\d{3})\.SRTMGL1\.hgt\.zip$',
            'startdate': datetime.date(2000, 2, 11),
            'latency': 0,
        },
    }

    def __init__(self, filename):
        super(srtmAsset, self).__init__(filename)

        fname = os.path.basename(filename)
        pattern_re = re.compile(self._assets['SRTMGL1']['pattern'])
        match = pattern_re.match(fname)

        if not match:
            msg = "No matching SRTM asset type for '{}'".format(fname)
            raise RuntimeError(msg, filename)

        self.asset = 'SRTMGL1'
        self.tile = match.group('tile')
        self.date = datetime.datetime(2000, 2, 11)

    @classmethod
    def query_service(cls, asset, tile, date):
        url_base = 'https://e4ftl01.cr.usgs.gov/MEASURES/SRTMGL1.003/2000.02.11/{}.SRTMGL1.hgt.zip'
        if date == datetime.datetime(2000, 2, 11):
            return {
                'url': url_base.format(tile),
                'basename': '{}.SRTMGL1.hgt.zip'.format(tile),
                'download_name': '{}.SRTMGL1.hgt.zip'.format(tile),
            }
        return None

    @classmethod
    def fetch(cls, asset, tile, date):
        qs_rv = cls.query_service(asset, tile, date)
        if qs_rv is None:
            return []
        url = qs_rv.pop('url')
        download_name = qs_rv.pop('download_name')

        stage_dir = cls.Repository.path('stage')
        fetched = []

        with utils.make_temp_dir(prefix='dwnld', dir=stage_dir) as dldir:
            zip_filename = os.path.join(dldir, download_name)
            subprocess.call([
                "wget",
                "--no-verbose",
                "--user", settings().REPOS['srtm']['username'],
                "--password", settings().REPOS['srtm']['password'],
                "--output-document", zip_filename,
                url
            ])
            os.rename(zip_filename,
                      os.path.join(stage_dir, os.path.basename(zip_filename)))
            fetched.append(os.path.join(stage_dir, os.path.basename(zip_filename)))
        return fetched


class srtmData(Data):
    Asset = srtmAsset

    _products = {
        'gl1': {
            'description': '',
            'assets': ['SRTMGL1'],
        },
    }

    @Data.proc_temp_dir_manager
    def process(self, *args, **kwargs):
        sensor = 'srtm'
        fname = self.temp_product_filename(sensor, 'gl1')
        os.symlink(self.assets['SRTMGL1'].datafiles()[0], fname)
        self.archive_temp_path(fname)
