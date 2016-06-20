#!/bin/bash

set -e

# this script needs to run in the clone dir
git remote get-url origin | grep Applied-GeoSolutions/gips.git -q
test -d .git

echo === install system deps ===
# TODO are these needed?
# innstall UbuntuGIS repository
# sudo apt-get install python-software-properties
# sudo add-apt-repository ppa:ubuntugis/ubuntugis-unstable
# sudo apt-get update

# TODO I doubt *ALL* the boost libs are needed and there are MANY of them;
# would be great to reduce the bulk
sudo apt-get install virtualenv python g++ gfortran swig \
                     libboost-all-dev libfreetype6-dev libgnutls-dev \
                     libatlas-base-dev libgdal-dev libgdal1-dev gdal-bin \
                     python-pip python-numpy python-scipy python-gdal 

echo === clone source repo and setup virtualenv ===
virtualenv .venv --system-site-packages
source .venv/bin/activate

echo === install a few dependencies via pip ===
pip install -r dev_requirements.txt
# gippy has to be done this way because gippy stopped being tracked in pypi
pip install 'https://github.com/Applied-GeoSolutions/gippy/tarball/v0.3.x#egg=gippy-0.3.8-'`date +%Y%m%d`

echo === install GIPS itself ===
# TODO --process-dependency-links is deprecated
pip install --process-dependency-links -e .

# check install: if this exits 0, install probably succeeded
gips_config print &>/dev/null
echo "Install complete."
