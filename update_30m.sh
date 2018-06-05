#!/usr/bin/env bash

# daily update of Landsat or Sentinel2 for a specific place
# this runs inside the GIPS container

ARGS=("$@")

ASSET=${ARGS[0]}
NAME=${ARGS[1]}
INSHPPATH="/archive/vector/"${ARGS[2]}
OUTSHPPATH="/archive/vector/"${ARGS[3]}
OUTSHPKEY=${ARGS[4]}
DATE=${ARGS[5]}

# the outdir from container perspective
OUTNAME=${ASSET}"_"${NAME}
OUTDIR="/archive/export/"${OUTNAME}"_"${DATE}

# they unfortunately have different mask product names
if [ ${ASSET} == "sentinel2" ]; then MASK="cfmask"; else MASK="fmask"; fi

# sentinel2 has no longwave bands
if [ ${ASSET} == "sentinel2" ]; then TEMP=""; else TEMP="temp"; fi

# fetch and process reflectance and cloud mask
echo "gips_process ${ASSET} -p ref ${TEMP} ${MASK} -s ${INSHPPATH} -v4 -d ${DATE} --fetch"
gips_process ${ASSET} -p ref ${TEMP} ${MASK} -s ${INSHPPATH} -v4 -d ${DATE} --fetch

# export feature rasters for output tiles
echo "gips_export ${ASSET} -p ref ${TEMP} ${MASK} -s ${OUTSHPPATH} -v4 -d ${DATE} --outdir ${OUTDIR} --notld --res 30 30 --key ${OUTSHPKEY}"
gips_export ${ASSET} -p ref ${TEMP} ${MASK} -s ${OUTSHPPATH} -v4 -d ${DATE} --outdir ${OUTDIR} --notld --res 30 30 --key ${OUTSHPKEY}

# apply cloud mask to reflectance images
echo "gips_mask ${OUTDIR}/* --pmask ${MASK}"
gips_mask ${OUTDIR}/* --pmask ${MASK}

# hackily split out separate bands
echo "gips_split ${OUTDIR}/* --prodname ref-masked"
gips_split ${OUTDIR}/* --prodname ref-masked
echo "gips_split ${OUTDIR}/* --prodname temp-masked"
gips_split ${OUTDIR}/* --prodname temp-masked
