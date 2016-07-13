Writing System Tests
====================

Eventually we'll have all kinds of tests, probably the standard three
categories of unit, integration, and system.  For now all existing tests are
system tests.  Here's how to write them and run them.  Prerequisites:

1. Make sure GIPS is set up for dev and testing (see the main README).
2. Confirm the existing system tests run (`cd path-to-your-dev-directory &&
   py.test -v`)
3. Edit a file named `gips/test/sys/t_something.py`, adding a simple test
   function to the file: `def t_meta(): assert "Ran correctly!"`
4. Run the test:  `py.test -k t_meta -vv`.  If the test runs and passes, you're
   ready to write system tests.

Optionally, it may be helpful to spend a little time learning pytest in and of
itself:  

http://pytest.org/latest/index.html

It's a unique framework, especially compared with the xUnit way.  Reading about
fixtures is especially recommended:

http://pytest.org/latest/fixture.html


Writing System Tests for a New Driver
-------------------------------------
Use an existing completed driver's test suite as a guide (currently only
modis); a new driver may need a similar collection of tests to be sufficiently
comprehensive.  The files implementing modis' test suite are:

* `t_modis.py`:  Contains most of the test suite.
* `t_repo_src_alteration.py`:  Tests that need to operate destructively on the
  repo should go in here, regardless of driver.
* `gips/test/sys/expected/` Keeps values needed for asserting a test is
  passing.  Each file named `t_something.py` should get a file named
  `something.py` in this directory.

Since automated tests are hopefully independent, each test in the test suite
can be developed and executed separately:

```
#!bash
$ # py.test's `-k` option is pretty magical:
$ py.test -k "modis and inf" # selects a single test, t_modis.py::t_info
```

An example test, explained:

```
!#python
# All three arguments to t_process are fixtures.  Look in `util.py` and
# `conftest.py` files for any that aren't local.
def t_process(setup_modis_data, repo_env, expected):
    """Test gips_process on modis data."""
    # STD_ARGS is an ordinary global provided by `util.py`:
    actual = repo_env.run('gips_process', *STD_ARGS)
    # A fixture provided the value needed for the crucial test
    # assertion; more on that shortly:
    assert expected == actual
```

Each test runs `gips_something` commands, usually just one, as subprocesses.
The test harness captures the command's exit status, standard output, and
standard error.  In addition, the filesystem is observed before and after the
test, and any created, deleted, or updated files are noted.  These observations
(named `actual` in the example) are then compared with known correct values to
see if the test ought to pass.  If there is any mismatch, a diff describing the
problem is displayed.  Finally any cleanup actions occur, which may include
removing created files to leave the filesystem in a pristine state.

The `expected` fixture is somewhat special:  It provides a convenient way to
store bulky data needed for tests in a separate file, without needing to
explicitly access the file itself nor configure anything.  See
`gips/test/sys/expected/modis.py` for the way this works in practice:  The
`expected` fixture looks for an object with the same name as the currently
running test.  It then loads that dictionary into a `GipsProcResult` object,
which is convenient for making assertions in these system tests.

The known-good values stored in `expected/` are usually captured from initial
test runs.  For convenience, newly developed tests may be run with 
`py.test -s --log-level debug`; parts of the output can be cutpasted into an
`expected/` file to establish these needed known-good values.

Caveats & Tips
--------------
If you want to view logger output or `print` statements, or if you want to run
the debugger (`import pdb; pdb.set_trace()`) you _must_ specify `py.test -s`.
This is due to pytest's somewhat draconian defaults regarding the brevity of
test run output by default.
