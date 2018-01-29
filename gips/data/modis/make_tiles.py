#!/usr/bin/env python

import sys
import os
import glob
from osgeo import gdal

import numpy as np
import fiona
from fiona.crs import from_string
from shapely.geometry import mapping, Polygon


STARTDIR = "/titan/data/modis6/tiles"
OUTPATH = "./tiles.shp"
PROJ = "+proj=sinu +lon_0=0 +x_0=0 +y_0=0 +a=6371007.181 +b=6371007.181 +units=m +no_defs"
WIDTH = 2400
NSTEP = 100
VALIDATED = True


def write_shapefile(data, proj):
    schema = {
        'geometry': 'Polygon',
        'properties': {'tileid': 'str', 'bounds': 'str'},
    }
    crs = from_string(proj)
    with fiona.open(OUTPATH, 'w', 'ESRI Shapefile', schema, crs=crs) as shp:
        for tileid, coords in data:
            arr = np.array(coords)
            xmin, ymin = tuple(arr.min(axis=0))
            xmax, ymax = tuple(arr.max(axis=0))
            bounds = str((xmin, ymin, xmax, ymax))
            poly = Polygon(coords)
            shp.write({
                'geometry': mapping(poly),
                'properties': {'tileid': tileid, 'bounds': bounds},
            })


if __name__ == "__main__":

    boxes = []
    tilecount = 0
    for basepath, dirnames, filenames in os.walk(STARTDIR):
        for filename in filenames:
            if filename.endswith('.tif'):

                filepath = os.path.join(basepath, filename)
                name = os.path.splitext(os.path.split(filepath)[1])[0]
                tile = name.split('_')[0]

                if VALIDATED == True and tile in [b[0] for b in boxes]:
                    continue

                gdalfile = gdal.Open(filepath)
                nx, ny = gdalfile.RasterXSize, gdalfile.RasterYSize
                if nx != WIDTH:
                    continue

                print filepath                
                x0, dx, dxy, y0, dyx, dy = gdalfile.GetGeoTransform()
                nstep = NSTEP
                xstep = nx/float(nstep)
                ystep = ny/float(nstep)
                xs, ys = (x0, y0)
                coords = [(x0, y0)]                
                for direction in ((1, 0), (0, 1), (-1, 0), (0, -1)):
                    for step in range(nstep):
                        x1 = x0 + dx*xstep*direction[0]
                        y1 = y0 + dy*ystep*direction[1]
                        coords.append((x1, y1))
                        x0, y0 = (x1, y1)

                coords[-1] = (xs, ys)
                box = (tile, coords)
                
                if (tile, coords) not in boxes:
                    assert tile not in [b[0] for b in boxes]
                    assert coords not in [b[1] for b in boxes]
                    print "appending", tile
                    boxes.append((tile, coords))
                    tilecount += 1

    print "writing %d features" % len(boxes)
    write_shapefile(boxes, PROJ)
