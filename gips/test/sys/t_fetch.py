import pytest

from . import util
from .util import repo_wrapper
from . import driver_setup

# 'driver': {'product': [ (path, type, data...),...]...}
from .expected.std_fetch import expectations, mark_spec

pytestmark = util.sys # skip everything unless --sys

#params = util.params_from_expectations(expectations, mark_spec)



@pytest.mark.parametrize("driver", expectations.keys())
def t_fetch(repo_wrapper, driver):
    """Test gips_inventory --fetch."""
    record_mode, runner = repo_wrapper
    # filter out the hack put in for sentinel-2:
    driver_args = tuple(a for a in driver_setup.STD_ARGS[driver] if a != '--overwrite')
    args = ('gips_inventory',) + driver_args + ('--fetch',)
    outcome, actual = runner(*args)
    if not record_mode: # don't evaluate assertions when in record-mode
        assert (outcome.exit_code == 0
                and expectations[driver] == actual)
