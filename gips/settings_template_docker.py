#!/usr/bin/env python

################################################################################
#    GIPS: Geospatial Image Processing System
#
#    AUTHOR: Matthew Hanson
#    EMAIL:  matt.a.hanson@gmail.com
#
#    Copyright (C) 2014 Applied Geosolutions
#
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program. If not, see <http://www.gnu.org/licenses/>
################################################################################

# GIPS complete settings file

# Used for anonymous FTP
EMAIL = 'rbraswell@ags.io'
TLD = '/archive'

prepend = lambda dir: ('{}/'+dir).format(TLD)

# Site files and data tiles vectors can be retrieved from a database
DATABASES = {
#    'tiles': {
#        'NAME': '',
#        'USER': '',
#        'PASSWORD': '',
#        'HOST': '',
#        'PORT': '5432',
#    }
    'inventory': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': prepend('gips-inv-db.sqlite3'),
    },
}

# STATS_FORMAT = {} # defaults to empty dict

# For NASA EarthData Authentication
EARTHDATA_USER = ""
EARTHDATA_PASS = ""

# For USGS machine-to-machine authentication
USGS_USER = ""
USGS_PASS = ""

# For USGS machine-to-machine authentication
ESA_USER = ""
ESA_PASS = ""

REPOS = {
    'aod': {
        'repository': prepend('aod'),
    },
    'landsat': {
        'repository': prepend('landsat'),
        '6S': True,             # atm correction for VIS/NIR/SWIR bands
        'MODTRAN': False,       # atm correction for LWIR
        'extract': False,       # extract files from tar.gz before processing instead of direct access
        'username': USGS_USER,
        'password': USGS_PASS,
        'source': 'gs',
    },
    'modis': {
        'repository': prepend('modis'),
        'username': EARTHDATA_USER,
        'password': EARTHDATA_PASS,
    },
    'sentinel2': {
        'repository': prepend('sentinel2'),
        'username': ESA_USER,
        'password': ESA_PASS,
        'extract': False,  # extract files from tar.gz before processing instead of direct access
    },
    'smap': {
        'repository': prepend('smap'),
        'username': EARTHDATA_USER,
        'password': EARTHDATA_PASS,
    },
    'cdl': {
        'repository': prepend('cdl'),
    },
    'chirps': {
        'repository': prepend('chirps'),
    },
    'prism': {
        'repository': prepend('prism'),
    },
    'merra': {
        'repository': prepend('merra'),
        'username': EARTHDATA_USER,
        'password': EARTHDATA_PASS,
    },
    'daymet': {
        'repository': prepend('daymet'),
    },
    'prism': {
        'repository': prepend('prism'),
    },
}
