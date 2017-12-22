from __future__ import print_function

import logging, os, shutil, re
import importlib
import hashlib
import pprint

import pytest
import scripttest
import envoy # deprecated
import sh

from gips.inventory import orm # believed to be safe even though it's the code under test

_log = logging.getLogger(__name__)


def set_constants(config):
    """Use pytest config API to set globals pointing at needed file paths."""
    global TEST_DATA_DIR, DATA_REPO_ROOT, OUTPUT_DIR, NH_SHP_PATH, DURHAM_SHP_PATH, NE_SHP_PATH
    TEST_DATA_DIR  = str(config.rootdir.join('gips/test'))
    DATA_REPO_ROOT = config.getini('data-repo')
    OUTPUT_DIR     = config.getini('output-dir')
    NH_SHP_PATH    = os.path.join(TEST_DATA_DIR, 'NHseacoast.shp')
    NE_SHP_PATH    = os.path.join(TEST_DATA_DIR, 'NE.shp')
    DURHAM_SHP_PATH = os.path.join(TEST_DATA_DIR, 'durham.shp')

slow = pytest.mark.skipif('not config.getoption("slow")',
                          reason="--slow is required for this test")
acolite = pytest.mark.skipif('not config.getoption("acolite")',
                          reason="--acolite is required for this test")
sys = pytest.mark.skipif('not config.getoption("sys")', reason="--sys is required for this test")


def extract_hashes(files):
    """Return a dict of file names and unique hashes of their content.

    `files` should be a dict in a result object from TestFileEnvironment.run().
    Directories' don't have hashes so use None instead."""
    return {k: getattr(v, 'hash', None) for k, v in files.items()}


def extract_timestamps(files):
    """Return a dict of file names and unique hashes of their content.

    `files` should be a dict in a result object from TestFileEnvironment.run().
    Directories' don't have hashes so use None instead."""
    return {k: getattr(v, 'hash', None) for k, v in files.items()}


class GipsTestFileEnv(scripttest.TestFileEnvironment):
    """As superclass but customized for GIPS use case.

    Captured values from the process under test:
        standard output
        standard error
        Created files & checksums (for a configured directory-under-test)
        Updated files & checksums (for a configured directory-under-test)
        Deleted files & checksums(?) (for a configured directory-under-test)
        exit status
    Saves ProcResult objects in self.proc_result."""
    proc_result = None

    @staticmethod
    def log_findings(description, files):
        """If user asks for debug output, log post-run file findings.

        Logs in a format suitable for updating known good values when tests
        need to be updated to match code changes."""
        _log.debug("{}: {}".format(description, pprint.pformat(files)))

    def run(self, *args, **kwargs):
        """As super().run but store result & prevent premature exits."""
        logging.debug("command line: `{}`".format(' '.join(args)))
        self.proc_result = super(GipsTestFileEnv, self).run(
            *args, expect_error=True, expect_stderr=True, **kwargs)
        self.gips_proc_result = gpr = GipsProcResult(self.proc_result)
        logging.debug("standard output: {}".format(
            gpr.stdout if gpr.stdout != '' else '(None)'))
        logging.debug("standard error: {}".format(
            gpr.stderr if gpr.stderr != '' else '(None)'))
        if pytest.config.getoption("--expectation-format"):
            print ('standard output (expectation format): """' +
                   re.sub('\\\\n', '\n', repr(gpr.stdout))[2:-1] + '"""')
            print ('standard error (expectation format):  """' +
                   re.sub('\\\\n', '\n', repr(gpr.stderr))[2:-1] + '"""')
        self.log_findings("Created files", gpr.created)
        self.log_findings("Updated files", gpr.updated)
        self.log_findings("Deleted files", gpr.deleted)
        return gpr

    def remove_created(self, strict=False):
        """Remove files & directories created by test run."""
        if self.proc_result is None:
            msg = "No previous run to clean up from."
            if strict:
                raise RuntimeError(msg)
            else:
                _log.warning("Can't remove_created: " + msg)
                return

        created = self.proc_result.files_created
        # first remove all the files
        fn = [n for (n, t) in created.items() if isinstance(t, scripttest.FoundFile)]
        [os.remove(os.path.join(DATA_REPO_ROOT, n)) for n in fn]
        # then remove all the directories (which should now be empty)
        dn = [n for (n, t) in created.items() if isinstance(t, scripttest.FoundDir)]
        for n in dn:
            # dirs are complex because they can exist inside eachother
            full_n = os.path.join(DATA_REPO_ROOT, n)
            if os.path.lexists(full_n):
                shutil.rmtree(full_n)

    def _find_files(self, *args, **kwargs):
        """As super, but log that the checksums are being computed.

        Logs are needed because the process takes time for large assets."""
        _log.debug("Starting file detection & checksumming")
        rv = super(GipsTestFileEnv, self)._find_files(*args, **kwargs)
        _log.debug("Completed file detection & checksumming")
        return rv


