#!/bin/bash

ARGS="-s /etc/gips/test/NHseacoast.shp -d 2012-12-01,2012-12-10 -v 4"
ARGS2="-s /etc/gips/test/nsamerica.shp --where "CNTRY_NAME='Guyana'" -d 2012-12-01 -v 4"


gips_info Modis
gips_inventory Modis $ARGS --fetch
gips_process Modis $ARGS

# mosaic
gips_project Modis $ARGS --res 100 100 --outdir modis_project --notld
gips_stats modis_project/*

# mosaic selected location
gips_project Modis $ARGS --res 1000 1000 --outdir modis_project_loc --notld
gips_stats modis_project_loc/*

# mosaic without warping
gips_project Modis $ARGS --outdir modis_project_nowarp --notld
gips_stats modis_project_nowarp

# warp tiles
gips_tiles Modis $ARGS --outdir modis_warped_tiles --notld
gips_stats modis_warped_tiles/*

# copy tiles
gips_tiles Modis -t h12v04 -d 2012-12-01,2012-12-10 -v 4 --outdir modis_tiles --notld
gips_stats modis_tiles
