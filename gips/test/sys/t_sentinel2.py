import logging
from datetime import datetime

import pytest
import envoy

from .util import *

logger = logging.getLogger(__name__)

pytestmark = sys # skip everything unless --sys

driver = 'sentinel2'

# changing this will require changes in expected/
# dates chosen for relative lack of cloud cover ------------vvv------vvv
STD_ARGS = ('sentinel2', '-s', DURHAM_SHP_PATH, '-d', '2017-010,2017-030', '-v', '4')
# for now sentinel2 only supports top-of-atmo products
PROD_ARGS = list(STD_ARGS) + ['-p', 'ref-toa', 'ndvi-toa', 'evi-toa', 'lswi-toa', 'ndsi-toa', 'bi-toa']

@pytest.fixture
def setup_fixture(pytestconfig):
    """Use gips_inventory to ensure presence of data in the data repo."""
    if not pytestconfig.getoption('setup_repo'):
        logger.debug("Skipping repo setup per lack of option.")
        return
    logger.info("Downloading Sentinel 2 data . . .")
    cmd_str = 'gips_inventory ' + ' '.join(STD_ARGS) + ' --fetch'
    outcome = envoy.run(cmd_str)
    logger.info("Data download complete.")
    if outcome.status_code != 0:
        raise RuntimeError("Data setup via `gips_inventory` failed",
                           outcome.std_out, outcome.std_err, outcome)


def t_inventory(setup_fixture, repo_env, expected):
    """Test `gips_inventory` and confirm recorded output is given."""
    actual = repo_env.run('gips_inventory', *STD_ARGS)
    assert expected == actual


def t_process(setup_fixture, repo_env, expected):
    """Test `gips_process`, confirming products are created."""
    process_actual = repo_env.run('gips_process', *PROD_ARGS)
    # TODO envoy doesn't respect --expectation-format the way repo_env does
    inventory_actual = envoy.run('gips_inventory ' + ' '.join(STD_ARGS))
    assert (expected == process_actual
            and expected._inv_stdout == inventory_actual.std_out)


def t_info(repo_env, expected):
    """Test `gips_info` and confirm recorded output is given."""
    actual = repo_env.run('gips_info', driver)
    assert expected == actual
