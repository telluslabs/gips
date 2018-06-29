#!/usr/bin/env bash

# this runs inside a new container

# there must be a conf dir with a copy of sixs
cp /conf/sixs /usr/local/bin/sixs
chmod +x /usr/local/bin/sixs

# there must be a file with data center credentials
source /conf/credentials.sh

# create a settings file with proper credentials
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

# create and initialize a db file if there isn't one
gips_config env

# put long term mean AOD data in the right place
tar xfvz /conf/aod.composites.tgz -C /archive > /dev/null

# create an export folder for the project outputs
mkdir /archive/export; chmod ogu+rwx /archive/export

# move initial vector data into a shared location
cp -r /conf/vector /archive/
