from __future__ import print_function

import logging
import os
import shutil

import envoy
import pytest
from _pytest.assertion.util import _compare_eq_dict, _diff_text

from gips.test.sys.util import GipsProcResult, set_constants

# configure logging (can config in command-line & config file, see below)
log_format = '%(levelname)-8s %(asctime)s %(filename)s:%(lineno)d: %(message)s'
root_logger = logging.getLogger()
root_streamer = logging.StreamHandler()
root_streamer.setFormatter(logging.Formatter(log_format))
root_logger.addHandler(root_streamer)

_log = logging.getLogger(__name__)

@pytest.fixture
def orm(db, mocker):
    """Garauntee use of the orm, regardless of user setting."""
    # Because tests should be isolated from the environment most of the time.
    mocker.patch('gips.data.core.orm.use_orm', return_value=True)
    yield db

@pytest.fixture
def mpo(mocker):
    """Just to save typing."""
    yield mocker.patch.object

@pytest.fixture
def mock_context_manager(mocker, mpo):
    """Mocks a given context manager.

    Generate the mock by calling the value of this fixture in situ:
    'with location.cm_name() as return_value:'.  location should be a module,
    cm_name is a string naming the context manager to mock, and return_value
    is the mock value emitted by the context manager at runtime.
    """
    def inner(location, cm_name, return_value=None):
        m_context_manager = mpo(location, cm_name).return_value
        if return_value is not None:
            m_context_manager.__enter__.return_value = return_value
        return m_context_manager
    return inner


# pytest_* functions are hooks automatically detected by pytest
def pytest_addoption(parser):
    """Add custom options & settings to py.test.

    These set up the data repo & configure log level."""
    help_str = ("Set log level to one of:  'debug', 'info', 'warning', "
                "'error', or 'critical'.  Default is 'warning'.")
    parser.addoption("--log-level", dest='log_level', help=help_str)
    parser.addoption(
        "--ll",        dest='log_level', help='Alias for --log-level'
    )

    help_str = "Set up a test data repo & download data for test purposes."
    parser.addoption("--setup-repo", action="store_true", help=help_str)

    help_str = (
        "Replace the data repo with a new empty one before testing begins.  "
        "Implies --setup-repo."
    )
    parser.addoption("--clear-repo", action="store_true", help=help_str)

    help_str = ("The directory housing the data repo for testing purposes.  "
                "MUST match GIPS' configured REPOS setting.")
    parser.addini('data-repo', help=help_str)
    parser.addini('output-dir',
                  help="The directory housing output files from test runs.")

    # old bits for ftp access
    #parser.addini('artifact-store-user', help="FTP artifact store username")
    #parser.addini('artifact-store-password',
    #              help="FTP artifact store password")
    #parser.addini('artifact-store-host', help="FTP artifact store hostname")

    # local file store
    parser.addini('artifact-store-path',
                  help="artifact store root path; files are presumed to be"
                       " stored driver-wise beneath this level,"
                       " eg path/sar/asset.tgz")

    parser.addoption(
        "--slow", action="store_true", help="Do not skip @slow tests.")

    parser.addoption(
        "--acolite", action="store_true", help="Don't skip ACOLITE tests."
    )

    help_str = ("Do not skip @src_altering system tests, which are tests that "
                "may alter or remove source data in the repo.")
    parser.addoption("--src-altering", action="store_true", help=help_str)

    help_str = ("Do not skip @system tests, which are tests that may "
                "change elements of the environment as they work.")
    parser.addoption("--sys", action="store_true", help=help_str)

    help_str = ("Whenever a subprocess' output streams are captured via "
                "GipsTestFileEnv, print them out in a format suitable for "
                "cutpasting into an expectations file.")
    parser.addoption(
        "--expectation-format", action="store_true", help=help_str)

    parser.addoption('--record', action='store', default=None,
                     help="Pass in a filename for expecations"
                          " to be written to that filename.")
    # cleanup may not need to be implemented at all
    #parser.addoption('--cleanup-on-failure', action='store_true',
    #        help="Normally cleanup is skipped on failure so you can examine"
    #             " files; pass this option to cleanup even on failure.")

