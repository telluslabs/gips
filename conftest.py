import logging
import envoy

# configure logging (can config in command-line & config file, see below)
log_format = '%(levelname)-8s %(filename)s:%(lineno)d: %(message)s'
root_logger = logging.getLogger()
root_streamer = logging.StreamHandler()
root_streamer.setFormatter(logging.Formatter(log_format))
root_logger.addHandler(root_streamer)

logger = logging.getLogger(__name__)

# pytest_* functions are hooks automatically detected by pytest
def pytest_addoption(parser):
    """Add custom options & settings to py.test.

    These set up the data repo & configure log level."""
    help_str = ("Set log level to one of:  'debug', 'info', 'warning', "
                "'error', or 'critical'.  Default is 'warning'.")
    parser.addoption("--log-level", action="store",
                     default="warning", help=help_str)

    help_str = "Set up a test data repo & download data for test purposes."
    parser.addoption("--setup-repo", action="store_true", help=help_str)

    help_str = ("The directory housing the data repo for testing purposes.  "
                "MUST match GIPS' configured REPOS setting.")
    parser.addini('data-repo', help=help_str)


def pytest_configure(config):
    """Process user config & command-line options."""
    root_logger.setLevel(config.getoption("log_level").upper())

    if config.getoption("setup_repo"):
        logger.debug("--setup-repo detected; setting up data repo")
        setup_data_repo()

    dr = str(config.getini('data-repo'))
    if not dr:
        raise ValueError("No value specified for 'data-repo' in pytest.ini")
    else:
        logger.debug("value detected for data-repo: " + dr)


def setup_data_repo():
    """Construct the data repo if it is absent."""
    # confirm the user's done basic config
    gcp = envoy.run("gips_config print")
    if gcp.status_code != 0:
        raise RuntimeError("config check via `gips_config print` failed",
                           gcp.std_out, gcp.std_err, gcp)
    logger.debug("`gips_config print` check succeeded.")

    # set up data root if it isn't there already
    gcp = envoy.run("gips_config env")
    if gcp.status_code != 0:
        raise RuntimeError("data root setup via `gips_config env` failed",
                           gcp.std_out, gcp.std_err, gcp)
    logger.debug("`gips_config env` succeeded; data repo (possibly) created")
