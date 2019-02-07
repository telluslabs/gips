"""
Any detail here is mostly pointless, this is a one-off intended to get CDL tiles

If multitemporal repo and GIPS coexisted we could add a composite step and this
would be potentially generally useful
"""

from __future__ import print_function

import os
import click

from backports import tempfile

from make_global_tiles import make_tileimg

from pdb import set_trace


LOGFILE = "/tmp/output.txt"

PRODUCTFILE = "/export/{asset}_{product}_ks/0/{year}001_{asset}_{product}.tif"

S3LOC = "s3://tellus-s3-vault/product/analysis_tiles/{product}_{window}/{year}/{tileid}.tif"

MASKFILE = "{dirname}/{tileid}_1_1.tif"

GIPS_CMD = "gips_export {asset} -p {product} -r {maskfile} -d {year} "\
"--days {dayrange} -v4 --outdir /export/{asset}_{product}_ks --notld --fetch --overwrite > {logfile}"

AWS_CMD = "aws s3 cp {} {} > {}"

LOCAL_VOLUME = '/tmp'


def temporary_directory():
    """Create temporary directory on local volume"""
    return tempfile.TemporaryDirectory(dir=LOCAL_VOLUME)


@click.command()
@click.option('-a', '--asset', required=True, help='')
@click.option('-p', '--product', required=True, help='')
@click.option('-y', '--years', required=True, help='')
@click.option('-w', '--window', help='')
@click.option('-d', '--dayrange', help='')
def main(asset, product, years, window, dayrange):

	h0 = 519
	v0 = 333

    if asset == "cdl":
    	if window is None:
        	window = "all"
        else:
        	assert window == "all"
        if dayrange is None:
            dayrange = "1,1"
        else:
        	assert dayrange = "1,1"

	years = years.split(',')
	years = [int(y) for y in years]

	for year in years:

		for i in range(51):
			for j in range(21):

				htile = h0 + i
				vtile = v0 + j

				tileid = '{}_{}'.format(htile, vtile)

				with temporary_directory() as tmp_dir:

					print('make_tileimg', tileid)
					make_tileimg(tmp_dir, tileid, '1,1')

					maskfile = MASKFILE.format(dirname=tmp_dir, tileid=tileid)

					# TODO: don't you like how I avoided using subprocess, sh, or commands?
					gips_cmd = GIPS_CMD.format(asset=asset, product=product, maskfile=maskfile,
						year=year, dayrange=dayrange, logfile=LOGFILE)

					print(gips_cmd)
					os.system(gips_cmd)
					print(open(LOGFILE).read())
					os.remove(LOGFILE)

					productfile = PRODUCTFILE.format(asset=asset, product=product, year=year)
					s3loc = S3LOC.format(product=product, window=window, year=year, tileid=tileid)

					aws_cmd = AWS_CMD.format(productfile, s3loc, LOGFILE)
					print(aws_cmd)
					os.system(aws_cmd)
					print(open(LOGFILE).read())
					os.remove(LOGFILE)

					print('removing', productfile)
					os.remove(productfile)

					print('removing', maskfile)
					os.remove(maskfile)


if __name__ == "__main__":
	main()
