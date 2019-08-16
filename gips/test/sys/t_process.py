import pytest

from . import util
from .util import repo_wrapper
from . import driver_setup

# 'driver': {'product': [ (path, type, data...),...]...}
from .expected.std_process import expectations, mark_spec

pytestmark = util.sys # skip everything unless --sys

params = util.params_from_expectations(expectations, mark_spec)

@pytest.mark.parametrize("driver, product", params)
def t_process(repo_wrapper, driver, product):
    """Test gips_process output."""
    record_mode, runner = repo_wrapper
    driver_setup.setup_repo_data(driver)
    args = ('gips_process',) + driver_setup.STD_ARGS[driver] + ('-p', product)
    outcome, actual = runner(*args)
    if not record_mode: # don't evaluate assertions when in record-mode
        assert (outcome.exit_code == 0
                and expectations[driver][product] == actual)
