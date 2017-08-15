import logging

import pytest
import envoy

from .util import *

import os

logger = logging.getLogger(__name__)

pytestmark = sys  # skip everything unless --sys

# changing this will require changes in expected/
driver = 'sar'
STD_TILE = 'N07E099'
STD_DATES = '2015-04-11'
STD_ARGS = (driver, '-t', STD_TILE, '-d', STD_DATES, '-v', '4')
ASSET_URL_PREFIX = (
    'ftp://anonymous:{USER}@volga.ags.io/files/{DRIVER}/'
    .format(
        USER=os.environ.get('USER', 'nobody'),
        DRIVER=driver
    )
)
STORED_ASSETS = [
    ASSET_URL_PREFIX + f
    for f in
    [
        'KC_999-C019DRN07E099WBDORSA1.tar.gz',
        'KC_017-C25N00E099WB1ORSA1.tar.gz',
        'KC_017-Y10N19E100FBDORSA1.tar.gz',
    ]
]


@pytest.fixture
def setup_sar_data(pytestconfig):
    """
    Use STORED_ASSETS+gips_archive or gips_inventory to ensure presence
    of asset data in the data repo.
    """
    if not pytestconfig.getoption('setup_repo'):
        logger.debug("Skipping repo setup per lack of option.")
        return
    if 'STORED_ASSETS' in globals():
        cwd = os.getcwd()
        stage = os.path.join(DATA_REPO_ROOT, driver, 'stage')
        os.chdir(stage)
        for asset in STORED_ASSETS:
            cmd_str = 'wget {URL}'.format(URL=asset)
            logger.info("Downloading SAR assets with " + cmd_str)
            outcome = envoy.run(cmd_str)
            if outcome.status_code != 0:
                raise RuntimeError(
                    "fetchinv via STORED_ASSETS failed",
                    outcome.std_out, outcome.std_err, outcome
                )
        cmd_str = ('gips_archive {DRIVER}'.format(DRIVER=driver))
        logger.info("Archiving SAR assets with " + cmd_str)
        outcome = envoy.run(cmd_str)
        logger.info("SAR data archival complete.")
        if outcome.status_code != 0:
            raise RuntimeError(
                "sar data setup via `gips_archive` failed",
                outcome.std_out, outcome.std_err, outcome
            )
    else:
        cmd_str = 'gips_inventory ' + ' '.join(STD_ARGS) + ' --fetch'
        logger.info("Downloading SAR assets with " + cmd_str)
        outcome = envoy.run(cmd_str)
        logger.info("SAR data download complete.")
        if outcome.status_code != 0:
            raise RuntimeError(
                "sar data setup via `gips_inventory` failed",
                outcome.std_out, outcome.std_err, outcome
            )


setup_fixture = setup_sar_data

# ###   SHOULD BE STANDARD BELOW HERE #####


def t_inventory(setup_fixture, repo_env, expected):
    """
    Test `gips_inventory` for {} and confirm recorded output is given.
    """.format(driver)
    actual = repo_env.run('gips_inventory', *STD_ARGS)
    assert expected == actual


def t_process(setup_fixture, repo_env, expected):
    """Test gips_process on {} data.""".format(driver)
    process_actual = repo_env.run('gips_process', *STD_ARGS)
    inventory_actual = envoy.run('gips_inventory ' + ' '.join(STD_ARGS))
    assert expected == process_actual
    assert inventory_actual.std_out == expected._inv_stdout


def t_info(repo_env, expected):
    """Test `gips_info {driver}` and confirm recorded output is given."""
    actual = repo_env.run('gips_info', driver)
    assert expected == actual


def t_project(setup_fixture, clean_repo_env, output_tfe, expected):
    """Test gips_project {} with warping.""".format(driver)
    args = STD_ARGS + ('--res', '100', '100', '--outdir', OUTPUT_DIR, '--notld')
    actual = output_tfe.run('gips_project', *args)
    assert expected == actual


def t_project_no_warp(setup_fixture, clean_repo_env, output_tfe, expected):
    """Test gips_project {} without warping.""".format(driver)
    args = STD_ARGS + ('--outdir', OUTPUT_DIR, '--notld')
    actual = output_tfe.run('gips_project', *args)
    assert expected == actual


# Haven't used gips_tiles ever
def t_tiles(setup_fixture, clean_repo_env, output_tfe, expected):
    """Test gips_tiles {} with warping.""".format(driver)
    args = STD_ARGS + ('--outdir', OUTPUT_DIR, '--notld')
    actual = output_tfe.run('gips_tiles', *args)
    assert expected == actual


def t_tiles_copy(setup_fixture, clean_repo_env, output_tfe, expected):
    """Test gips_tiles {} with copying.""".format(driver)
    # doesn't quite use STD_ARGS
    args = (driver, '-t', STD_TILE, '-d', STD_DATES, '-v', '4',
            '--outdir', OUTPUT_DIR, '--notld')
    actual = output_tfe.run('gips_tiles', *args)
    assert expected == actual


def t_stats(setup_fixture, clean_repo_env, output_tfe, expected):
    """Test gips_stats on projected files."""
    # generate data needed for stats computation
    args = STD_ARGS + ('--res', '100', '100', '--outdir', OUTPUT_DIR, '--notld')
    prep_run = output_tfe.run('gips_project', *args)
    assert prep_run.exit_status == 0  # confirm it worked; not really in the test

    # compute stats
    gtfe = GipsTestFileEnv(OUTPUT_DIR, start_clear=False)
    actual = gtfe.run('gips_stats', OUTPUT_DIR)

    # check for correct stats content
    assert expected == actual
