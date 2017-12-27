from __future__ import print_function

import pytest
import sh

import util
from util import export_wrapper
import driver_setup

# 'driver': {'product': [ (path, type, data...),...]...}
from expected.std_stats import expectations

@pytest.mark.parametrize("driver, product",
                         util.params_from_expectations(expectations))
def t_stats(export_wrapper, driver, product):
    """Test gips_stats on projected files."""
    record_mode, runner, working_dir = export_wrapper

    # generate data needed for stats computation
    args = driver_setup.STD_ARGS[driver] + ('--res', '100', '100', '--notld',
                            '--outdir', working_dir, '-p', product)
    outcome = sh.gips_project(*args)
    assert outcome.exit_code == 0 # sanity check

    # compute & confirm stats
    outcome, actual = runner('gips_stats', working_dir, '-p', product)
    if not record_mode:
        assert (outcome.exit_code == 0
                and expectations[driver][product] == actual)
