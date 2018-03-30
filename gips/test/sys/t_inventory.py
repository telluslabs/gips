import pytest
import sh
import os

import util
import driver_setup

pytestmark = util.sys # skip everything unless --sys

ARGS = driver_setup.STD_ARGS['modisndti']
SITE = ARGS[2]
RASTERMASK = '/tmp/{}.tif'.format(os.path.basename(SITE))
DATE = ARGS[4]
sh.gdal_rasterize('-at -burn 1 -a_nodata 0 -init 0 -ot Byte'
                  ' -tr 463 463 {} {}'
                  .format(SITE, RASTERMASK).split(' '))

inv_cli_params = (
    ('modisndti', SITE, 'ndti', DATE, DATE.split('-')[-1]),
    ('modisndti', SITE, 'ndti', '2012-333', 'No matching files in inventory'),
    ('modisndti', RASTERMASK, 'ndti', DATE, DATE.split('-')[-1]),
    ('modisndti', RASTERMASK, 'ndti', '2012-333', 'No matching files in inventory'),
)
inv_api_params = (
    tuple((tup[:-1] + (i,) for (tup, i) in zip(inv_cli_params, (1, 0, 1, 0))))
)


@pytest.mark.parametrize("driver, spatial, product, datespec, expected", inv_cli_params)
def t_cli_inventory(driver, spatial, product, datespec, expected):
    """Test gips_inventory for different CLI parameter combinations."""
    driver_setup.setup_repo_data(driver)
    spat_opt = '-r' if spatial.endswith('.tif') else '-s'
    outcome = sh.gips_inventory(
        ('modis', spat_opt, spatial, '-d', datespec, '-p', product)
    )
    assert (outcome.exit_code == 0 and expected in outcome.stdout)


@pytest.mark.django_db
@pytest.mark.parametrize("driver, spatial, product, datespec, expected", inv_api_params)
def t_api_inventory(driver, spatial, product, datespec, expected):
    """
    Test gips.data.core.Data.inventory for different API parameter
    combinations.
    """
    driver_setup.setup_repo_data(driver)
    from gips.data.modis import modisData, modisAsset
    from gips.inventory import orm
    import gips.inventory.dbinv.api as api

    orm.setup()
    api.rectify_assets(modisAsset)
    r = spatial if spatial.endswith('.tif') else None
    s = spatial if r is None else None
    inv = modisData.inventory(
        site=s, rastermask=r, dates=datespec, products=[product],
    )
    assert len(inv.dates) == expected
