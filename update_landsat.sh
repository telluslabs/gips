#!/usr/bin/env bash

# daily update of Landsat for a specific place

ARGS=("$@")
OUTNAME=${ARGS[0]}
INSHPPATH="/archive/vector/"${ARGS[1]}
OUTSHPPATH="/archive/vector/"${ARGS[2]}
OUTSHPKEY=${ARGS[3]}
DATE=${ARGS[4]}

# the outdir from container perspective
OUTDIR="/archive/export/"${OUTNAME}"_"${DATE}

# fetch and process reflectance and cloud mask
echo "gips_process landsat -p ref fmask -s ${INSHPPATH} -v4 -d ${DATE} --fetch"
gips_process landsat -p ref fmask -s ${INSHPPATH} -v4 -d ${DATE} --fetch

# export feature rasters for output tiles
echo "gips_export landsat -p ref fmask -s ${OUTSHPPATH} -v4 -d ${DATE} --outdir ${OUTDIR} --notld --res 30 30"
gips_export landsat -p ref fmask -s ${OUTSHPPATH} -v4 -d ${DATE} --outdir ${OUTDIR} --notld --res 30 30 --key ${OUTSHPKEY}

# apply cloud mask to reflectance images
echo "gips_mask ${OUTDIR}/* --pmask fmask"
gips_mask ${OUTDIR}/* --pmask fmask

# hackily split out separate bands
echo "gips_split ${OUTDIR}/* --prodname ref-masked"
gips_split ${OUTDIR}/* --prodname ref-masked
