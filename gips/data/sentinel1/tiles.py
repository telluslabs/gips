from __future__ import print_function

import sys, os

import numpy as np
import fiona
from fiona.crs import from_epsg
from shapely.geometry import mapping, Polygon
from shapely.wkt import loads
from osgeo import ogr
import geopandas as gpd

# from fieldtools.boundaries.utils import read_raster, write_raster
# from fieldtools.boundaries.geom_intersects import extract

from gips.data.sentinel1.geom_intersects import extract


from pdb import set_trace


TEMPDIR = "/archive/vector"


# Tile dimensions
DLON = 0.15
DLAT = 0.15


def segmentize(geom, mindist):
    # shapely Polygon to wkt
    wkt = geom.wkt
    # create ogr geometry
    geom = ogr.CreateGeometryFromWkt(wkt)
    # densify geometry
    geom.Segmentize(mindist)
    # ogr geometry to wkt
    wkt2 = geom.ExportToWkt()
    # wkt to shapely Polygon
    geom2 = loads(wkt2)
    return geom2



def make_tilegrid(shpfile, tileid):

    gdf = gpd.read_file(shpfile)
    orig_crs = gdf.crs
    gdf = gdf.to_crs(epsg=4326)
    bounds = gdf.bounds

    # UL
    minx = bounds['minx'].min()
    maxy = bounds['maxy'].max()
    # LR
    maxx = bounds['maxx'].max()
    miny = bounds['miny'].min()

    print(minx, maxx, miny, maxy)

    v_ul = int((90. - maxy)/DLON)
    h_ul = int((minx + 180.)/DLON)

    v_lr = int((90. - miny)/DLON)
    h_lr = int((maxx + 180.)/DLON)

    nygrid = v_lr - v_ul + 1
    nxgrid = h_lr - h_ul + 1

    # outdir = os.path.split(shpfile)[0]

    tileid = "{}_{}".format(h_ul, v_ul)

    lon_ul = -180.0 + DLON*h_ul
    lat_ul = 90.0 - DLAT*v_ul

    # the rectangular grid which might contain some extra tiles
    rectfile = os.path.join(TEMPDIR, '{}_{}_{}.shp'.format(tileid, nxgrid, nygrid))

    dlon = DLON
    dlat = DLAT

    schema = {
        'geometry': 'Polygon',
        'properties': {'tileid': 'str', 'h':'int', 'v':'int', 'bounds': 'str'},
    }
    print(dlon, dlat)
    crs = from_epsg(4326)
    with fiona.open(rectfile, 'w', 'ESRI Shapefile', schema, crs=crs) as shp:
        # latitude
        for i in range(nygrid):
            lat1 = lat_ul - i*dlat
            lat0 = lat1 - dlat
            # longitude
            for j in range(nxgrid):
                lon0 = lon_ul + j*dlon
                lon1 = lon0 + dlon
                poly = Polygon(
                    [(lon0, lat1), (lon1, lat1), (lon1, lat0), (lon0, lat0), (lon0, lat1)])
                poly = segmentize(poly, dlon/10.)
                h = j + h_ul
                v = i + v_ul
                tileid = "%03d_%03d" % (h, v)
                bounds = str((lon0, lat0, lon1, lat1))
                shp.write({
                    'geometry': mapping(poly),
                    'properties': {'tileid': tileid,'bounds': bounds, 'h':int(h), 'v':int(v)},
                })

    print('wrote', rectfile)

    # change crs of rectfile to match crs of shpfile
    # gdf = gpd.read_file(shpfile)
    gdf = gpd.read_file(rectfile)
    gdf = gdf.to_crs(orig_crs)
    gdf.to_file(rectfile)


    outfile = os.path.join('/archive/vector', 'tiles.shp')

    print('extracting', rectfile, shpfile, outfile)
    tilelist = extract(rectfile, shpfile, outfile, merge=True, buffer=None, buffer_after=None, filter=None, same_attrs=None)

    print('removing', rectfile)
    os.remove(rectfile)

    # return the tilelist
    return outfile, tilelist

