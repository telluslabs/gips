from __future__ import print_function

import logging
from datetime import datetime

import pytest
import envoy

import util
from .util import *

logger = logging.getLogger(__name__)

pytestmark = sys # skip everything unless --sys

driver = 'modis'

# changing this will require changes in expected/
STD_ARGS = ('modis', '-s', NH_SHP_PATH, '-d', '2012-12-01,2012-12-03', '-v', '4')

@pytest.fixture
def setup_modis_data(pytestconfig):
    """Use gips_inventory to ensure presence of MODIS data in the data repo."""
    if not pytestconfig.getoption('setup_repo'):
        logger.debug("Skipping repo setup per lack of option.")
        return
    if datetime.today().date().weekday() == 2: # <-- is it Wednesday?
        raise Exception("It seems to be Wednesday; modis downloads are likely to fail.")
    logger.info("Downloading MODIS data . . .")
    cmd_str = 'gips_inventory ' + ' '.join(STD_ARGS) + ' --fetch'
    outcome = envoy.run(cmd_str)
    logger.info("MODIS data download complete.")
    if outcome.status_code != 0:
        #msg = ("MODIS data setup via `gips_inventory` technically failed, but this may be due to false"
        #       " positives in the driver; proceeding with tests")
        #logger.warning(msg)
        #logger.warning('=== standard out:  ' + outcome.std_out)
        #logger.warning('=== standard error:  ' + outcome.std_err)
        raise RuntimeError("MODIS data setup via `gips_inventory` failed",
                           outcome.std_out, outcome.std_err, outcome)


def t_inventory(setup_modis_data, repo_env, expected):
    """Test `gips_inventory modis` and confirm recorded output is given."""
    actual = repo_env.run('gips_inventory', *STD_ARGS)
    assert expected == actual

from .expected import modis as expectations

@pytest.mark.parametrize("product", expectations.t_process.keys())
def t_process(setup_modis_data, product):
    """Test gips_process on modis data."""
    dut = util.DATA_REPO_ROOT # directory under test
    record_path = pytest.config.getoption('--record')
    recording_mode = record_path is not None

    if recording_mode:
        initial_files = util.find_files(dut)
    else:
        expectation = expectations.t_process[product]
        expected_filenames = [e[0] for e in expectation]
        interlopers = [fn for fn in expected_filenames if os.path.exists(fn)]
        if interlopers:
            raise IOError('Files in the way of the test: {}'.format(interlopers))

    # run
    import sh
    args = ('modis', '-s', NH_SHP_PATH, '-d', '2012-12-01,2012-12-03',
            '-v', '4', '-p', product)
    print("command line: `gips_process {}`".format(' '.join(args)))
    outcome = sh.gips_process(*args)

    if recording_mode:
        final_files = find_files(dut)
        created_files = set(final_files) - set(initial_files)

        # when recording the path, do '<record_dir>/foo/bar/baz/file.tif'
        relpath_start = os.path.dirname(dut)
        rel_cf = [os.path.relpath(fp, relpath_start) for fp in created_files]

        cf_expectations = [util.generate_expectation(fn, dut) for fn in rel_cf]
        print("Recording {} outcome to {}.".format(product, record_path))
        import pprint
        with open(record_path, 'a') as rfo:
            print('\n# {}[{}] recording:'.format(t_process.__name__, product),
                    file=rfo)
            print("'{}':".format(product), file=rfo)
            pretty_hashes = pprint.pformat(cf_expectations)
            print('    ', end='', file=rfo)
            print('\n    '.join(pretty_hashes.split('\n')), end='', file=rfo)
            print(',', file=rfo)
    else:
        # actual test: assemble data to compare to expectation
        files = [util.generate_expectation(fn, dut)
                    for fn in expected_filenames]
        assert outcome.exit_code == 0 and expectation == files


def t_info(repo_env, expected):
    """Test `gips_info modis` and confirm recorded output is given."""
    actual = repo_env.run('gips_info', 'modis')
    assert expected == actual


def t_project(setup_modis_data, clean_repo_env, output_tfe, expected):
    """Test gips_project modis with warping."""
    args = STD_ARGS + ('--res', '100', '100', '--outdir', OUTPUT_DIR, '--notld')
    actual = output_tfe.run('gips_project', *args)
    assert expected == actual


def t_project_two_runs(setup_modis_data, clean_repo_env, output_tfe, expected):
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


def t_project_no_warp(setup_modis_data, clean_repo_env, output_tfe, expected):
    """Test gips_project modis without warping."""
    args = STD_ARGS + ('--outdir', OUTPUT_DIR, '--notld')
    actual = output_tfe.run('gips_project', *args)
    assert expected == actual


def t_tiles(setup_modis_data, clean_repo_env, output_tfe, expected):
    """Test gips_tiles modis with warping."""
    args = STD_ARGS + ('--outdir', OUTPUT_DIR, '--notld')
    actual = output_tfe.run('gips_tiles', *args)
    assert expected == actual


def t_tiles_copy(setup_modis_data, clean_repo_env, output_tfe, expected):
    """Test gips_tiles modis with copying."""
    # doesn't quite use STD_ARGS
    args = ('modis', '-t', 'h12v04', '-d', '2012-12-01,2012-12-03', '-v', '4',
            '--outdir', OUTPUT_DIR, '--notld')
    actual = output_tfe.run('gips_tiles', *args)
    assert expected == actual


def t_stats(setup_modis_data, clean_repo_env, output_tfe, expected):
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
    
    
def t_gridded_export(setup_modis_data, clean_repo_env, output_tfe, expected):
    """Test gips_project using rastermask spatial spec"""
    rastermask = os.path.join(TEST_DATA_DIR, 'site_mask.tif')
    args = ('modis', '-p', 'indices', '-r', rastermask, '--fetch',
            '-d', '2005-01-01',
            '--outdir', OUTPUT_DIR, '--notld')

    actual = output_tfe.run('gips_project', *args)
    assert expected == actual

    
def t_cubic_gridded_export(setup_modis_data, clean_repo_env, output_tfe, expected):
    """Test gips_project using rastermask spatial spec"""
    rastermask = os.path.join(TEST_DATA_DIR, 'site_mask.tif')
    args = ('modis', '-p', 'indices', '-r', rastermask, '--fetch',
            '-d', '2005-01-01', '--interpolation', "2",
            '--outdir', OUTPUT_DIR, '--notld')

    actual = output_tfe.run('gips_project', *args)
    assert expected == actual