class GipsProcResult(object):
    """Storage & equality comparison for a process's various outcomes.

    Standard output is handled specially for equality comparison; see __eq__.
    Can accept scripttest.ProcResult objects at initialization; see __init__.
    """
    attribs = ('exit_status', 'stdout', 'stderr', 'updated', 'deleted',
               'created', 'ignored',)  # 'timestamps')

    def __init__(self, proc_result=None, compare_stdout=None, compare_stderr=True, **kwargs):
        """Initialize the object using a ProcResult, explicit kwargs, or both.

        ProcResults' reports on files (created, deleted, updated) are saved as
        their names and hashes.  compare_stdout is an explicit way to request
        stdout be considered in __eq__; see below.  If it is not set, then
        self.stdout is examined.  If set by the user, it is assumed stdout
        comparison is desired.  compare_stderr is less magical:  Do the
        comparison unless the user specifies otherwise.
        """
        if proc_result is None:
            self.exit_status = 0
            self.stdout = None
            self.stderr = u''
            self.updated = {}
            self.deleted = {}
            self.created = {}
            # self.timestamps = {}
        else:
            # self.proc_result = proc_result # not sure if this is needed
            self.exit_status = proc_result.returncode
            self.stdout = proc_result.stdout
            self.stderr = proc_result.stderr
            self.updated = extract_hashes(proc_result.files_updated)
            self.deleted = extract_hashes(proc_result.files_deleted)
            self.created = extract_hashes(proc_result.files_created)
            # self.timestamps = dict()
            # for files in [proc_result.files_updated, proc_result.files_created]:
            #     self.timestamps.update(extract_timestamps(files))

        self.ignored = []  # list of filenames to ignore for comparison purposes

        # special keys are permitted if they begin with an underscore
        input_fields = set(k for k in kwargs.keys() if k[0] != '_')
        if not input_fields.issubset(set(self.attribs)):
            raise ValueError('Unknown attributes for GipsProcResult',
                             list(input_fields - set(self.attribs)))

        self.__dict__.update(kwargs)  # set user's desired values

        # guess the user's wishes regarding stdout comparison;
        # explicit request should override guesswork
        if compare_stdout is not None:
            self.compare_stdout = compare_stdout
        else:
            self.compare_stdout = self.stdout is not None
        # need a valid value to compare against either way
        # self.stdout = self.stdout or u''
        self.compare_stderr = compare_stderr

    def strip_ignored(self, d):
        """Return a copy of dict d but strip out items in self.ignored.

        If self.ignored = ['a', 'b'] then
        strip_ignored({'a': 1, 'b': 2, 'c': 2}) returns {'c': 2}.
        """
        return {k: v for k, v in d.items() if k not in self.ignored}

    def __eq__(self, other):
        """Equality means all attributes must match, except possibly stdout & stderr.

        Note that the type of other is not considered.
        """
        # only compare standard streams if both parties agree
        compare_stdout = self.compare_stdout and other.compare_stdout
        compare_stderr = self.compare_stderr and other.compare_stderr
        matches = (
            self.exit_status == other.exit_status,
            not compare_stdout or self.stdout == other.stdout,
            not compare_stderr or self.stderr == other.stderr,
            self.strip_ignored(self.updated) == self.strip_ignored(other.updated),
            self.strip_ignored(self.deleted) == self.strip_ignored(other.deleted),
            self.strip_ignored(self.created) == self.strip_ignored(other.created),
        )
        return all(matches)


