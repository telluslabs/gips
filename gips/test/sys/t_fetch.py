import pytest

import util
from util import repo_wrapper
import driver_setup

# 'driver': {'product': [ (path, type, data...),...]...}
from expected.std_fetch import expectations

pytestmark = util.sys # skip everything unless --sys

params = util.params_from_expectations(expectations)
@pytest.mark.parametrize("driver", params)
def t_fetch(repo_wrapper, driver):
    """Test gips_inventory --fetch output."""
    try:
        driver_setup.special_cases(driver)
    except CannotFetch as cf:
        print(cf)
        return

    record_mode, runner = repo_wrapper
    #driver_setup.setup_repo_data(driver)
    args = ('gips_inventory',) + driver_setup.STD_ARGS[driver] + ('--fetch',)
    outcome, actual = runner(*args)
    if not record_mode: # don't evaluate assertions when in record-mode
        assert (outcome.exit_code == 0
                and expectations[driver] == actual)
