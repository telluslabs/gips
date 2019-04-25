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
# from gips.parsers import GIPSParser
from gips.core import SpatialExtent, TemporalExtent
from gips.utils import Colors, VerboseOut, import_data_class
from gips import utils
from gips.inventory import DataInventory, ProjectInventory
from gips.inventory import orm

from gips.scripts.export import run_export

import click
import glob
import shutil
import ogr

from backports import tempfile
import boto3
import zipfile


class Args(object):
    pass


@click.command()
@click.option('--name', '-n', type=str, help='Job name')
@click.option('--jobid', '-j', type=int, help='Job index')
def main(name, jobid):

    title = Colors.BOLD + 'GIPS Data Export (v%s)' % __version__ + Colors.OFF
    print(title)

    args = Args()
    args.command = "hls"
    args.products = ['ndvi', 'lswi', 'brgt', 'cmask']
    args.res = [30., 30.]
    args.stop_on_error = "False"
    args.suffix = ""
    args.format = "GTiff"
    args.verbose = 4
    args.interpolation = 0
    args.ptile = 0
    args.pcov = 0
    args.pclouds = 100.
    args.chunksize = 128.0
    args.numprocs = 1
    args.notld = True
    args.fetch = True
    args.crop = False
    args.overwrite = False
    args.alltouch = False
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

        args.site = "s3://tl-octopus/user/gips/vector/{}.zip".format(name)

        # get the number of features TLDR
        S3 = boto3.resource('s3')
        s3path = args.site.lstrip('s3://')
        filename = s3path.split('/')[-1]
        s3_bucket = s3path.split('/')[0]
        s3_key = "/".join(s3path.split('/')[1:])
        zippath = os.path.join(tmpdir, filename)
        S3.Bucket(s3_bucket).download_file(s3_key, zippath)
        zipped = zipfile.ZipFile(zippath)
        zipped.extractall(tmpdir)
        shppath = os.path.splitext(zippath)[0] + '.shp'
        driver = ogr.GetDriverByName('ESRI Shapefile')
        source = driver.Open(shppath, 0)
        layer = source.GetLayer()

        nfeatures = layer.GetFeatureCount()
        source.Destroy()

        doy = jobid

        for fid in range(nfeatures):

            print(fid)

            args.site = "s3://tl-octopus/user/gips/vector/{}.zip".format(name)
            args.outdir = "s3://tl-octopus/user/gips/export/{}/{}_{}_{}".format(name, doy, fid)

            args.dates = "2017-{}".format(str(doy+1).zfill(3))
            args.where = "FID={}".format(fid)

            print(args.dates)
            print(args.where)

            run_export(args)

            print('done export')

        print('cleaning up')

        items = glob.glob('/archive/hls/tiles/*')
        for item in items:
            shutil.rmtree(item)

        utils.gips_exit()


if __name__ == "__main__":
    main()
