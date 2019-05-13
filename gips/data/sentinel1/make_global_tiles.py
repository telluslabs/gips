from __future__ import print_function

import sys, os
import click

import numpy as np
import fiona
from fiona.crs import from_epsg
from shapely.geometry import mapping, Polygon
from shapely.wkt import loads
from osgeo import ogr
import geopandas as gpd

from fieldtools.boundaries.utils import read_raster, write_raster
from fieldtools.boundaries.geom_intersects import extract


from pdb import set_trace


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


def make_rectangular_tilegrid(outdir, tileid, nxgrid, nygrid):
    """
    Example:
    python make_global_tiles.py -d /data/analysis_tiles -t 553_330 -g 1,1
    """

    # nxgrid, nygrid = [int(g) for g in grid.split(',')]

    htile, vtile = [int(t) for t in tileid.split('_')]

    lon_ul = -180.0 + DLON*htile
    lat_ul = 90.0 - DLAT*vtile

    outfile = os.path.join(outdir, '{}_{}_{}.shp'.format(tileid, nxgrid, nygrid))

    # create_grid(outfile, lon_ul, lat_ul, nxgrid, nygrid, DLON, DLAT)

    dlon = DLON
    dlat = DLAT

    schema = {
        'geometry': 'Polygon',
        'properties': {'tileid': 'str', 'h':'int', 'v':'int', 'bounds': 'str'},
    }
    print(dlon, dlat)
    crs = from_epsg(4326)
    with fiona.open(outfile, 'w', 'ESRI Shapefile', schema, crs=crs) as shp:
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
                h = j + htile
                v = i + vtile
                tileid = "%03d_%03d" % (h, v)
                bounds = str((lon0, lat0, lon1, lat1))
                shp.write({
                    'geometry': mapping(poly),
                    'properties': {'tileid': tileid,'bounds': bounds, 'h':int(h), 'v':int(v)},
                })

    print('wrote', outfile)
    return(outfile)


def find_rectangular_tiles(shpfile):

    df = gpd.read_file(shpfile)
    df = df.to_crs(epsg=4326)
    bounds = df.bounds

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

    nv = v_lr - v_ul + 1
    nh = h_lr - h_ul + 1

    return(h_ul, v_ul, h_lr, v_lr, nh, nv)


@click.group()
def cli():
    pass


@click.command()
@click.option('--outdir', '-o', type=str, required=True)
@click.option('--tileid', '-t', type=str, required=True)
def make_tileimg(outdir, tileid):

    htile, vtile = [int(t) for t in tileid.split('_')]

    lon_ul = -180.0 + DLON*htile
    lat_ul = 90.0 - DLAT*vtile

    outfile = os.path.join(outdir, '{}_blank.tif'.format(tileid))

    dlon = DLON
    dlat = DLAT

    res = 0.000049999

    data = np.ones((3000,3000), dtype=np.uint8)
    proj = 'GEOGCS["WGS 84",DATUM["WGS_1984",SPHEROID["WGS 84",6378137,298.257223563,AUTHORITY["EPSG","7030"]],AUTHORITY["EPSG","6326"]],PRIMEM["Greenwich",0],UNIT["degree",0.0174532925199433],AUTHORITY["EPSG","4326"]]'
    geo = [lon_ul, res, 0, lat_ul, 0, -res]

    print('writing', outfile)
    write_raster(outfile, data, proj, geo, meta={}, missing=None)


def _make_tilegrid(shpfile, outfile):

    h_ul, v_ul, h_lr, v_lr, nh, nv = find_rectangular_tiles(shpfile)
    print(h_ul, v_ul, h_lr, v_lr, nh, nv)

    outdir = os.path.split(shpfile)[0]
    tileid = "{}_{}".format(h_ul, v_ul)
    rectfile = make_rectangular_tilegrid(outdir, tileid, nh, nv)

    # change crs of rectfile to match crs of shpfile
    gdf = gpd.read_file(shpfile)
    crs = gdf.crs
    gdf = gpd.read_file(rectfile)
    gdf = gdf.to_crs(crs)
    gdf.to_file(rectfile)

    print('extracting', rectfile, shpfile, outfile)
    extract(rectfile, shpfile, outfile, merge=True, buffer=None, buffer_after=None, filter=None, same_attrs=None)

    print('removing', rectfile)
    os.remove(rectfile)

    set_trace()

    # return the tilelist



@click.command()
@click.option('--shpfile', '-s', required=True)
@click.option('--outfile', '-o', required=True)
def make_tilegrid(shpfile, outfile):
    _make_tilegrid(shpfile, outfile)


@click.command()
@click.option('--outdir', '-o', type=str, required=True)
@click.option('--tileid', '-t', type=str, required=True)
def make_onetile(outdir, tileid):
    """ Make a shapefile that has the boundary of a single tile """
    make_rectangular_tilegrid(outdir, tileid, 1, 1)


cli.add_command(make_tilegrid)
cli.add_command(make_tileimg)
cli.add_command(make_onetile)


if __name__ == "__main__":
    cli()
