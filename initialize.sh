#!/usr/bin/env bash

# runs inside a new container

cp /conf/sixs /usr/local/bin/sixs
chmod +x /usr/local/bin/sixs

source /conf/credentials.sh

cd /gips
cp -f gips/settings_template_docker.py gips/settings.py
sed -i~ \
    -e "s/^EARTHDATA_USER.*/EARTHDATA_USER = \"${EARTHDATA_USER}\"/" \
    -e "s/^EARTHDATA_PASS.*/EARTHDATA_PASS = \"${EARTHDATA_PASS}\"/" \
    -e "s/^USGS_USER.*/USGS_USER = \"${USGS_USER}\"/" \
    -e "s/^USGS_PASS.*/USGS_PASS = \"${USGS_PASS}\"/" \
    -e "s/^ESA_USER.*/ESA_USER = \"${ESA_USER}\"/" \
    -e "s/^ESA_PASS.*/ESA_PASS = \"${ESA_PASS}\"/" \
    gips/settings.py

gips_config env
tar xfvz /conf/aod.composites.tgz -C /archive
mkdir /archive/export
