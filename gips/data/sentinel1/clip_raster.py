from osgeo import gdal
import os
import glob

files = glob.glob('/processed/*.tif')

for filename in files:
    print('Processing {0}'.format(filename))
    ds = gdal.Warp(os.path.join('/output', os.path.basename(filename)), filename, format='GTiff',
                   cutlineDSName='/shp/{0}.shp'.format(os.getenv('SHAPEFILE')), cutlineLayer=os.getenv('SHAPEFILE'),
                   options=['COMPRESS=LZW'], cropToCutline=True, dstAlpha=True, xRes=0.0001, yRes=0.0001)
    if ds is None:
        raise NameError('File: {0} Not Found'.format(str(filename)))
