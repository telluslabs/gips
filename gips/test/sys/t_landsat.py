import logging

import envoy
import pytest

from .util import *

logger = logging.getLogger(__name__)

# changing this will require changes in expected/
STD_ARGS = ('landsat', '-s', NH_SHP_PATH, '-d', '2015-352', '-v', '4')

product_args = tuple('-p acca bqashadow ref-toa ndvi-toa rad-toa'.split())

@pytest.fixture
def setup_landsat_data(pytestconfig):
    """Use gips_inventory to ensure presence of MODIS data in the data repo."""
    driver = 'landsat'
    if not pytestconfig.getoption('setup_repo'):
        logger.info("Skipping repo setup per lack of option.")
        return
    cmd_str = 'gips_inventory ' + ' '.join(STD_ARGS) + ' --fetch'
    logger.info("Downloading data via `{}`".format(cmd_str))
    outcome = envoy.run(cmd_str)
    logger.info("{} data download complete.".format(driver))
    if outcome.status_code != 0:
        raise RuntimeError("{} data setup via `gips_inventory` failed".format(driver),
                           outcome.std_out, outcome.std_err, outcome)


def t_info(repo_env, expected):
    """Test `gips_info modis` and confirm recorded output is given."""
    actual = repo_env.run('gips_info', 'landsat')
    assert expected == actual


def t_inventory(setup_landsat_data, repo_env, expected):
    """Test `gips_inventory` to confirm it notices the emplaced data file."""
    actual = repo_env.run('gips_inventory', *STD_ARGS)
    assert expected == actual

@slow
def t_process(setup_landsat_data, repo_env, expected):
    """Test gips_process on landsat data."""
    PROCESS_ARGS = STD_ARGS + product_args
    actual = repo_env.run('gips_process', *PROCESS_ARGS)
    # can't use `expected == actual`; it emits nondeterministic strings on stderr
    # TODO make it not do that for normal operations ^^^
    assert expected.created == actual.created
