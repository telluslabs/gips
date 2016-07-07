import logging, os, shutil
from pprint import pformat

import pytest
from scripttest import TestFileEnvironment, ProcResult, FoundFile, FoundDir

from . import data


# technically imported by people who use `from .util import *`
# TODO change to _log to prevent accidental import
logger = logging.getLogger(__name__)


def set_constants(config):
    # set constants, mostly places to find various needed files
    global TEST_DATA_DIR, DATA_REPO_ROOT, OUTPUT_DIR, NH_SHP_PATH, slow
    TEST_DATA_DIR  = str(config.rootdir.join('gips/test'))
    DATA_REPO_ROOT = config.getini('data-repo')
    OUTPUT_DIR     = config.getini('output-dir')
    NH_SHP_PATH    = os.path.join(TEST_DATA_DIR, 'NHseacoast.shp')
    slow = pytest.mark.skipif(not config.getoption("slow"),
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
        # TODO no need to extract things that are extracted already elsewhere
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
        return GipsProcResult(pr)

    def remove_created(self, strict=False):
        """Remove files & directories created by test run."""
        if self.proc_result is None:
            msg = "No previous run to clean up from."
            if strict:
                raise RuntimeError(msg)
            else:
                logger.warning("Can't remove_created: " + msg)
                return

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


class GipsProcResult(object):
    attribs = ('exit_status', 'stdout', 'stderr', 'updated', 'deleted', 'created')
    def __init__(self, proc_result=None, compare_stdout=None, **kwargs):
        """stdout is usually produced but it's not often tested, so ignore it for comparisons
        unless the user explicitly asks for it, and let compare_stdout override that if needed.
        """
        if proc_result is None:
            self.exit_status = 0
            self.stdout = None
            self.stderr = u''
            self.updated = {}
            self.deleted = {}
            self.created = {}
        else:
            # self.proc_result = proc_result # not sure if this is needed
            self.exit_status = proc_result.returncode
            self.stdout = proc_result.stdout
            self.stderr = proc_result.stderr
            self.updated = extract_hashes(proc_result.files_updated)
            self.deleted = extract_hashes(proc_result.files_deleted)
            self.created = extract_hashes(proc_result.files_created)

        input_fields = set(kwargs.keys())
        if not input_fields.issubset(set(self.attribs)):
            raise ValueError('Unknown attributes for GipsProcResult',
                             list(input_fields - set(self.attribs)))

        self.__dict__.update(kwargs) # set user's desired values

        # guess the user's wishes regarding stdout comparison;
        # explicit request should override guesswork
        if compare_stdout is not None:
            self.compare_stdout = compare_stdout
        else:
            self.compare_stdout = self.stdout is not None
        # need a valid value to compare against either way
        self.stdout = self.stdout or u''

    def __eq__(self, other):
        matches = (
            self.exit_status == other.exit_status,
            not self.compare_stdout or self.stdout == other.stdout,
            self.stderr == other.stderr,
            self.updated == other.updated,
            self.deleted == other.deleted,
            self.created == other.created,
        )
        return all(matches)

    def __repr__(self):
        return "GipsProcResult(object) repr called!"


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


@pytest.yield_fixture(scope='module')
def keep_data_repo_clean(request):
    """Keep data repo clean without having to run anything in it.

    This emulates tfe.run()'s checking the directory before and after a run,
    then working out how the directory has changed.  Unfortunately half the
    work is done in tfe, the other half in ProcResult."""
    file_env = GipsTestFileEnv(DATA_REPO_ROOT, start_clear=False)
    before = file_env._find_files()
    logger.debug("Generating file env: {}".format(file_env))
    yield file_env
    after = file_env._find_files()
    file_env.proc_result = ProcResult(file_env, ['N/A'], '', '', '', 0, before, after)
    file_env.remove_created()
    logger.debug("Finalized file env: {}".format(file_env))


@pytest.fixture
def output_tfe():
    """Provide means to test files created by run & clean them up after."""
    gtfe = GipsTestFileEnv(OUTPUT_DIR)
    return gtfe


@pytest.fixture
def expected(request):
    return GipsProcResult(**data.expectations[request.function.func_name])
