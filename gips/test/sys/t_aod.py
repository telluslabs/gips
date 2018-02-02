import logging

import pytest
import envoy

from .util import *

logger = logging.getLogger(__name__)

pytestmark = sys  # skip everything unless --sys

# changing this will require changes in expected/
driver = 'aod'
STD_TILE = 'h01v01'
STD_DATES = '2017-004,2017-006'
STD_ARGS = (driver, '-s', NE_SHP_PATH, '-d', STD_DATES, '-v', '4', '-p', 'aod' )


@pytest.fixture
def setup_driver_data(pytestconfig):
    """
    Use gips_inventory to ensure presence of driver data in the data repo.
    """
    if not pytestconfig.getoption('setup_repo'):
        logger.debug("Skipping repo setup per lack of option.")
        return
    logger.info("Downloading {} data . . .".format(driver.upper()))
    cmd_str = 'gips_inventory ' + ' '.join(STD_ARGS) + ' --fetch'
    outcome = envoy.run(cmd_str)
    logger.info("{} data download complete.".format(driver.upper()))
    if outcome.status_code != 0:
        raise RuntimeError("{} data setup via `gips_inventory` failed"
                           .format(driver),
                           outcome.std_out, outcome.std_err, outcome)


setup_fixture = setup_driver_data

# ###   SHOULD BE STANDARD BELOW HERE #####


def t_project_no_warp(setup_fixture, clean_repo_env, output_tfe, expected):
    """Test gips_project {} without warping.""".format(driver)
    args = STD_ARGS + ('--outdir', OUTPUT_DIR, '--notld')
    actual = output_tfe.run('gips_project', *args)
    assert expected == actual


# Haven't used gips_tiles ever
def t_tiles(setup_fixture, clean_repo_env, output_tfe, expected):
    """Test gips_tiles {} with warping.""".format(driver)
    args = STD_ARGS + ('--outdir', OUTPUT_DIR, '--notld')
    actual = output_tfe.run('gips_tiles', *args)
    assert expected == actual


def t_tiles_copy(setup_fixture, clean_repo_env, output_tfe, expected):
    """Test gips_tiles {} with copying.""".format(driver)
    # doesn't quite use STD_ARGS
    args = (driver, '-t', STD_TILE, '-d', STD_DATES, '-v', '4',
            '--outdir', OUTPUT_DIR, '--notld')
    actual = output_tfe.run('gips_tiles', *args)
    assert expected == actual
