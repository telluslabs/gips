#from __future__ import print_function

### WHERE I LEFT THIS:
# working on optional test teardown (removal of created files) on test failure/error
# two approaches, probably going with the second one:
# PS this conftest.py only applies to system tests due to location; nifty!

# https://stackoverflow.com/questions/28198585/pytest-how-to-take-action-on-test-failure/47908872#47908872
"""
def pytest_exception_interact(node, call, report):
    print('pytest_exception_interact')
    import pdb; pdb.set_trace()
    if report.failed:
        print("node:", node)
        print("call:", call)
        print("report:", report)
        # report.outcome == 'failed'
        #import pdb; pdb.set_trace()
"""

# https://docs.pytest.org/en/latest/example/simple.html#making-test-result-information-available-in-fixtures
"""
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    # execute all other hooks to obtain the report object
    outcome = yield
    rep = outcome.get_result()

    # set a report attribute for each phase of a call, which can
    # be "setup", "call", "teardown"

    setattr(item, "rep_" + rep.when, rep)
"""
