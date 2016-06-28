import logging, os
from pprint import pformat

import pytest
import envoy
from scripttest import TestFileEnvironment

logger = logging.getLogger(__name__)

# set constants, mostly places to find various needed files
TEST_DATA_DIR  = str(pytest.config.rootdir.join('gips/test'))
DATA_REPO_ROOT = pytest.config.getini('data-repo')
NH_SHP_PATH    = os.path.join(TEST_DATA_DIR, 'NHseacoast.shp')
# changing this will require changes in expected_files below:
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

    @staticmethod
    def log_findings(description, files):
        """If user asks for debug output, log post-run file findings.

        Logs in a format suitable for updating known good values when tests
        need to be updated to match code changes."""
        files_and_hashes = {k: getattr(v, 'hash', None)
                            for k, v in files.items()}
        logger.debug("{}: {}".format(description, pformat(files_and_hashes)))

    def run(self, *args, **kwargs):
        """As super().run but store result & prevent premature exits."""
        pr = super(GipsTestFileEnv, self).run(
                *args, expect_error=True, expect_stderr=True, **kwargs)
        self.proc_result = pr
        logging.debug("standard output: {}".format(pr.stdout))
        logging.debug("standard error: {}".format(pr.stderr))
        self.log_findings("Created files", pr.files_created)
        self.log_findings("Updated files", pr.files_updated)
        self.log_findings("Deleted files", pr.files_deleted)
        return pr

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
    # This step isn't effective if DATA_REPO_ROOT isn't right; in that case it
    # ruins further test runs because files already exist when the test starts.
    # Maybe add self-healing by having setup_modis_data run in a TFE and
    # detecting which files are present when it starts.
    gtfe.remove_created()


# list of recorded output file names and their checksums; each should be
# created by the test
expected_process_created_files = {
    # TODO Are these broken or what?  Each None is a broken symlink:
    'modis/tiles/h12v04/2012337/h12v04_2012337_MCD_quality.tif': None,
    'modis/tiles/h12v04/2012337/h12v04_2012337_MOD_temp8td.tif': None,
    'modis/tiles/h12v04/2012337/h12v04_2012337_MOD_temp8tn.tif': None,
    'modis/tiles/h12v04/2012336/MOD10A1.A2012336.h12v04.005.2012339213007.hdf.index': -1075525670,
    'modis/tiles/h12v04/2012336/MOD11A1.A2012336.h12v04.005.2012339180517.hdf.index': -1602319177,
    'modis/tiles/h12v04/2012336/MYD10A1.A2012336.h12v04.005.2012340031954.hdf.index': 1623945316,
    'modis/tiles/h12v04/2012336/MYD11A1.A2012336.h12v04.005.2012341040543.hdf.index': -1720582124,
    'modis/tiles/h12v04/2012336/h12v04_2012336_MCD_fsnow.tif': -843500181,
    'modis/tiles/h12v04/2012336/h12v04_2012336_MCD_snow.tif': 388495321,
    'modis/tiles/h12v04/2012336/h12v04_2012336_MOD-MYD_obstime.tif': 1994827924,
    'modis/tiles/h12v04/2012336/h12v04_2012336_MOD-MYD_temp.tif': 2094570047,
    'modis/tiles/h12v04/2012336/h12v04_2012336_MOD_clouds.tif': 161070470,
    'modis/tiles/h12v04/2012337/MCD43A2.A2012337.h12v04.005.2012356160504.hdf.index': 1869798455,
    'modis/tiles/h12v04/2012337/MCD43A4.A2012337.h12v04.005.2012356160504.hdf.index': 1702701995,
    'modis/tiles/h12v04/2012337/MOD09Q1.A2012337.h12v04.005.2012346141041.hdf.index': 1528708875,
    'modis/tiles/h12v04/2012337/MOD10A1.A2012337.h12v04.005.2012340033542.hdf.index': 1739917027,
    'modis/tiles/h12v04/2012337/MOD11A1.A2012337.h12v04.005.2012339204007.hdf.index': 640817914,
    'modis/tiles/h12v04/2012337/MOD11A2.A2012337.h12v04.005.2012346152330.hdf.index': 53371709,
    'modis/tiles/h12v04/2012337/MYD10A1.A2012337.h12v04.005.2012340112013.hdf.index': 531935583,
    'modis/tiles/h12v04/2012337/MYD11A1.A2012337.h12v04.005.2012341072847.hdf.index': 1676310978,
    'modis/tiles/h12v04/2012337/h12v04_2012337_MCD_fsnow.tif': 297883486,
    'modis/tiles/h12v04/2012337/h12v04_2012337_MCD_indices.tif': -2140726827,
    'modis/tiles/h12v04/2012337/h12v04_2012337_MCD_snow.tif': -748640537,
    'modis/tiles/h12v04/2012337/h12v04_2012337_MOD-MYD_obstime.tif': -1729084231,
    'modis/tiles/h12v04/2012337/h12v04_2012337_MOD-MYD_temp.tif': -1718009535,
    'modis/tiles/h12v04/2012337/h12v04_2012337_MOD_clouds.tif': -832284681,
    'modis/tiles/h12v04/2012337/h12v04_2012337_MOD_ndvi8.tif': -593200294,
    'modis/tiles/h12v04/2012338/MOD10A1.A2012338.h12v04.005.2012341091201.hdf.index': 1725484908,
    'modis/tiles/h12v04/2012338/MOD11A1.A2012338.h12v04.005.2012341041222.hdf.index': 838676814,
    'modis/tiles/h12v04/2012338/MYD10A1.A2012338.h12v04.005.2012340142152.hdf.index': -130649785,
    'modis/tiles/h12v04/2012338/MYD11A1.A2012338.h12v04.005.2012341075802.hdf.index': -642783734,
    'modis/tiles/h12v04/2012338/h12v04_2012338_MCD_fsnow.tif': -1930181337,
    'modis/tiles/h12v04/2012338/h12v04_2012338_MCD_snow.tif': 387672365,
    'modis/tiles/h12v04/2012338/h12v04_2012338_MOD-MYD_obstime.tif': -1693632983,
    'modis/tiles/h12v04/2012338/h12v04_2012338_MOD-MYD_temp.tif': 1712906003,
    'modis/tiles/h12v04/2012338/h12v04_2012338_MOD_clouds.tif': 296967275
}


