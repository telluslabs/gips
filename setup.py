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

"""
setup for GIPS
"""

import os
from setuptools import setup, find_packages
import shutil
import glob
import traceback
import imp

__version__ = imp.load_source('gips.version', 'gips/version.py').__version__

# collect console scripts to install
console_scripts = []
for f in glob.glob('gips/scripts/*.py'):
    try:
        name = os.path.splitext(os.path.basename(f))[0]
        if name not in ['__init__', 'core']:
            script = 'gips_%s = gips.scripts.%s:main' % (name, name.lower())
            console_scripts.append(script)
    except:
        print traceback.format_exc()

# GIPS requirements should be added at the level appropriate
#  lib - required to install and import gips.core classes

_lib_req = ['gippy>=0.3.8,<0.4.0']
_base_req = [
    'shapely',
    'python-dateutil',
]
_full_req = _base_req + [
    'landsat-util==0.8.0ircwaves0',
    'Py6S>=1.5.0',
    'requests',
    'pydap<=3.2',
    'netCDF4',
]
_orm_req = _full_req + [
    'django==1.10',
    'psycopg2<=2.6',
]
_dh_req = _orm_req + [
    'rq',
]

setup(
    name='gips',
    version=__version__,
    description='Geospatial Image Processing System',
    author='Matthew Hanson',
    author_email='matt.a.hanson@gmail.com',
    maintainer='Ian Cooke',
    maintainer_email='icooke@ags.io',
    packages=find_packages(),
    package_data={'': ['*.shp', '*.prj', '*.shx', '*.dbf']},
    install_requires=_lib_req,
    extras_require={
        'base': _base_req,
        'full': _full_req,
        'orm': _orm_req,
        'dh-rq': _dh_req,
    },
    dependency_links=[
        'http://github.com/ircwaves/landsat-util/tarball/landsat_util#egg=landsat-util-0.8.0ircwaves0',
        'http://github.com/Applied-GeoSolutions/gippy/archive/v0.3.9.tar.gz#egg=gippy-0.3.9',
    ],
    entry_points={'console_scripts': console_scripts},
    zip_safe=False,
)
