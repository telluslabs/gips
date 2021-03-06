from __future__ import print_function

import os
from copy import deepcopy

import click
import boto3
import geopandas as gpd

from backports import tempfile
# from tempfile import TemporaryDirectory

from make_global_tiles import make_tileimg

from pdb import set_trace


TMPFILE = "/tmp/output.txt"

PRODUCTFILE = "/export/{asset}_{product}/0/{year}001_{asset}_{product}.tif"


S3_BUCKET = "tellus-s3-vault"
S3LOC = "s3://tellus-s3-vault/product/analysis_tiles/cdl_all/{}/{}.tif"

MASKFILE = "{}/{}_1_1.tif"

GIPS_CMD = "gips_export {asset} -p {product} -r {maskfile} -d {year} "\
"--days 1,1 -v4 --outdir /export/{asset}_{product} --notld --fetch --overwrite > {tmpfile}"

AWS_CMD = "aws s3 cp {} {} > {}"

AWS_LS_CMD = "aws s3 ls {} > {}"

LOCAL_VOLUME = '/tmp'



def get_tileids(shpfile):

    df = gpd.read_file(shpfile)

    tileids =  [str(t) for t in df['tileid'].tolist()]

    print(len(tileids))

    for tileid in deepcopy(tileids):
        htile, vtile = tileid.split('_')
        for i in [-1,0,1]:
            for j in [-1,0,1]:
                newtileid = "{}_{}".format(int(htile)+i, int(vtile)+j)
                if newtileid not in tileids:
                    tileids.append(newtileid)

    print(len(tileids))

    return sorted(tileids)


def run(tileids, year):

    asset = "cdl"
    product = "cdl"

    for tileid in tileids:

        htile, vtile = tileid.split('_')

        with tempfile.TemporaryDirectory() as tmp_dir:

            productfile = PRODUCTFILE.format(asset=asset, product=product, year=year)
            s3loc = S3LOC.format(year, tileid)

            aws_cmd = AWS_LS_CMD.format(s3loc, TMPFILE)

            print(aws_cmd)
            os.system(aws_cmd)

            result = open(TMPFILE).read()

            if tileid+'.tif' in result:
                print('have', tileid)
                continue

            print('make_tileimg', tileid)
            make_tileimg(tmp_dir, tileid, '1,1')

            maskfile = MASKFILE.format(tmp_dir, tileid)

            gips_cmd = GIPS_CMD.format(asset=asset, product=product, maskfile=maskfile, year=year, tmpfile=TMPFILE)
            print(gips_cmd)
            os.system(gips_cmd)
            print(open(TMPFILE).read())

            aws_cmd = AWS_CMD.format(productfile, s3loc, TMPFILE)

            print(aws_cmd)
            os.system(aws_cmd)
            print(open(TMPFILE).read())

            print('removing', productfile)
            os.remove(productfile)

            print('removing', maskfile)
            os.remove(maskfile)


@click.command()
@click.option('--shapefile', '-s')
@click.option('--years', '-y')
def main(shapefile, years):

    # e.g. python cdl_tiles.py -s /export/kansas/kansas_tiles.shp -y 2008,2009,2010,2011,2012,2013,2014,2015,2016,2017,2018

    tileids = get_tileids(shapefile)
    years = [int(y) for y in years.split(',')]

    for year in years:
        run(tileids, year)


if __name__ == "__main__":
    main()