def test_e2e_process(setup_modis_data, test_file_environment):
    """Test gips_process on modis data."""
    logger.info('starting run')
    outcome = test_file_environment.run('gips_process', *STD_ARGS)
    logger.info('run complete')

    # extract the checksum from each found file
    detected_files = {k: v.hash for k, v in outcome.files_created.items()}
    # repo should now have specific new files with the right content
    # TODO refactor this into four separate tests that DO NOT repeat the
    # gips_process command; need this because 'and' is lazy so not all branches
    # are being evaluated (and thus reported-on).
    assert (outcome.returncode == 0
            and not outcome.stderr
            and not outcome.files_deleted
            and expected_process_created_files == detected_files)


# trailing whitespace and other junk characters are in current output
expected_info_stdout = """\x1b[1mGIPS Data Repositories (v0.8.2)\x1b[0m
\x1b[1m
Modis Products v1.0.0\x1b[0m
\x1b[1m
Terra 8-day Products
\x1b[0m   ndvi8       Normalized Difference Vegetation Index: 250m
   temp8td     Surface temperature: 1km                
   temp8tn     Surface temperature: 1km                
\x1b[1m
Nadir BRDF-Adjusted 16-day Products
\x1b[0m   indices     Land indices                            
   quality     MCD Product Quality                     
\x1b[1m
Terra/Aqua Daily Products
\x1b[0m   fsnow       Fractional snow cover data              
   obstime     MODIS Terra/Aqua overpass time          
   snow        Snow and ice cover data                 
   temp        Surface temperature data                
\x1b[1m
Standard Products
\x1b[0m   clouds      Cloud Mask                              
   landcover   MCD Annual Land Cover                   
"""

def test_e2e_info(test_file_environment):
    """Test `gips_info modis` and confirm recorded output is given."""
    outcome = test_file_environment.run('gips_info', 'modis')
    assert (outcome.returncode == 0
            and not outcome.stderr
            and not outcome.files_created
            and not outcome.files_updated
            and not outcome.files_deleted
            and outcome.stdout == expected_info_stdout)
