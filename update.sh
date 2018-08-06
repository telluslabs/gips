#!/bin/bash

# Make sure we fail on errors
set -e

# perform processing for a single day

SHPFILE=$1
DATE=$2
OUTDIR=$3
S3PREFIX=$4

/bin/bash initialize.sh

gips_process landsat -p ref temp fmask -s $SHPFILE -d $DATE -v4 --fetch --overwrite

gips_export landsat -p ref temp fmask -s $SHPFILE -d $DATE -v4 --outdir $OUTDIR --notld --res 30 30 --key tileid --overwrite

gips_mask ${OUTDIR}/* --pmask fmask

gips_split ${OUTDIR}/* --prodname ref-masked

gips_split ${OUTDIR}/* --prodname temp-masked

python upload_s3.py --startpath $OUTDIR --s3prefix $S3PREFIX

rm -rf /archive/gips
