import pytest

import util
from util import export_wrapper
import driver_setup

# 'driver': {'product': [ (path, type, data...),...]...}
from expected.std_project import expectations

@pytest.mark.parametrize("driver, product",
                         util.params_from_expectations(expectations))
def t_project(export_wrapper, driver, product):
    """Test gips_project with warping."""
    record_mode, runner = export_wrapper
    args = ('gips_project',) + driver_setup.STD_ARGS[driver] + (
        '--res', '100', '100', '--outdir', util.OUTPUT_DIR, '--notld',
        '-p', product)
    outcome, actual = runner(*args)
    if not record_mode: # don't evaluate assertions when in record-mode
        assert (outcome.exit_code == 0
                and expectations[driver][product] == actual)
