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
EMAIL = '$EMAIL'


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
        'NAME': '$TLD/gips-inv-db.sqlite3',
    },
}

# For NASA EarthData Authentication
EARTHDATA_USER = ""
EARTHDATA_PASS = ""

REPOS = dict()


"""
# to add repository add a `${driver_dir}/settings_template.py` of the form
REPOS['dataname'] = {
        # REQUIRED: path to top level directory of data
        'repository': '$TLD/dataname',
        # OPTIONAL: path to driver directory location
        #(default to gips/data/dataname/ if not given)
        'driver': '',
        # OPTIONAL: override location of tiles vector
        # (default to gips/data/dataname/tiles.shp)
       'tiles': '',
        #'tiles': 'mydatabase:mydatatype_tiles',        # database format
        #'tiles': '~/randomdir/dataname_tiles.shp'      # file format
    }
"""
