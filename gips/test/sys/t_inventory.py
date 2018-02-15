import pytest
import sh

import util
import driver_setup

pytestmark = util.sys # skip everything unless --sys


ARGS = driver_setup.STD_ARGS['modisndti']
core_data_inv_params = (
    ('modisndti', 'ndti', ARGS[4], ARGS[4].split('-')[-1]),
    ('modisndti', 'ndti', '2012-333', 'No matching files in inventory'),
)
# expectations = {
#     'modisndti': {
#         'ndti': []
#     }
# }

@pytest.mark.parametrize("driver, product, datespec, expected", core_data_inv_params)
def t_data_core_Data_inventory(driver, product, datespec, expected):
    """Test gips_process output."""
    global ARGS
    driver_setup.setup_repo_data(driver)
    outcome = sh.gips_inventory(ARGS[:3] + ('-d', datespec) + ('-p', product))
    assert (outcome.exit_code == 0 and expected in outcome.stdout)
