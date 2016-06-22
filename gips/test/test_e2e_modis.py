import logging, os

import pytest
import envoy
from scripttest import TestFileEnvironment

logger = logging

# set constants, mostly places to find various needed files
TEST_DATA_DIR  = str(pytest.config.rootdir.join('gips/test'))
# TODO if data-repo is wrong, silent error(!!)
DATA_REPO_ROOT = str(pytest.config.getini('data-repo'))
NH_SHP_PATH    = os.path.join(TEST_DATA_DIR, 'NHseacoast.shp')
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


class GipsTestFileEnv(TestFileEnvironment):
    """As superclass but customized for GIPS use case.

    Saves ProcResult objects in self.proc_result."""
    proc_result = None

    def run(self, *args, **kwargs):
        self.proc_result = super(GipsTestFileEnv, self).run(*args, **kwargs)
        return self.proc_result

    def remove_created(self):
        """Remove files created by test run."""
        if self.proc_result is None:
            raise RuntimeError("No previous run to clean up from.")
        for fname in self.proc_result.files_created.keys():
            os.remove(os.path.join(DATA_REPO_ROOT, fname))


@pytest.yield_fixture
def test_file_environment():
    """Provide means to test files created by run & clean them up after."""
    gtfe = GipsTestFileEnv(DATA_REPO_ROOT, start_clear=False)
    yield gtfe
    # TODO when does this step get skipped?  During some errors it seems?
    gtfe.remove_created()

def test_e2e_process(setup_modis_data, test_file_environment):
    """Test gips_process on modis data."""
    logger.info('starting run')
    # TODO why is expect_error there?
    # TODO better error reporting when this process fails (break path to
    # shapefile to reproduce problem)
    outcome = test_file_environment.run('gips_process', *STD_ARGS,
                                        expect_error=True)
    logger.info('run complete')

    # confirm files created but not deleted;
    # files_updated includes dirs whose contents have changed
    assert (bool(outcome.files_created)
            and bool(outcome.files_updated)
            and not bool(outcome.files_deleted))
