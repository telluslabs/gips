from __future__ import print_function

import datetime

import pytest
import sh

import util

nh_shp = util.NH_SHP_PATH

STD_ARGS = {
    'modis': ('modis', '-s', nh_shp, '-d', '2012-12-01,2012-12-03', '-v', '4'),
    'merra': ('merra', '-s', nh_shp, '-d', '2015-135', '-v', '4'),
    'aod':   ('aod',   '-s', nh_shp, '-d', '2017-004,2017-006', '-v', '4'),
    'prism': ('prism', '-s', nh_shp, '-d', '1982-12-01,1982-12-03', '-v4'),
}

setup_attempted = []

def setup_repo_data(driver):
    """Use gips_inventory to ensure assets are present."""
    if driver in setup_attempted:
        print(driver, "setup already attempted; skipping.")
        return
    setup_attempted.append(driver)
    if not pytest.config.getoption('setup_repo'):
        print("Skipping", driver, "repo setup per lack of option.")
        return
    # handle modis scheduled downtime case
    if driver == 'modis' and datetime.datetime.today().date().weekday() == 2:
        raise RuntimeError("It's Wednesday; modis downloads are likely to fail.")
    print('Downloading', driver, 'data . . .')
    args = STD_ARGS[driver] + ('--fetch',)
    outcome = sh.Command('gips_inventory')(*args)
    if outcome.exit_code != 0:
        raise RuntimeError(driver + " data setup via `gips_inventory` failed",
                           outcome)
    print(driver, "data download complete.")
