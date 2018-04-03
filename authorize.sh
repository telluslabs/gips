#!/usr/bin/env bash

cd /gips
source credentials.sh
cp -f gips/settings_template_docker.py gips/settings.py
sed -i~ \
    -e "s/^EARTHDATA_USER.*/EARTHDATA_USER = \"${EARTHDATA_USER}\"/" \
    -e "s/^EARTHDATA_PASS.*/EARTHDATA_PASS = \"${EARTHDATA_PASS}\"/" \
    -e "s/^USGS_USER.*/USGS_USER = \"${USGS_USER}\"/" \
    -e "s/^USGS_PASS.*/USGS_PASS = \"${USGS_PASS}\"/" \
    -e "s/^ESA_USER.*/ESA_USER = \"${ESA_USER}\"/" \
    -e "s/^ESA_PASS.*/ESA_PASS = \"${ESA_PASS}\"/" \
    gips/settings.py
