from __future__ import print_function

import pytest
import sh

import util
from util import export_wrapper
import driver_setup

pytestmark = util.sys # skip everything unless --sys

# 'driver': {'product': [ (path, type, data...),...]...}
from expected.std_stats import expectations, mark_spec

@pytest.mark.parametrize("driver, product",
                         util.params_from_expectations(expectations, mark_spec))
def t_stats(export_wrapper, driver, product):
    """Test gips_stats on projected files."""
    record_mode, runner, working_dir = export_wrapper

    driver_setup.setup_repo_data(driver)

    # generate data needed for stats computation
    args = driver_setup.STD_ARGS[driver] + ('--res', '100', '100', '--notld',
                            '--outdir', working_dir, '-p', product)
    print('prepping for stats:', 'gips_project', *args)
    outcome = sh.gips_project(*args)

    # compute & confirm stats
    outcome, actual = runner('gips_stats', working_dir, '-p', product)
    if not record_mode:
        assert (outcome.exit_code == 0
                and expectations[driver][product] == actual)
