import logging, os

import pytest
import envoy

from .data import *
from .util import *

logger = logging.getLogger(__name__)

# changing this will require changes in expected_*_files below:
STD_ARGS       = ('modis', '-s', NH_SHP_PATH,
                  '-d', '2012-12-01,2012-12-03', '-v', '4')


@pytest.fixture
def setup_modis_data(pytestconfig):
    """Use gips_inventory to ensure presence of MODIS data in the data repo."""
    if not pytestconfig.getoption('setup_repo'):
        logger.debug("Skipping repo setup per lack of option.")
        return
    logger.info("Downloading MODIS data . . .")
    cmd_str = 'gips_inventory ' + ' '.join(STD_ARGS) + ' --fetch'
    outcome = envoy.run(cmd_str)
    logger.info("MODIS data download complete.")
    if outcome.status_code != 0:
        raise RuntimeError("MODIS data setup via `gips_inventory` failed",
                           outcome.std_out, outcome.std_err, outcome)


@slow
def test_inventory_fetch(test_file_environment):
    """Test gips_inventory --fetch; actually contacts data provider."""
    # only get data for one day to save time
    args = ('modis', '-s', NH_SHP_PATH,
            '-d', '2012-12-01,2012-12-01', '-v', '4', '--fetch')
    # check repo before run to see if it's cleaned out; remove DATA_REPO_ROOT
    # then run `gips_config env` to clean it (this could be done by the test
    # but if the user has files that are difficult to replace we don't want to
    # make assumptions about what we can destroy).
    before = set(test_file_environment._find_files().keys())
    expected = set(expected_inventory_fetch_created_files.keys())
    if before & expected:
        # TODO report on specifics
        raise RuntimeError('Output files found before test; repo '
                           'may not be clean.')
    expected = GipsProcResult(created=expected_inventory_fetch_created_files,
                              updated={'modis/stage': None, 'modis/tiles': None})
    logger.info('starting run')
    actual = test_file_environment.run('gips_inventory', *args)
    logger.info('run complete')
    assert expected == actual


def test_inventory(setup_modis_data, test_file_environment):
    """Test `gips_inventory modis` and confirm recorded output is given.

    This is currently the fastest test so if you want to run this file to
    confirm its sanity without running a bunch of slow tests, do this:
        $ py.test gips/test/test_e2e_modis.py::test_inventory
    """
    expected = GipsProcResult(stdout=expected_inventory_stdout)
    actual = test_file_environment.run('gips_inventory', *STD_ARGS)
    assert expected == actual


def test_process(setup_modis_data, test_file_environment):
    """Test gips_process on modis data."""
    expected = GipsProcResult(created=expected_process_created_files,
                              updated={'modis/tiles/h12v04/2012336': None,
                                       'modis/tiles/h12v04/2012337': None,
                                       'modis/tiles/h12v04/2012338': None})
    logger.info('starting run')
    actual = test_file_environment.run('gips_process', *STD_ARGS)
    logger.info('run complete')
    assert expected == actual


def test_info(test_file_environment):
    """Test `gips_info modis` and confirm recorded output is given."""
    actual = test_file_environment.run('gips_info', 'modis')
    expected = GipsProcResult(stdout=expected_info_stdout)
    assert expected == actual


def test_project(setup_modis_data, keep_data_repo_clean, output_tfe):
    """Test gips_project modis with warping."""
    expected = GipsProcResult(created=expected_project_created_files)
    args = STD_ARGS + ('--res', '100', '100', '--outdir', OUTPUT_DIR, '--notld')
    logger.info('starting run')
    actual = output_tfe.run('gips_project', *args)
    logger.info('run complete')
    assert expected == actual


def test_project_two_runs(setup_modis_data, keep_data_repo_clean, output_tfe):
    """As test_project, but run twice to confirm idempotence of gips_project.

    The data repo is only cleaned up after both runs are complete; this is
    intentional as changes in the data repo may influence gips_project.
    """
    args = STD_ARGS + ('--res', '100', '100',
                       '--outdir', OUTPUT_DIR, '--notld')

    logger.info('starting first run: gips_project ' + ' '.join(args))
    actual = output_tfe.run('gips_project', *args)
    logger.info('first run complete')

    # confirm generated files match expected fingerprints
    expected = GipsProcResult(created=expected_project_created_files)
    assert 'initial test_project run' and expected == actual

    logger.info('starting second run: gips_project ' + ' '.join(args))
    actual = output_tfe.run('gips_project', *args)
    logger.info('second run complete')

    # confirm generated files match expected fingerprints
    expected = GipsProcResult()
    assert 'final test_project run' and expected == actual


def test_project_no_warp(setup_modis_data, keep_data_repo_clean, output_tfe):
    """Test gips_project modis without warping."""
    expected = GipsProcResult(created=expected_project_no_warp_created_files)
    args = STD_ARGS + ('--outdir', OUTPUT_DIR, '--notld')
    logger.info('starting run')
    actual = output_tfe.run('gips_project', *args)
    logger.info('run complete')
    assert expected == actual


def test_tiles(setup_modis_data, keep_data_repo_clean, output_tfe):
    """Test gips_tiles modis with warping."""
    # TODO there should be something here but nothing is saved here during manual runs.
    expected = GipsProcResult(created={'h12v04': None})
    args = STD_ARGS + ('--outdir', OUTPUT_DIR, '--notld')
    logger.info('starting run')
    actual = output_tfe.run('gips_tiles', *args)
    logger.info('run complete')
    assert expected == actual


def test_tiles_copy(setup_modis_data, keep_data_repo_clean, output_tfe):
    """Test gips_tiles modis with copying."""
    expected = GipsProcResult(created=expected_tiles_copy_created_files)
    # doesn't quite use STD_ARGS
    args = ('modis', '-t', 'h12v04', '-d', '2012-12-01,2012-12-03', '-v', '4',
            '--outdir', OUTPUT_DIR, '--notld')
    logger.info('starting run')
    actual = output_tfe.run('gips_tiles', *args)
    logger.info('run complete')
    assert expected == actual


def test_stats(setup_modis_data, keep_data_repo_clean, output_tfe):
    """Test gips_stats on projected files."""
    expected = GipsProcResult(created=expected_stats_created_files)

    # generate data needed for stats computation
    args = STD_ARGS + ('--res', '100', '100', '--outdir', OUTPUT_DIR, '--notld')
    prep_run = output_tfe.run('gips_project', *args)
    assert prep_run.exit_status == 0 # confirm it worked; not really in the test

    # compute stats
    gtfe = GipsTestFileEnv(OUTPUT_DIR, start_clear=False)
    actual = gtfe.run('gips_stats', OUTPUT_DIR)

    # check for correct stats content
    assert expected == actual
