from __future__ import print_function

import datetime
import ftplib
import tempfile
import shutil
import os

import pytest
import sh

import util

nh_shp = util.NH_SHP_PATH

STD_ARGS = {
    'modis': ('modis', '-s', nh_shp, '-d', '2012-12-01,2012-12-03', '-v', '4'),
    'merra': ('merra', '-s', nh_shp, '-d', '2015-135', '-v', '4'),
    'prism': ('prism', '-s', nh_shp, '-d', '1982-12-01,1982-12-03', '-v4'),
    'landsat': ('landsat', '-s', nh_shp, '-d', '2017-08-01', '-v4'),
    # Here down, not NH shapefile:
    'aod': ('aod', '-s', util.NE_SHP_PATH, '-d', '2017-004,2017-006', '-v4'),
    'sentinel2': ('sentinel2', '-s', util.DURHAM_SHP_PATH, '-d2017-010', '-v4'),
    'sar': ('sar', '-t', 'N07E099', 'N19E100', 'N00E099', '-d2009,2015', '-v4'),
}

class CannotFetch(Exception):
    pass


sar_asset_fns = [
    'KC_017-C25N00E099WB1ORSA1.tar.gz',
    'KC_017-Y10N19E100FBDORSA1.tar.gz',
    'KC_999-C019DRN07E099WBDORSA1.tar.gz',
]

def special_cases(driver):
    # handle modis scheduled downtime case
    if driver == 'modis' and datetime.datetime.today().date().weekday() == 2:
        raise RuntimeError("It's Wednesday; modis downloads are likely to fail.")
    # sar isn't fetchable; get it from the artifact server
    # TODO emplace sar assets in the existing collection of system test artifacts
    # and write code that works for all of these artifacts
    if driver == 'sar':
        username = pytest.config.getini('artifact-store-user')
        password = pytest.config.getini('artifact-store-password')
        host     = pytest.config.getini('artifact-store-host')
        path     = pytest.config.getini('artifact-store-path')
        url_head = 'ftp://{}:{}@{}/{}/{}/'.format(
                                        username, password, host, path, driver)
        bookmark = os.getcwd()
        try:
            temp_dir = tempfile.mkdtemp()
            os.chdir(temp_dir)
            [sh.wget(url_head + fn) for fn in sar_asset_fns]
            sh.gips_archive('sar')
        finally:
            os.chdir(bookmark)
            shutil.rmtree(temp_dir)

        # sar fetch currently doesn't work; this fails:
        # gips_inventory sar -t N07E099 N19E100 N00E099 -d 2009,2015 -v 4 --fetch
        raise CannotFetch("sar assets can't be fetched (reason TBD);"
                          " used artifact server.")

setup_attempted = []

def setup_repo_data(driver):
    """Use gips_inventory to ensure assets are present."""
    if driver in setup_attempted or not pytest.config.getoption('setup_repo'):
        return
    setup_attempted.append(driver)
    try:
        special_cases(driver)
    except CannotFetch as cf:
        print(cf)
        return

    print('Downloading', driver, 'data . . .')
    args = STD_ARGS[driver] + ('--fetch',)
    outcome = sh.Command('gips_inventory')(*args)
    print(driver, "data download complete.")
