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
        raise RuntimeError('Output files found before test; repo '
                           'may not be clean.')

    logger.info('starting run')
    outcome = test_file_environment.run('gips_inventory', *args)
    logger.info('run complete')

    # repo should now have specific new files with the right content
    detected_files = extract_hashes(outcome.files_created)

    assert (outcome.returncode == 0
            and not outcome.stderr
            and not outcome.files_deleted
            and expected_inventory_fetch_created_files == detected_files)


def test_inventory(setup_modis_data, test_file_environment):
    """Test `gips_inventory modis` and confirm recorded output is given.

    This is currently the fastest test so if you want to run this file to
    confirm its sanity without running a bunch of slow tests, do this:
        $ py.test gips/test/test_e2e_modis.py::test_inventory
    """
    outcome = test_file_environment.run('gips_inventory', *STD_ARGS)
    assert (outcome.returncode == 0
            and not outcome.stderr
            and not outcome.files_created
            and not outcome.files_updated
            and not outcome.files_deleted
            and expected_inventory_stdout == outcome.stdout)


def test_process(setup_modis_data, test_file_environment):
    """Test gips_process on modis data."""
    logger.info('starting run')
    outcome = test_file_environment.run('gips_process', *STD_ARGS)
    logger.info('run complete')

    # extract the checksum from each found file
    detected_files = extract_hashes(outcome.files_created)
    # repo should now have specific new files with the right content
    # TODO refactor this into four separate tests that DO NOT repeat the
    # gips_process command; need this because 'and' is lazy so not all branches
    # are being evaluated (and thus reported-on).
    assert (outcome.returncode == 0
            and not outcome.stderr
            and not outcome.files_deleted
            and expected_process_created_files == detected_files)


def test_info(test_file_environment):
    """Test `gips_info modis` and confirm recorded output is given."""
    outcome = test_file_environment.run('gips_info', 'modis')
    assert (outcome.returncode == 0
            and not outcome.stderr
            and not outcome.files_created
            and not outcome.files_updated
            and not outcome.files_deleted
            and outcome.stdout == expected_info_stdout)


def test_project(setup_modis_data, keep_data_repo_clean, output_tfe):
    """Test gips_project modis with warping."""
    args = STD_ARGS + ('--res', '100', '100',
                       '--outdir', OUTPUT_DIR, '--notld')
    logger.info('starting run')
    outcome = output_tfe.run('gips_project', *args)
    logger.info('run complete')

    # confirm generated files match expected fingerprints
    detected_files = extract_hashes(outcome.files_created)
    assert (outcome.returncode == 0
            and not outcome.stderr
            and not outcome.files_deleted
            and expected_project_created_files == detected_files)


def test_project_two_runs(setup_modis_data, keep_data_repo_clean, output_tfe):
    """As test_project, but run twice to confirm idempotence of gips_project.

    The data repo is only cleaned up after both runs are complete; this is
    intentional as changes in the data repo may influence gips_project.
    """
    args = STD_ARGS + ('--res', '100', '100',
                       '--outdir', OUTPUT_DIR, '--notld')

    logger.info('starting first run: gips_project ' + ' '.join(args))
    outcome = output_tfe.run('gips_project', *args)
    logger.info('first run complete')

    # confirm generated files match expected fingerprints
    detected_files = extract_hashes(outcome.files_created)
    assert ('initial test_project run'
            and outcome.returncode == 0
            and not outcome.stderr
            and not outcome.files_deleted
            and expected_project_created_files == detected_files)

    logger.info('starting second run: gips_project ' + ' '.join(args))
    outcome = output_tfe.run('gips_project', *args)
    logger.info('second run complete')

    # confirm generated files match expected fingerprints
    detected_files = extract_hashes(outcome.files_created)
    assert ('final test_project run'
            and outcome.returncode == 0
            and not outcome.stderr
            and not outcome.files_deleted
            and not detected_files) # shouldn't create any files this time


def test_project_no_warp(setup_modis_data, keep_data_repo_clean, output_tfe):
    """Test gips_project modis without warping."""
    args = STD_ARGS + ('--outdir', OUTPUT_DIR, '--notld')
    logger.info('starting run')
    outcome = output_tfe.run('gips_project', *args)
    logger.info('run complete')

    # confirm generated files match expected fingerprints
    detected_files = extract_hashes(outcome.files_created)
    assert (outcome.returncode == 0
            and not outcome.stderr
            and not outcome.files_deleted
            and expected_project_no_warp_created_files == detected_files)


expected_tiles_created_files = {
    'h12v04': None, # directory
    # TODO there should be something here but nothing is saved here during
    # manual runs.
}


def test_tiles(setup_modis_data, keep_data_repo_clean, output_tfe):
    """Test gips_tiles modis with warping."""
    # gips_tiles modis $ARGS --outdir modis_warped_tiles --notld
    args = STD_ARGS + ('--outdir', OUTPUT_DIR, '--notld')
    logger.info('starting run')
    outcome = output_tfe.run('gips_tiles', *args)
    logger.info('run complete')

    # confirm generated files match expected fingerprints
    detected_files = extract_hashes(outcome.files_created)
    assert (outcome.returncode == 0
            and not outcome.stderr
            and not outcome.files_deleted
            and expected_tiles_created_files == detected_files)


def test_tiles_copy(setup_modis_data, keep_data_repo_clean, output_tfe):
    """Test gips_tiles modis with copying."""
    # doesn't quite use STD_ARGS this time
    COPY_STD_ARGS = ('modis', '-t', 'h12v04',
                     '-d', '2012-12-01,2012-12-03', '-v', '4')
    args = COPY_STD_ARGS + ('--outdir', OUTPUT_DIR, '--notld')
    logger.info('starting run')
    outcome = output_tfe.run('gips_tiles', *args)
    logger.info('run complete')

    # confirm generated files match expected fingerprints
    detected_files = extract_hashes(outcome.files_created)
    assert (outcome.returncode == 0
            and not outcome.stderr
            and not outcome.files_deleted
            and expected_tiles_copy_created_files == detected_files)


def test_stats(setup_modis_data, keep_data_repo_clean, output_tfe):
    """Test gips_stats on projected files."""
    # generate data needed for stats computation
    args = STD_ARGS + ('--res', '100', '100',
                       '--outdir', OUTPUT_DIR, '--notld')
    outcome = output_tfe.run('gips_project', *args)
    assert outcome.returncode == 0 # confirm it worked; not really in the test

    # compute stats
    gtfe = GipsTestFileEnv(OUTPUT_DIR, start_clear=False)
    outcome = gtfe.run('gips_stats', OUTPUT_DIR)

    # check for correct stats content
    detected_files = extract_hashes(outcome.files_created)
    assert (outcome.returncode == 0
            and not outcome.stderr
            and not outcome.files_deleted
            and expected_stats_created_files == detected_files)
