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

expected_files = set([os.path.join('modis/tiles/h12v04/', f) for f in [
    '2012337/h12v04_2012337_MCD_quality.tif',
    '2012337/h12v04_2012337_MOD_temp8td.tif',
    '2012337/h12v04_2012337_MCD_snow.tif',
    '2012337/h12v04_2012337_MCD_fsnow.tif',
    '2012337/MYD11A1.A2012337.h12v04.005.2012341072847.hdf.index',
    '2012337/MCD43A2.A2012337.h12v04.005.2012356160504.hdf.index',
    '2012337/MOD09Q1.A2012337.h12v04.005.2012346141041.hdf.index',
    '2012337/h12v04_2012337_MOD_temp8tn.tif',
    '2012337/MOD11A1.A2012337.h12v04.005.2012339204007.hdf.index',
    '2012337/h12v04_2012337_MOD_clouds.tif',
    '2012337/MYD10A1.A2012337.h12v04.005.2012340112013.hdf.index',
    '2012337/MOD11A2.A2012337.h12v04.005.2012346152330.hdf.index',
    '2012337/h12v04_2012337_MOD-MYD_obstime.tif',
    '2012337/h12v04_2012337_MOD_ndvi8.tif',
    '2012337/MCD43A4.A2012337.h12v04.005.2012356160504.hdf.index',
    '2012337/MOD10A1.A2012337.h12v04.005.2012340033542.hdf.index',
    '2012337/h12v04_2012337_MOD-MYD_temp.tif',
    '2012337/h12v04_2012337_MCD_indices.tif',
    '2012336/MOD11A1.A2012336.h12v04.005.2012339180517.hdf.index',
    '2012336/MYD11A1.A2012336.h12v04.005.2012341040543.hdf.index',
    '2012336/h12v04_2012336_MCD_fsnow.tif',
    '2012336/h12v04_2012336_MOD_clouds.tif',
    '2012336/h12v04_2012336_MOD-MYD_obstime.tif',
    '2012336/MYD10A1.A2012336.h12v04.005.2012340031954.hdf.index',
    '2012336/h12v04_2012336_MOD-MYD_temp.tif',
    '2012336/h12v04_2012336_MCD_snow.tif',
    '2012336/MOD10A1.A2012336.h12v04.005.2012339213007.hdf.index',
    '2012338/MYD10A1.A2012338.h12v04.005.2012340142152.hdf.index',
    '2012338/h12v04_2012338_MOD-MYD_temp.tif',
    '2012338/MYD11A1.A2012338.h12v04.005.2012341075802.hdf.index',
    '2012338/h12v04_2012338_MCD_fsnow.tif',
    '2012338/h12v04_2012338_MCD_snow.tif',
    '2012338/MOD10A1.A2012338.h12v04.005.2012341091201.hdf.index',
    '2012338/h12v04_2012338_MOD_clouds.tif',
    '2012338/MOD11A1.A2012338.h12v04.005.2012341041222.hdf.index',
    '2012338/h12v04_2012338_MOD-MYD_obstime.tif',
]])

def test_e2e_process(setup_modis_data, test_file_environment):
    """Test gips_process on modis data."""
    logger.info('starting run')
    # TODO why is expect_error there?
    # TODO better error reporting when this process fails (break path to
    # shapefile to reproduce problem)
    # TODO how do I make gips_process output appear on the console in real time?
    outcome = test_file_environment.run('gips_process', *STD_ARGS,
                                        expect_error=True)
    logger.info('run complete')

    # confirm files created but not deleted;
    assert (expected_files == set(outcome.files_created.keys())
            and not outcome.files_deleted)
