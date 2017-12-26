import logging

import pytest
import envoy # deprecated
import sh

from .util import *

logger = logging.getLogger(__name__)

pytestmark = sys  # skip everything unless --sys

# changing this will require changes in expected/
driver = 'merra'
STD_TILE = 'h01v01'
STD_DATES = '2015-135'
STD_ARGS = (driver, '-s', NH_SHP_PATH, '-d', STD_DATES, '-v', '4')

@pytest.fixture
def setup_merra_data(pytestconfig):
    """Use gips_inventory to ensure presence of MERRA2 data in the data repo."""
    if not pytestconfig.getoption('setup_repo'):
        logger.debug("Skipping repo setup per lack of option.")
        return
    cmd_str = 'gips_inventory ' + ' '.join(STD_ARGS) + ' --fetch'
    logger.info("Downloading MERRA assets with " + cmd_str)
    outcome = envoy.run(cmd_str)
    logger.info("MERRA data download complete.")
    if outcome.status_code != 0:
        raise RuntimeError("merra data setup via `gips_inventory` failed",
                           outcome.std_out, outcome.std_err, outcome)

setup_fixture = setup_merra_data

# ###   SHOULD BE STANDARD BELOW HERE #####

# TODO revive this test?
'''
def t_project_no_warp(setup_fixture, clean_repo_env, output_tfe, expected):
    """Test gips_project {} without warping.""".format(driver)
    args = STD_ARGS + ('--outdir', OUTPUT_DIR, '--notld')
    actual = output_tfe.run('gips_project', *args)
    assert expected == actual
'''

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
