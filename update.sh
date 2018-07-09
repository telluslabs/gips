!#/usr/bin/env bash

SHPFILE=$1
DATE=$2
OUTDIR=$3

/bin/bash initialize.sh

gips_process landsat -p ref temp fmask -s $SHPFILE -d $DATE -v4 --fetch

gips_export landsat -p ref temp fmask -s $SHPFILE -d $DATE -v4 --outdir $OUTDIR --notld --res 30 30

gips_mask ${OUTDIR}/* --pmask fmask

gips_split ${OUTDIR}/* --prodname ref-masked

gips_split ${OUTDIR}/* --prodname temp-masked
