#!/usr/bin/env python

import os

import gippy

import numpy as np
from osgeo import gdal

from gips.parsers import GIPSParser
from gips.inventory import ProjectInventory
from gips.utils import Colors, VerboseOut, basename
from gips import utils


def read_raster(infile):
    fp = gdal.Open(infile)
    proj = fp.GetProjection()
    geo = fp.GetGeoTransform()
    data = fp.ReadAsArray()
    band = fp.GetRasterBand(1)
    nodata = band.GetNoDataValue()
    ny, nx = (fp.RasterYSize, fp.RasterXSize)
    return data, proj, geo, nodata


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

FORCE_OUTPUT_DIM = (5000, 5000)


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

                    imgdata, proj, geo, nodata = read_raster(fname)

                    for i,bname in enumerate(bnames):

                        fnameout = "{}_{}.tif".format(
                            os.path.splitext(fname)[0], bname)

                        VerboseOut("splitting {}".format(fnameout))

                        try:
                            data = imgdata[i,:,:].squeeze()
                        except:
                            data = imgdata[:,:]


                        if FORCE_OUTPUT_DIM is not None:
                            if data.shape != FORCE_OUTPUT_DIM:
                                yf, xf = FORCE_OUTPUT_DIM
                                yd, xd = data.shape
                                if xd > xf:
                                    data = data[:,:xf]
                                elif xd < xf:
                                    data = np.hstack((data, np.zeros((data.shape[0], 1), dtype=data.dtype)))
                                if yd > yf:
                                    data = data[:yf,:]
                                elif yd < yf:
                                    data = np.vstack((data, np.zeros((1, data.shape[1]), dtype=data.dtype)))

                        scale = 10000
                        data = data.astype('int16')
                        dtype = gdal.GDT_Int16

                        write_raster(fnameout, data, proj, geo, nodata, dtype)

                    img = None

    utils.gips_exit()


if __name__ == "__main__":
    main()

