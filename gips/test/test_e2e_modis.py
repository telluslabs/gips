import logging

import pytest
import envoy
from scripttest import TestFileEnvironment

logger = logging

# where input and output files go; in other words everything but the data repo
SYSTEM_TEST_WD = "/home/tolson/src/gips/test" # TODO this is unused
DATA_REPO_ROOT = "/home/tolson/src/gips/data-root" # TODO this MUST be programmable
# TODO don't hardcode paths ----v
NH_SHP_PATH = '/home/tolson/src/gips/gips/test/NHseacoast.shp'
STD_ARGS = ('modis', '-s', NH_SHP_PATH,
            '-d', '2012-12-01,2012-12-10', '--fetch', '-v', '4')

@pytest.fixture
def setup_modis_data(pytestconfig):
    """Use gips_inventory to ensure presence of MODIS data in the data repo."""
    if not pytestconfig.getoption('setup_repo'):
        logger.debug("Skipping repo setup per lack of option.")
        return
    logger.info("Downloading MODIS data . . .")
    cmd_str = ("gips_inventory modis -s gips/test/NHseacoast.shp "
               "-d 2012-12-01,2012-12-10 --fetch -v 4")
    outcome = envoy.run(cmd_str)
    logger.info("MODIS data download complete.")
    if outcome.status_code != 0:
        raise RuntimeError("MODIS data setup via `gips_inventory` failed",
                           outcome.std_out, outcome.std_err, outcome)

@pytest.fixture
def test_file_environment():
    """Use scripttest to provide a directory for testing."""
    return TestFileEnvironment(DATA_REPO_ROOT, start_clear=False)

def test_e2e_process(setup_modis_data, test_file_environment):
    """Test gips_process on modis data."""
    logger.info('starting run')
    outcome = test_file_environment.run('gips_process', *STD_ARGS,
                                        expect_error=True)
    logger.info('run complete')

    # confirm files created but not deleted;
    # files_updated includes dirs whose contents have changed
    assert (bool(outcome.files_created)
            and bool(outcome.files_updated)
            and not bool(outcome.files_deleted))
