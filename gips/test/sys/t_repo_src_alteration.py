import logging

import pytest

from .util import *

logger = logging.getLogger(__name__)


@pytest.yield_fixture
def careful_repo_env(request, expected):
    """Carefully provides access to the data repo.

    It won't let the test run if existing files in the repo would be
    overwritten by files created during the test."""
    gtfe = GipsTestFileEnv(DATA_REPO_ROOT, start_clear=False)
    intersection = set(gtfe._find_files().keys()) & set(expected.created.keys())
    if intersection:
        msg = '{} output files found before test; test cannot proceed'
        raise RuntimeError(msg.format(len(intersection)), list(intersection))
    yield gtfe
    gtfe.remove_created()


src_altering = pytest.mark.skipif(not pytest.config.getoption("src_altering"),
                                  reason="--src-altering is required for this test")

@src_altering
def t_modis_inv_fetch(careful_repo_env, expected):
    """Test gips_inventory --fetch; actually contacts data provider."""
    # only get data for one day to save time
    args = ('modis', '-s', NH_SHP_PATH,
            '-d', '2012-12-01,2012-12-01', '-v', '4', '--fetch')
    actual = careful_repo_env.run('gips_inventory', *args)
    assert expected == actual


@src_altering
def t_landsat_inv_fetch(careful_repo_env, expected):
    """Test gips_inventory --fetch; actually contacts data provider."""
    args = ('landsat', '-s', NH_SHP_PATH, '-d', '2015-352', '-v', '4', '--fetch')
    actual = careful_repo_env.run('gips_inventory', *args)
    # can't compare checksums because landsat's checksums are different every time.
    assert (expected.created.keys() == actual.created.keys() and
            expected.updated == actual.updated)