def pytest_configure(config):
    """Process user config & command-line options."""
    raw_level = config.getoption("log_level")
    level = ('warning' if raw_level is None else raw_level).upper()
    root_logger.setLevel(level)

    record_path = config.getoption('record')
    if record_path and os.path.lexists(record_path):
        raise IOError("Record file already exists at {}".format(record_path))

    dr = str(config.getini('data-repo'))
    if not dr:
        raise ValueError("No value specified for 'data-repo' in pytest.ini")
    else:
        _log.debug("value detected for data-repo: " + dr)

    set_constants(config)

    if config.getoption("slow"):
        _log.debug("--slow detected; will not skip @slow tests")

    if config.getoption("clear_repo"):
        _log.debug("--clear-repo detected; trashing and rebuilding data"
                   " repo & inventory DB")
        path = config.getini('data-repo')
        os.path.lexists(path) and shutil.rmtree(path)
        setup_data_repo()
        config.option.setup_repo = True
    elif config.getoption("setup_repo"):
        print("--setup-repo detected; setting up data repo")
        setup_data_repo()
    else:
        print("Skipping repo setup per lack of --setup-repo.")


def setup_data_repo():
    """Construct the data repo if it is absent."""
    # confirm the user's done basic config
    # TODO do these checks every run if fast enough
    gcp = envoy.run("gips_config print")
    if gcp.status_code != 0:
        raise RuntimeError("config check via `gips_config print` failed",
                           gcp.std_out, gcp.std_err, gcp)

    # set up data root if it isn't there already
    gcp = envoy.run("gips_config env")
    if gcp.status_code != 0:
        _log.error("data root setup via `gips_config env` failed; stdout:")
        [_log.error(line) for line in gcp.std_out.split('\n')]
        _log.error("data root setup via `gips_config env` failed; stderr:")
        [_log.error(line) for line in gcp.std_err.split('\n')]
        raise RuntimeError("data root setup via `gips_config env` failed")
    _log.debug("`gips_config env` succeeded; data repo (possibly) created")


def pytest_assertrepr_compare(config, op, left, right):
    """
    When asserting equality between process results, show detailed differences.
    """
    checks = (op == '==',
              isinstance(left, GipsProcResult),
              isinstance(right, GipsProcResult))
    if not all(checks):
        return

    def header_and_indent(header, lines):
        if lines:
            return [header + ':'] + ['  ' + line for line in lines]
        else:
            return [header + ':  matches']

    verbose = config.getoption('verbose')

    output = ['GipsProcResult == GipsProcResult:']

    oper = {True: '==', False: '!='}[left.exit_status == right.exit_status]
    output += ['exit_status:  {} {} {}'
               .format(left.exit_status, oper, right.exit_status)]

    for s in ('stdout', 'stderr'):
        l_compare = getattr(left, 'compare_' + s)
        r_compare = getattr(right, 'compare_' + s)
        if l_compare and r_compare:
            (l_stream, r_stream) = (getattr(left, s), getattr(right, s))
            # TODO text diff breaks due to terminal control sequences (I
            # think it's escaping them wrong or not at all).
            output += header_and_indent(s, _diff_text(l_stream, r_stream, verbose))
        else:
            output += [s + ':  ignored']

    updated_diff = _compare_eq_dict(left.strip_ignored(left.updated),
                                    left.strip_ignored(right.updated),
                                    verbose)
    deleted_diff = _compare_eq_dict(left.strip_ignored(left.deleted),
                                    left.strip_ignored(right.deleted),
                                    verbose)
    created_diff = _compare_eq_dict(left.strip_ignored(left.created),
                                    left.strip_ignored(right.created),
                                    verbose)
    output += header_and_indent('updated', updated_diff)
    output += header_and_indent('deleted', deleted_diff)
    output += header_and_indent('created', created_diff)
    output += header_and_indent('ignored', left.ignored)

    return output
