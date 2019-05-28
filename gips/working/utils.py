from __future__ import print_function

import os
import re

import numpy as np
import geopandas as gpd
from osgeo import gdal, ogr, osr


def read_raster(infile, meta=False):
    fp = gdal.Open(infile)
    proj = fp.GetProjection()
    geo = fp.GetGeoTransform()
    data = fp.ReadAsArray()
    ny, nx = (fp.RasterYSize, fp.RasterXSize)
    if meta is True:
        meta = fp.GetMetadata()
        return data, proj, geo, meta
    else:
        return data, proj, geo


def write_raster(outfile, data, proj, geo, meta={}, missing=None, ct=None):
    gdal.GDT_UInt8 = gdal.GDT_Byte
    np_dtype = str(data.dtype)
    dtype = eval('gdal.GDT_' + np_dtype.title().replace('Ui','UI'))
    driver = gdal.GetDriverByName('GTiff')
    dims = data.shape
    if len(dims) == 3:
        nb, ny, nx = data.shape
    else:
        ny, nx = data.shape
        nb = 1
        data = data.reshape(nb, ny, nx)
    tfh = driver.Create(outfile, nx, ny, nb, dtype, [])
    tfh.SetProjection(proj)
    tfh.SetGeoTransform(geo)
    tfh.SetMetadata(meta)
    for i in range(nb):
        tband = tfh.GetRasterBand(i+1)
        if missing is not None:
            tband.SetNoDataValue(missing)
        if ct is not None:
            tband.SetColorTable(ct)
        tband.WriteArray(data[i,:,:].squeeze())
    del tfh


def polygonize(rasterTemp, outShp):
    """
    Create polygon shapefile for a single band image
    The band value is written to an attribute field called 'class'
    """
    sourceRaster = gdal.Open(rasterTemp)
    band = sourceRaster.GetRasterBand(1)
    driver = ogr.GetDriverByName("ESRI Shapefile")
    # if shapefile already exist, delete it
    if os.path.exists(outShp):
        driver.DeleteDataSource(outShp)
    outDatasource = driver.CreateDataSource(outShp)
    # get proj from raster
    srs = osr.SpatialReference()
    srs.ImportFromWkt(sourceRaster.GetProjectionRef())
    # create layer with proj
    outLayer = outDatasource.CreateLayer(outShp, srs)
    # add class column to shapefile
    newField = ogr.FieldDefn('class', ogr.OFTInteger)
    outLayer.CreateField(newField)
    gdal.Polygonize(band, None, outLayer, 0, [], callback=None)
    outDatasource.Destroy()
    sourceRaster = None
    band = None
    ioShpFile = ogr.Open(outShp, update=1)
    lyr = ioShpFile.GetLayerByIndex(0)
    lyr.ResetReading()
    for i in lyr:
        lyr.SetFeature(i)
    ioShpFile.Destroy()


def get_tileids(tileids, attrname='tileid'):
    """
    Get list of tileids from a variety of possible sources using
    ridiculously overloaded input 'tileids'
    """
    if tileids.endswith('.txt'):
        # tileids might come from a file
        tileids = open(tileids).readlines()
        tileids = [t.strip() for t in tileids]
    elif tileids.endswith('.shp'):
        # tileids might come from a shapefile
        gdf = gpd.read_file(tileids)
        tileids = gdf[attrname].values.tolist()
    elif os.path.isdir(tileids):
        # tileids can come from a directory tree
        tileids_dir = tileids
        tileids = []
        for root, dirs, files in os.walk(tileids_dir):
            for file in files:
                if re.search('\d{3}_\d{3}\.tif', file):
                    tileids.append(file.split('.')[0])
    else:
        # or one or more specified on the command line
        tileids = tileids.split(',')
    return tileids
