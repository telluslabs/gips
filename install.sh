#!/usr/bin/env bash

echo "This hasn't yet been ported to python 3 + gippy 1.0"
exit 1

set -e
git remote show origin | grep 'Fetch URL: .*gips.git$' -q

echo -n "Enter full path to data repository: "
read ARCHIVEDIR

echo -n "Enter your email address: "
read EMAIL

sudo apt-get update

sudo apt-get install git virtualenv python python-pip gfortran libboost-all-dev\
     libfreetype6-dev libgnutls-dev libatlas-base-dev libgdal-dev libgdal1-dev\
     gdal-bin python-numpy python-scipy python-gdal swig2.0

sudo -H pip install -U pip>=9.0.1

virtualenv --system-site-packages venv

source venv/bin/activate

pip install --process-dependency-links -e .

pip install -r dev_requirements.txt # if you wish to run the test suite; CF docker/

gips_config env -r $ARCHIVEDIR -e $EMAIL
gips_config user

echo ""
echo "Now edit settings.py for things like EARTHDATA password"
echo "gips_project modis --fetch -s gips/test/NHseacoast.shp -d 2017-5-25 -v5 -p ndvi8"
