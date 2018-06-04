import datetime
import re
import os
import subprocess
from zipfile import ZipFile

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
        'srtm': {'description': 'Shuttle Radar Topography Mission'},
    }

    _assets = {
        'SRTMGL1': {
            'pattern': r'^(?P<tile>[NS]\d{2}[WE]\d{3})_2000042_srtm_srtm.tif$',
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

        self.tile = match.group('tile')
        self.date = datetime.datetime(2000, 2, 11)

    @classmethod
    def query_service(cls, asset, tile, date):
        url_base = 'https://e4ftl01.cr.usgs.gov/MEASURES/SRTMGL1.003/2000.02.11/{}.SRTMGL1.hgt.zip'
        if date == datetime.datetime(2000, 2, 11):
            return {
                'url': url_base.format(tile),
                'basename': '{}_2000042_srtm_srtm.tif'.format(tile),
                'download_name': '{}.SRTMGL1.hgt.zip'.format(tile),
            }
        return None

    @classmethod
    def fetch(cls, asset, tile, date):
        qs_rv = cls.query_service(asset, tile, date)
        if qs_rv is None:
            return []
        url = qs_rv.pop('url')
        basename = qs_rv.pop('basename')
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

            zip_file = ZipFile(zip_filename)
            hgt_filename = zip_file.extract(zip_file.filelist[0], dldir)
            tif_filename = os.path.join(dldir, basename)
            subprocess.call(["gdal_translate", "-of", "GTiff", hgt_filename, tif_filename])

            os.rename(tif_filename,
                      os.path.join(stage_dir, os.path.basename(tif_filename)))
            fetched.append(os.path.join(stage_dir, os.path.basename(tif_filename)))
        return fetched


class srtmData(Data):
    Asset = srtmAsset

    _products = {
        'dem': {
            'description': '',
            'assets': ['SRTMGL1'],
        },
    }
