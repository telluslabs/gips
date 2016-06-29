#!/bin/bash

set -e

[ -z "$GIPSTESTPATH" ] && GIPSTESTPATH="."

ARGS="-s $GIPSTESTPATH/NHseacoast.shp -d 2012-12-01,2012-12-10 -v 4"

# TODO why is this here but unused?
ARGS2="-s /etc/gips/test/nsamerica.shp --where "CNTRY_NAME='Guyana'" -d 2012-12-01 -v 4"

echo ARGS="$ARGS"

# mosaic without warping
# DONE:  gips_project modis $ARGS --outdir modis_project_nowarp --notld
# TODO it's not clear if this needs to be converted to a test as gips_stats is
# already exercised by a previous test; same for further stats commands below.
gips_stats modis_project_nowarp

# warp tiles
# DONE:  gips_tiles modis $ARGS --outdir modis_warped_tiles --notld
gips_stats modis_warped_tiles/*

# copy tiles
# DONE:  gips_tiles modis -t h12v04 -d 2012-12-01,2012-12-10 -v 4 --outdir modis_tiles --notld
gips_stats modis_tiles