def rectify(driver):
    """Ensure inv DB matches files on disk."""
    if not orm.use_orm():
        return
    rectify_cmd = 'gips_inventory {} --rectify'.format(driver)
    outcome = envoy.run(rectify_cmd)
    if outcome.status_code != 0:
        raise RuntimeError("failed: " + rectify_cmd,
                           outcome.std_out, outcome.std_err, outcome)

def find_files(path):
    """Finds all non-directory files under the given path.

    A lot like running find(1) with no arguments.  Doesn't follow symlinks.
    Doesn't report errors (see os.walk docs for details).
    """
    return [os.path.join(subpath, f)
            for subpath, _, filenames in os.walk(path) for f in filenames]

def generate_expectation(filename, base_path):
    """Return an expectation of the file's content, based on its file type.

    Expectation formats:
        Symlink:  (filename, 'symlink', prefix_string, suffix_string)
            With symlinks one often can't use the whole link target
            because parts differ across environments (eg /home/usr/etc).
             So just use the bits before and after the base_path.
        Hash:  (filename, 'hash', 'sha256', <hex digest string>).
            Used as a fallback if nothing else matches the file type.
        Text-full:  (filename, 'text-full', list(<lines-in-file>))
        Finally, if the file is absent:  (filename, 'absent')
    """
    # may want to try python-magic at some point:  https://github.com/ahupp/python-magic
    # but for now going by file extension seems to be sufficient.

    # have to use lexists to cover for foolish abuse of symlinks by GDAL et al
    if not os.path.lexists(filename):
        return (filename, 'absent')

    # symlinks
    if os.path.islink(filename):
        #                    vvvvvvvvvvvvvvvvvvvvvv--- have to rmeove this bit
        # HDF4_EOS:EOS_GRID:"/home/tolson/src/gips/data-root/modis/tiles/h12v04/2012337
        #   /MCD43A2.A2012337.h12v04.006.2016112013509.hdf":MOD_Grid_BRDF:Snow_BRDF_Albedo
        # when recording the path, do '<record_dir>/foo/bar/baz/file.tif'
        link_target = os.readlink(filename)
        separator = os.path.dirname(base_path)
        prefix, suffix = link_target.split(separator)
        return (filename, 'symlink', prefix, suffix)

    # text files
    size_threshold = 80 * 25 # about one terminal-screen
    if filename.endswith('.txt'):
        f_size = os.stat(filename).st_size
        if f_size <= size_threshold: # give up if there's too much text
            with open(filename) as fo:
                lines = fo.readlines()
            return (filename, 'text-full', lines)
        print('{} ({} bytes) exceeds max supported size for text diffs'
              ' ({} bytes); defaulting to checksum'.format(
                    filename, f_size, size_threshold))

    # product TIFFs
    if filename.endswith('.tif'):
        pass # TODO https://github.com/Applied-GeoSolutions/gips/issues/463

    # use a hash as a fallback
    return (filename, 'hash', 'sha256', generate_file_hash(filename))

def generate_file_hash(filename, blocksize=2**20):
    # stolen from SO: https://stackoverflow.com/questions/1131220/get-md5-hash-of-big-files-in-python
    m = hashlib.sha256()
    with open(filename, 'rb' ) as f:
        while True:
            buf = f.read(blocksize)
            if not buf:
                break
            m.update(buf)
    return m.hexdigest()

def record_path():
    path = pytest.config.getoption('--record')
    return False if path in (None, '') else path

