import logging
from datetime import datetime

import pytest
import envoy

from .util import *

logger = logging.getLogger(__name__)

pytestmark = sys # skip everything unless --sys

driver = 'merra'

# changing this will require changes in expected/
STD_ARGS = ('merra', '-s', NH_SHP_PATH, '-d', '1980-01-01,1980-01-02', '-v', '4')

@pytest.fixture
def setup_merra_data(pytestconfig):
    """Use gips_inventory to ensure presence of MERRA data in the data repo."""
    if not pytestconfig.getoption('setup_repo'):
        logger.debug("Skipping repo setup per lack of option.")
        return
    logger.info("Downloading MERRA data . . .")
    cmd_str = 'gips_inventory ' + ' '.join(STD_ARGS) + ' --fetch'
    outcome = envoy.run(cmd_str)
    logger.info("MERRA data download complete.")
    if outcome.status_code != 0:
        raise RuntimeError("MERRA data setup via `gips_inventory` failed",
                           outcome.std_out, outcome.std_err, outcome)


def t_inventory(setup_merra_data, repo_env, expected):
    """Test `gips_inventory merra` and confirm recorded output is given."""
    actual = repo_env.run('gips_inventory', *STD_ARGS)
    assert expected == actual


def t_process(setup_merra_data, repo_env, expected):
    """Test gips_process on merra data."""
    actual = repo_env.run('gips_process', *STD_ARGS)
    assert expected == actual


def t_info(repo_env, expected):
    """Test `gips_info modis` and confirm recorded output is given."""
    actual = repo_env.run('gips_info', 'merra')
    assert expected == actual


def t_project(setup_modis_data, clean_repo_env, output_tfe, expected):
    """Test gips_project merra with warping."""
    args = STD_ARGS + ('--res', '100', '100', '--outdir', OUTPUT_DIR, '--notld')
    actual = output_tfe.run('gips_project', *args)
    assert expected == actual


def t_project_two_runs(setup_merra_data, clean_repo_env, output_tfe, expected):
    """As test_project, but run twice to confirm idempotence of gips_project.

    The data repo is only cleaned up after both runs are complete; this is
    intentional as changes in the data repo may influence gips_project.
    """
    args = STD_ARGS + ('--res', '100', '100',
                       '--outdir', OUTPUT_DIR, '--notld')

    actual = output_tfe.run('gips_project', *args)
    assert 'initial test_project run' and expected == actual

    actual = output_tfe.run('gips_project', *args)
    expected.created = {} # no created files on second run
    assert 'final test_project run' and expected == actual


def t_project_no_warp(setup_merra_data, clean_repo_env, output_tfe, expected):
    """Test gips_project merra without warping."""
    args = STD_ARGS + ('--outdir', OUTPUT_DIR, '--notld')
    actual = output_tfe.run('gips_project', *args)
    assert expected == actual


def t_tiles(setup_modis_data, clean_repo_env, output_tfe, expected):
    """Test gips_tiles modis with warping."""
    args = STD_ARGS + ('--outdir', OUTPUT_DIR, '--notld')
    actual = output_tfe.run('gips_tiles', *args)
    assert expected == actual


def t_tiles_copy(setup_merra_data, clean_repo_env, output_tfe, expected):
    """Test gips_tiles merra with copying."""
    # doesn't quite use STD_ARGS
    args = ('merra', '-t', 'h12v04', '-d', '1980-01-01,1980-01-02', '-v', '4',
            '--outdir', OUTPUT_DIR, '--notld')
    actual = output_tfe.run('gips_tiles', *args)
    assert expected == actual


def t_stats(setup_merra_data, clean_repo_env, output_tfe, expected):
    """Test gips_stats on projected files."""
    # generate data needed for stats computation
    args = STD_ARGS + ('--res', '100', '100', '--outdir', OUTPUT_DIR, '--notld')
    prep_run = output_tfe.run('gips_project', *args)
    assert prep_run.exit_status == 0 # confirm it worked; not really in the test

    # compute stats
    gtfe = GipsTestFileEnv(OUTPUT_DIR, start_clear=False)
    actual = gtfe.run('gips_stats', OUTPUT_DIR)

    # check for correct stats content
    assert expected == actual
