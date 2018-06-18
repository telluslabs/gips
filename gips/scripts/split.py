#!/usr/bin/env python

import os

import gippy

import numpy as np
from osgeo import gdal

from gips.parsers import GIPSParser
from gips.inventory import ProjectInventory
from gips.utils import Colors, VerboseOut, basename
from gips import utils

from pdb import set_trace


def read_raster(infile):
    fp = gdal.Open(infile)
    proj = fp.GetProjection()
    geo = fp.GetGeoTransform()
    data = fp.ReadAsArray()
    ny, nx = (fp.RasterYSize, fp.RasterXSize)
    return data, proj, geo


def write_raster(outfile, outdata, proj, geo, nodata, dtype):
    driver = gdal.GetDriverByName('GTiff')
    ny, nx = outdata.shape
    tfh = driver.Create(outfile, nx, ny, 1, dtype, [])
    tfh.SetProjection(proj)
    tfh.SetGeoTransform(geo)
    tband = tfh.GetRasterBand(1)
    tband.SetNoDataValue(nodata)
    tband.WriteArray(outdata)
    tfh = None


__version__ = '0.1.0'

def main():
    title = Colors.BOLD + 'GIPS Project Raster Splitter (v%s)' % __version__ + Colors.OFF

    parser = GIPSParser(datasources=False, description=title)
    parser.add_projdir_parser()

    group = parser.add_argument_group('splitting options')
    group.add_argument('--prodname', help='Pattern of the target images')
    args = parser.parse_args()

    utils.gips_script_setup(None, args.stop_on_error)

    with utils.error_handler('Splitting error'):

        VerboseOut(title)
        for projdir in args.projdir:

            inv = ProjectInventory(projdir, args.products)
            for date in inv.dates:
                VerboseOut('Splitting files from %s' % date)

                for p in inv.products(date):

                    VerboseOut(p)

                    img = inv[date].open(p)
                    fname = img.Filename()

                    if not fname.endswith("{}.tif".format(args.prodname)):
                        continue

                    bnames = img.BandNames()

                    imgdata, proj, geo = read_raster(fname)

                    for i,bname in enumerate(bnames):

                        fnameout = "{}_{}.tif".format(
                            os.path.splitext(fname)[0], bname)

                        #data = img[i].Read()

                        try:
                            data = imgdata[i,:,:].squeeze()
                        except:
                            data = imgdata[:,:]

                        nodata = -32768
                        scale = 10000
                        data = data.astype('int16')
                        dtype = gdal.GDT_Int16

                        write_raster(fnameout, data, proj, geo, nodata, dtype)

                        #imgout = gippy.GeoImage(fnameout, img, gippy.GDT_Int16, 1)
                        #imgout.SetNoData(-32768)
                        #imgout.SetOffset(0.0)
                        #imgout.SetGain(0.0001)
                        #imgout[0].Write(data)
                        #imgout.SetBandName(bname, 1)
                        #imgout = None

                    img = None

    utils.gips_exit()


if __name__ == "__main__":
    main()

