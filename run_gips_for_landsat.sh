#!/usr/bin/env bash

# run this from inside the gips container

DATE="2018-05-22"
OUTDIR="/archive/export_landsat_ard_indigo_"${DATE}

# fetch and process reflectance and cloud mask
gips_process landsat -p ref fmask -s /archive/vector/indigo_temp_buffer.shp -v4 -d ${DATE} --fetch

# export feature rasters
gips_export landsat -p ref fmask -s /archive/vector/conus_ard_grid.shp -v4 -d ${DATE} --outdir ${OUTDIR} --notld --res 30 30

# perform cloud mask
gips_mask ${OUTDIR}/* --pmask fmask

# hackily split out bands
gips_split ${OUTDIR}/* --prodname ref-masked