def sys_test_wrapper(request, path):
    """Provides for system testing by watching the specified directory.

    `request` is a pytest request object probably passed in to a fixture
    that is calling this function. Yields to let some process work, then
    reports on files created in the path during the wait.
    """
    # DATA_REPO_ROOT is the directory under test
    rp = record_path()
    product = request.getfixturevalue('product')
    expectations = load_expectation_module(request.module.__name__)
    expected = getattr(expectations, request.function.__name__)[product]
    expected_filenames = [e[0] for e in expected]

    if rp:
        initial_files = find_files(path)
    else:
        interlopers = [fn for fn in expected_filenames if os.path.exists(fn)]
        if interlopers:
            raise IOError('Files in the way of the test: {}'.format(interlopers))

    def wrapped_runner(cmd_string, *args):
        print("command line: `{} {}`".format(cmd_string, ' '.join(args)))
        outcome = sh.Command(cmd_string)(*args)
        return outcome, [generate_expectation(fn, path)
                         for fn in expected_filenames]

    yield bool(rp), expected, wrapped_runner

    if rp:
        final_files = find_files(path)
        created_files = set(final_files) - set(initial_files)

        # when recording the path, do '<record_dir>/foo/bar/baz/file.tif'
        relpath_start = os.path.dirname(path)
        rel_cf = [os.path.relpath(fp, relpath_start) for fp in created_files]

        cf_expectations = [generate_expectation(fn, path) for fn in rel_cf]
        print("Recording {} outcome to {}.".format(product, rp))
        with open(rp, 'a') as rfo:
            print('\n# {}[{}] recording:'.format(request.function.__name__, product),
                  file=rfo)
            print("'{}':".format(product), file=rfo)
            pretty_hashes = pprint.pformat(cf_expectations)
            print('    ', end='', file=rfo)
            print('\n    '.join(pretty_hashes.split('\n')), end='', file=rfo)
            print(',', file=rfo)

@pytest.yield_fixture
def repo_wrapper(request):
    for rv in sys_test_wrapper(request, DATA_REPO_ROOT):
        yield rv

@pytest.yield_fixture
def export_wrapper(request):
    for rv in sys_test_wrapper(request, OUTPUT_DIR):
        yield rv

@pytest.yield_fixture
def repo_env(request):
    """Provide means to test files created by run & clean them up after."""
    if not orm.use_orm():
        _log.warning("ORM is deactivated; check GIPS_ORM.")
    gtfe = GipsTestFileEnv(DATA_REPO_ROOT, start_clear=False)
    yield gtfe
    # This step isn't effective if DATA_REPO_ROOT isn't right; in that case it
    # ruins further test runs because files already exist when the test starts.
    # Maybe add self-healing by having setup_modis_data run in a TFE and
    # detecting which files are present when it starts.
    gtfe.remove_created()
    rectify(request.module.driver)


@pytest.yield_fixture(scope='module')
def clean_repo_env(request):
    """Keep data repo clean without having to run anything in it.

    This emulates tfe.run()'s checking the directory before and after a run,
    then working out how the directory has changed.  Unfortunately half the
    work is done in tfe, the other half in ProcResult."""
    if not orm.use_orm():
        _log.warning("ORM is deactivated; check GIPS_ORM.")
    file_env = GipsTestFileEnv(DATA_REPO_ROOT, start_clear=False)
    before = file_env._find_files()
    _log.debug("Generating file env: {}".format(file_env))
    yield file_env
    after = file_env._find_files()
    file_env.proc_result = scripttest.ProcResult(file_env, ['N/A'], '', '', '', 0, before, after)
    file_env.remove_created()
    rectify(request.module.driver)
    _log.debug("Finalized file env: {}".format(file_env))


@pytest.fixture
def output_tfe():
    """Provide means to test files created by run & clean them up after."""
    gtfe = GipsTestFileEnv(OUTPUT_DIR)
    return gtfe

def load_expectation_module(name):
    """Use introspection to find known-good values for test assertions.

    Loads the model given by a part of `name`.  For instance, pass in
    'foo.bar.baz.t_qux' to locate and load the module `..expected.qux`.
    """
    _, mod_name = name.split('.')[-1].split('_', 1)
    relative_mod_name = '..expected.' + mod_name
    try:
        return importlib.import_module(relative_mod_name, __name__)
    except ImportError as ie:
        msg = "Eror importing expectations from {}.".format(relative_mod_name)
        raise ImportError(msg, ie.args)

@pytest.fixture
def expected(request):
    """Load the expectations for the running test.

    For example, assume a test named 't_process' in t_modis.py.
    expected() will then load a result object with values from
    expected.modis.t_process.
    """
    module = load_expectation_module(request.module.__name__)
    return GipsProcResult(**getattr(module, request.function.func_name))
