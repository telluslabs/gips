import logging
import envoy

### TODO for logging:
# use logging properly:  logger = logging.getLogger(__name__)
# config in cmd line (verbosity levels)
logging.basicConfig(level=logging.DEBUG)
logger = logging

# pytest_* functions are hooks automatically detected by pytest
def pytest_addoption(parser):
    """Add --setup-repo to py.test to optionally set up a data repo.

    If this option is present, data sources will be downloaded; otherwise
    existing sources are assumed to be sufficient."""
    help_str = "Set up a test data repo."
    parser.addoption("--setup-repo", action="store_true", help=help_str)

def pytest_configure(config):
    """If the user wishes, bring data repo into usable state for testing."""
    if config.getoption("setup_repo"):
        logger.debug("--setup-repo detected; setting up data repo")
        setup_data_repo()

def setup_data_repo():
    """Construct the data repo and populate it with test data."""
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
