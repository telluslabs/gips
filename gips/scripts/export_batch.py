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

from __future__ import print_function

import os

from gips import __version__
from gips.core import SpatialExtent, TemporalExtent
from gips.utils import Colors, VerboseOut, import_data_class
from gips import utils
from gips.inventory import DataInventory, ProjectInventory
from gips.inventory import orm

from gips.scripts.export import run_export, get_s3_shppath

import click
import glob
import shutil
import ogr

from backports import tempfile
import boto3
from botocore.exceptions import ClientError
import zipfile


class Args(object):
    pass


BUCKET = "tl-octopus"


def s3_head(bucket, key):
    s3 = boto3.client('s3')
    try:
        return s3.head_object(Bucket=bucket, Key=key)
    except ClientError as e:
        if e.response['ResponseMetadata']['HTTPStatusCode'] == 404:
            return None
        else:
            raise e


def s3_exists(bucket, key):
    return s3_head(bucket, key) is not None


@click.command()
@click.option('--jobid', '-j', type=int, help='Job index')
def main(jobid):

    title = Colors.BOLD + 'GIPS Data Export (v%s)' % __version__ + Colors.OFF
    print(title)

    print('cleaning up')
    assetdirs = ['hls', 'modis']
    subdirs = ['tiles', 'stage']
    for assetdir in assetdirs:
        for subdir in subdirs:
            path = os.path.join('/archive', assetdir, subdir)
            for file_or_dir in os.listdir(path):
                shutil.rmtree(os.path.join(path, file_or_dir))


    args = Args()
    args.stop_on_error = "False"
    args.suffix = ""
    args.format = "GTiff"
    args.verbose = 5
    args.ptile = 0
    args.pcov = 0
    args.pclouds = 100.
    args.chunksize = 128.0
    args.numprocs = 1
    args.notld = True
    args.fetch = True
    args.crop = False
    args.overwrite = True
    args.alltouch = True
    args.tree = False
    args.size = False
    args.update = False
    args.days = None
    args.rastermask = None
    args.tiles = None
    args.batchout = None
    args.sensors = None
    args.key = ''

    with tempfile.TemporaryDirectory() as tmpdir:

        # get name, year, and asset

        confpath = os.path.join(tmpdir, 'config')
        S3 = boto3.resource('s3')
        S3.Bucket(BUCKET).download_file('user/gips/config', confpath)

        # get config parameters
        config = eval(open(confpath).read())
        args.command = config['source']
        args.products = config['products']
        args.res = [config['res'], config['res']]
        args.interpolation = config['interp']
        year = config['year']
        s3shpfile = config['shapefile']
        try:
            name = config['name']
        except:
            name = s3shpfile.split('/')[-1].split('.zip')[0]

        shppath = get_s3_shppath(s3shpfile, tmpdir)
        driver = ogr.GetDriverByName('ESRI Shapefile')
        source = driver.Open(shppath, 0)
        layer = source.GetLayer()

        nfeatures = layer.GetFeatureCount()
        source.Destroy()

        doy = jobid

        for fid in range(nfeatures):
            print(fid)

            args.site = s3shpfile

            key = "user/gips/export/{}/{}_{}_{}_{}_{}".format(
                name, name, args.command, year, doy, fid)

            args.outdir = "s3://{}/{}".format(BUCKET, key)

            if s3_exists(BUCKET, key + '.zip'):
                print('skipping', BUCKET, key)
                continue


            args.dates = "{}-{}".format(year, str(doy+1).zfill(3))
            args.where = "FID={}".format(fid)
            print('outdir', args.outdir)
            print(args.dates)
            print(args.where)

            run_export(args)
            print('done export')

        print('cleaning up')
        items = glob.glob('/archive/{}/tiles/*'.format(args.command))
        for item in items:
            shutil.rmtree(item)

        utils.gips_exit()


if __name__ == "__main__":
    main()
