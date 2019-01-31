from __future__ import print_function

import os
import click

from make_global_tiles import make_tileimg

from pdb import set_trace


TMPFILE = "/tmp/output.txt"

PRODUCTFILE = "/export/{asset}_{product}_ks/0/{year}001_{asset}_{product}.tif"

S3LOC = "s3://tellus-s3-vault/product/analysis_tiles/cdl_all/{}/{}.tif"

MASKFILE = "/export/mask_tiles/{}_1_1.tif"

GIPS_CMD = "gips_export {asset} -p {product} -r {maskfile} -d {year} "\
"--days 1,1 -v4 --outdir /export/{asset}_{product}_ks --notld --fetch --overwrite > {tmpfile}"

AWS_CMD = "aws s3 cp {} {} > {}"

@click.command()
@click.option('-a', '--asset', help='')
@click.option('-p', '--product', help='')
@click.option('-y', '--year', help='')
def main(asset, product, year):

	h0 = 519
	v0 = 333

	for i in range(51):
		for j in range(21):

			htile = h0 + i
			vtile = v0 + j

			tileid = '{}_{}'.format(htile, vtile)

			print('make_tileimg', tileid)
			make_tileimg('/export/mask_tiles/', tileid, '1,1')

			maskfile = MASKFILE.format(tileid)

			gips_cmd = GIPS_CMD.format(asset=asset, product=product, maskfile=maskfile, year=year, tmpfile=TMPFILE)
			print(gips_cmd)
			os.system(gips_cmd)
			print(open(TMPFILE).read())

			productfile = PRODUCTFILE.format(asset=asset, product=product, year=year)
			s3loc = S3LOC.format(year, tileid)

			aws_cmd = AWS_CMD.format(productfile, s3loc, TMPFILE)

			print(aws_cmd)
			os.system(aws_cmd)
			print(open(TMPFILE).read())

			print('removing', productfile)
			os.remove(productfile)

			print('removing', maskfile)
			os.remove(maskfile)

	os.remove(TMPFILE)


if __name__ == "__main__":
	main()
