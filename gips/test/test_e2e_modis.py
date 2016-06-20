import logging
import pytest
import envoy

logger = logging

# where input and output files go; in other words everything but the data repo
SYSTEM_TEST_WD = "system-test-wd"

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

def test_e2e_modis_normal_case(setup_modis_data):
    """."""
