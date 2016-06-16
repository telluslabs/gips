#!/bin/bash

set -e

[ -z "$GIPSTESTPATH" ] && GIPSTESTPATH="."

ARGS="-s $GIPSTESTPATH/NHseacoast.shp -d 2012-12-01,2012-12-10 -v 4"

gips_info modis
gips_inventory modis $ARGS --fetch
gips_process modis $ARGS

# mosaic
gips_project modis $ARGS --res 100 100 --outdir modis_project --notld
gips_stats modis_project/*

# mosaic without warping
gips_project modis $ARGS --outdir modis_project_nowarp --notld
gips_stats modis_project_nowarp

# warp tiles
gips_tiles modis $ARGS --outdir modis_warped_tiles --notld
gips_stats modis_warped_tiles/*

# copy tiles
gips_tiles modis -t h12v04 -d 2012-12-01,2012-12-10 -v 4 --outdir modis_tiles --notld
gips_stats modis_tiles
