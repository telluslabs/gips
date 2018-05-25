#!/usr/bin/env bash

# daily update of Landsat for a specific place

ARGS=("$@")
OUTNAME=${ARGS[0]}
INSHPPATH="/archive/vector/"${ARGS[1]}
OUTSHPPATH="/archive/vector/"${ARGS[2]}

# the date is always yesterday
DATE=$(date -d "yesterday" '+%Y-%m-%d')

# the outdir from container perspective
OUTDIR="/archive/"${OUTNAME}${DATE}

# fetch and process reflectance and cloud mask
gips_process landsat -p ref fmask -s ${INSHPPATH} -v4 -d ${DATE} --fetch

# export feature rasters for output tiles
gips_export landsat -p ref fmask -s ${OUTSHPPATH} -v4 -d ${DATE} --outdir ${OUTDIR} --notld --res 30 30

# apply cloud mask to reflectance images
gips_mask ${OUTDIR}/* --pmask fmask

# hackily split out separate bands
gips_split ${OUTDIR}/* --prodname ref-masked
