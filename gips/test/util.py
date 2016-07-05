import logging, os, shutil
from pprint import pformat

import pytest
from scripttest import TestFileEnvironment, ProcResult, FoundFile, FoundDir

# technically imported by people who use `from .util import *`
# TODO change to _log to prevent accidental import
logger = logging.getLogger(__name__)


# set constants, mostly places to find various needed files
TEST_DATA_DIR  = str(pytest.config.rootdir.join('gips/test'))
DATA_REPO_ROOT = pytest.config.getini('data-repo')
OUTPUT_DIR     = pytest.config.getini('output-dir')
NH_SHP_PATH    = os.path.join(TEST_DATA_DIR, 'NHseacoast.shp')


slow = pytest.mark.skipif(not pytest.config.getoption("slow"),
                          reason="--slow is required for this test")


def extract_hashes(files):
    """Return a dict of file names and unique hashes of their content.

    `files` should be a dict in a result object from TestFileEnvironment.run().
    Directories' don't have hashes so use None instead."""
    return {k: getattr(v, 'hash', None) for k, v in files.items()}


class GipsTestFileEnv(TestFileEnvironment):
    """As superclass but customized for GIPS use case.

    Saves ProcResult objects in self.proc_result."""
    proc_result = None

    @staticmethod
    def log_findings(description, files):
        """If user asks for debug output, log post-run file findings.

        Logs in a format suitable for updating known good values when tests
        need to be updated to match code changes."""
        files_and_hashes = extract_hashes(files)
        logger.debug("{}: {}".format(description, pformat(files_and_hashes)))

    def run(self, *args, **kwargs):
        """As super().run but store result & prevent premature exits."""
        # TODO can remove expect_* & all those assumptions
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
        """Remove files & directories created by test run."""
        if self.proc_result is None:
            raise RuntimeError("No previous run to clean up from.")
        created = self.proc_result.files_created
        # first remove all the files
        fn = [n for (n, t) in created.items() if isinstance(t, FoundFile)]
        [os.remove(os.path.join(DATA_REPO_ROOT, n)) for n in fn]
        # then remove all the directories (which should now be empty)
        dn = [n for (n, t) in created.items() if isinstance(t, FoundDir)]
        for n in dn:
            # dirs are complex because they can exist inside eachother
            full_n = os.path.join(DATA_REPO_ROOT, n)
            if os.path.lexists(full_n):
                shutil.rmtree(full_n)


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


@pytest.yield_fixture
def keep_data_repo_clean(test_file_environment):
    """Keep data repo clean without having to run anything in it.

    This emulates tfe.run()'s checking the directory before and after a run,
    then working out how the directory has changed.  Unfortunately half the
    work is done in tfe, the other half in ProcResult."""
    tfe = test_file_environment
    before = tfe._find_files()
    yield # directory mutation happens here
    after = tfe._find_files()
    tfe.proc_result = ProcResult(tfe, ['N/A'], '', '', '', 0, before, after)


@pytest.fixture
def output_tfe():
    """Provide means to test files created by run & clean them up after."""
    gtfe = GipsTestFileEnv(OUTPUT_DIR)
    return gtfe
