"""Integration tests for core functions, such as those found in gips.core and gips.data.core."""

import os

from gips.data.landsat import landsat
from gips.data.modis import modis
from gips.data.sentinel2 import sentinel2
from gips.data.merra import merra

def t_make_temp_proc_dir():
    """Test Data.make_temp_proc_dir:

    Confirm creation of tempdir in stage/ with the right name, and
    destruction of same on context exit.
    """
    lsd = landsat.landsatData(search=False)
    with lsd.make_temp_proc_dir() as tempdir:
        tempdir_existed = os.path.exists(tempdir)

    # confirm was here, now it's gone, and had the right name
    dir_prefix = lsd.Repository.path('stage') + '/proc'
    assert tempdir_existed and not os.path.exists(tempdir) and tempdir.startswith(dir_prefix)


def t_get_geometry_landsat():
    """Test Asset.get_geometry:

    Confirm that a landsat asset can retrieve correct geometry.
    """
    asset_name = 'LE07_L1TP_012030_20170521_20170616_01_T1.tar.gz'
    expected = ("POLYGON ((108.8335 79.1226165284883,109.092717989112 "
                "79.0632647998117,109.566 78.9549,109.409193979199 "
                "78.9304760391032,108.8335 78.8408064768977,103.645842853291 "
                "78.0327817936009,103.506 78.011,97.6962458591181 "
                "79.192889924327,97.6785 79.1965,97.8200162657159 "
                "79.2205408109837,97.9773877740876 "
                "79.2472751137004,100.965474350711 "
                "79.7548918475664,102.431954328297 "
                "80.0040177538656,103.579758537076 "
                "80.1990069580392,103.730968501405 "
                "80.2246945364452,103.848884340444 "
                "80.2447261023149,103.897 80.2529,103.91859893174 "
                "80.2479546104429,108.8335 79.1226165284883))")
    la = landsat.landsatAsset(asset_name)
    actual = la.get_geometry()
    assert expected == actual


def t_get_geometry_modis():
    """Test Asset.get_geometry:

    Confirm that a modis asset can retrieve correct geometry.
    """
    asset_name = 'MOD09Q1.A2017145.h12v04.006.2017154032124.hdf'
    expected = ("POLYGON ((-6316297.66666667 4434443.0,-6686668 "
                "4434443,-6686668 5545554,-6316297.66666667 "
                "5545554.0,-5945927.33333333 5545554.0,-5575557 "
                "5545554,-5575557 4434443,-5945927.33333333 "
                "4434443.0,-6316297.66666667 4434443.0))")
    ma = modis.modisAsset(asset_name)
    actual = ma.get_geometry()
    assert expected == actual


def t_get_geometry_sentinel2():
    """Test Asset.get_geometry:

    Confirm that a sentinel2 asset can retrieve correct geometry.
    """
    asset_name = 'S2A_MSIL1C_20170719T170851_N0205_R112_T14TQM_20170719T172046.zip'
    expected = ("POLYGON ((-96.569289547 42.4269119955,-95.2368635673 "
                "42.3908806617,-95.2944377015 41.4040347455,-96.6065392232 "
                "41.4388462443,-96.569289547 42.4269119955))")
    s2a = sentinel2.sentinel2Asset(asset_name)
    actual = s2a.get_geometry()
    assert expected == actual


def t_get_geometry_merra():
    """Test Asset.get_geometry:

    Confirm that a merra asset can retrieve correct geometry.
    """
    asset_name = 'MERRA2_400.tavg1_2d_flx_Nx.20170521.nc4'
    expected = ("POLYGON ((-180 90,180 90,180 -90,-180 -90,-180 90))")
    ma = merra.merraAsset(asset_name)
    actual = ma.get_geometry()
    assert expected == actual
