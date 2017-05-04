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

import os
import datetime
import time
import numpy as np

from pydap.client import open_url

import gippy
from gips.data.core import Repository, Asset, Data
from gips.utils import VerboseOut, basename


PROJ = ''.join([
    'PROJCS["unnamed",GEOGCS["WGS 84",DATUM["WGS_1984",SPHEROID["WGS 84",6378',
    '137,298.257223563,AUTHORITY["EPSG","7030"]],AUTHORITY["EPSG","6326"]],PR',
    'IMEM["Greenwich",0],UNIT["degree",0.0174532925199433],AUTHORITY["EPSG","',
    '4326"]],PROJECTION["Lambert_Conformal_Conic_2SP"],PARAMETER["standard_pa',
    'rallel_1",25],PARAMETER["standard_parallel_2",60],PARAMETER["latitude_of',
    '_origin",42.5],PARAMETER["central_meridian",-100],PARAMETER["false_easti',
    'ng",0],PARAMETER["false_northing",0],UNIT["metre",1,AUTHORITY["EPSG","90',
    '01"]]]'
])

# Cyanomap: tmax, tmin, tmean, ppt, solar rad, and vapor pressure

# maximum temperature (C) - tmax.nc *
# minimum temperature (C) - tmin.nc  *
# precipitation (mm day-1) - prcp.nc *
# shortwave radiation (W m-2) - srad.nc *
# vapor pressure (Pa) - vp.nc *
# snow-water equivalent (kg m-2) - swe.nc
# daylength (sec day-1) - dayl.nc


def create_datatype(np_dtype):
    """ provide translation between data type codes """
    gippy.GDT_UInt8 = gippy.GDT_Byte
    np_dtype = str(np_dtype)
    typestr = 'gippy.GDT_' + np_dtype.title().replace('Ui', 'UI')
    g_dtype = eval(typestr)
    return g_dtype

class daymetRepository(Repository):
    name = 'Daymet'
    description = 'Daymet weather data'


class daymetAsset(Asset):
    Repository = daymetRepository

    _sensors = {
        'daymet': {
            'description': 'Daily surface weather and climatological summaries',
        }
    }

    _latency = 0
    _startdate = datetime.date(1980, 1, 1)
    _url = "https://thredds.daac.ornl.gov/thredds/dodsC/ornldaac/1328/tiles/%d/%s_%d"
    _basename_pat = 'daymet_{}_{}_{}{}.tif'

    _assets = {
        'tmin': {
            'description': 'Daily minimum air temperature (C)',
            'pattern': 'daymet_tmin_*_???????.tif',
            'source': 'tmin.nc',
            'url': _url,
            'startdate': _startdate,
            'latency': _latency,
        },
        'tmax': {
            'description': 'Daily maximum air temperature (C)',
            'pattern': 'daymet_tmax_*_???????.tif',
            'source': 'tmax.nc',
            'url': _url,
            'startdate': _startdate,
            'latency': _latency,
        },
        'prcp': {
            'description': 'Daily precipitation (mm)',
            'pattern': 'daymet_prcp_*_???????.tif',
            'source': 'prcp.nc',
            'url': _url,
            'startdate': _startdate,
            'latency': _latency,
        },
        'srad': {
            'description': 'Daily solar radiation (W m-2)',
            'pattern': 'daymet_srad_*_???????.tif',
            'source': 'srad.nc',
            'url': _url,
            'startdate': _startdate,
            'latency': _latency,
        },
        'vp': {
            'description': 'Daily vapor pressure (Pa)',
            'pattern': 'daymet_vp_*_???????.tif',
            'source': 'vp.nc',
            'url': _url,
            'startdate': _startdate,
            'latency': _latency,
        },
    }

    _defaultresolution = (1000., 1000.,)

    def __init__(self, filename):
        """ Inspect a single file and get some metadata """
        super(daymetAsset, self).__init__(filename)
        parts = basename(filename).split('_')
        self.sensor = 'daymet'
        self.asset = parts[1]
        self.tile = parts[2]
        self.date = datetime.datetime.strptime(parts[3], '%Y%j').date()
        self.products[self.asset] = filename


    @classmethod
    def query_provider(cls, asset, tile, date):
        """Determine availability of data for the given (asset, tile, date).

        Returns (basename, url) on success; (None, None) otherewise.
        Something of a no-op for daymet as the data is daily for the
        entire run of the dataset and the URLs are deterministic.
        """
        source = cls._assets[asset]['source']
        url = (cls._assets[asset]['url'] + '/%s') % (date.year, tile, date.year, source)
        bn = cls._basename_pat.format(asset, tile, date.year, date.strftime('%j'))
        return (bn, url)


    @classmethod
    def fetch(cls, asset, tile, date):
        """Fetch a daymet asset and convert it to a gips-friendly format."""
        asset_bn, url = cls.query_provider(asset, tile, date)

        dataset = open_url(url)
        x0 = dataset['x'].data[0] - 500.0
        y0 = dataset['y'].data[0] + 500.0
        iday = date.timetuple().tm_yday - 1
        var = dataset[asset]
        data = np.array(var.array[iday, :, :]).squeeze().astype('float32')
        ysz, xsz = data.shape
        description = cls._assets[asset]['description']
        meta = {'ASSET': asset, 'TILE': tile, 'DATE': str(date.date()), 'DESCRIPTION': description}
        # save the asset in the stage
        fout = os.path.join(cls.Repository.path('stage'), asset_bn)
        geo = [float(x0), cls._defaultresolution[0], 0.0, float(y0), 0.0, -cls._defaultresolution[1]]
        geo = np.array(geo).astype('double')
        dtype = create_datatype(data.dtype)
        imgout = gippy.GeoImage(fout, xsz, ysz, 1, dtype)
        imgout.SetBandName(asset, 1)
        imgout.SetNoData(-9999.)
        imgout.SetProjection(PROJ)
        imgout.SetAffine(geo)
        imgout[0].Write(data)    


class daymetData(Data):
    """ A tile of data (all assets and products) """
    name = 'Daymet'
    version = '0.1'
    Asset = daymetAsset

    _products = {
        'tmin': {
            'description': 'Daily minimum air temperature (C)',
            'assets': ['tmin']
        },
        'tmax': {
            'description': 'Daily maximum air temperature (C)',
            'assets': ['tmax']
        },
        'prcp': {
            'description': 'Daily precipitation (mm)',
            'assets': ['prcp']
        },
        'srad': {
            'description': 'Daily solar radiation (W m-2)',
            'assets': ['srad']
        },
        'vp': {
            'description': 'Daily vapor pressure (Pa)',
            'assets': ['vp']
        },
    }
