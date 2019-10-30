GIPS Automated Testing
======================
See also `docker/README.md`.

See the end of this file for a quick-start section, after configuring pytest:

Configuration
-------------
Create a file named `pytest.ini` in the project directory, and use it to set
the `data-repo` and `output-dir` settings to full paths to the respective
directories.

```
[pytest]
# these will save time/prevent certain errors
testpaths = gips/test
norecursedirs = .venv data-root
# GIPS' configured data repository:
data-repo = /home/your-user-name-here/src/gips/data-repo
# a directory of your choice, used for output from, e.g., gips_project
output-dir = /home/your-user-name-here/src/gips/testout

# These should remain as they are (placing them in a committed file is a TODO):
python_functions =  t_
python_classes =    T_
python_files =      t_*.py
DJANGO_SETTINGS_MODULE=gips.inventory.orm.settings

# config for artifact store
artifact-store-path     = /ask/for/this/value
```

Library Dependencies
--------------------
GIPS automated testing uses a few libraries, mainly pytest and mock, and a
library for gluing them together (pytest-mock).  These are installed by
the gips installation process.  Further reading:

* Pytest:  http://docs.pytest.org/en/latest/index.html
* Mock:  http://www.voidspace.org.uk/python/mock/
* pytest-mock:  https://pypi.python.org/pypi/pytest-mock
* pytest-django:  https://pytest-django.readthedocs.io/en/latest/

Test selection
--------------
Running unit tests is straightforward, as is selecting specific tests:

https://pytest.org/latest/usage.html#specifying-tests-selecting-tests

You can also select tests based on mark (marks are tags for tests):

https://pytest.org/latest/example/markers.html

Examples:

```
py.test                 # only runs non-system tests (should be fast)
py.test -k inventory    # use py.test's -k to select tests conveniently:
========================= test session starts =========================
platform linux2 -- Python 2.7.11+, pytest-2.9.2, py-1.4.31, pluggy-0.3.1
Django settings: gips.inventory.orm.settings (from ini file)
rootdir: /home/tolson/src/gips, inifile: pytest.ini
plugins: mock-1.1, django-3.0.0, cov-2.2.1, timeout-1.0.0
collected 112 items

gips/test/sys/t_landsat.py s    # skips system tests by default; see --sys
gips/test/sys/t_modis.py s
gips/test/sys/t_prism.py s
gips/test/sys/t_script_invocation.py s
gips/test/unit/t_inventory.py ..
gips/test/unit/t_inventory_settings.py ..

=============== 104 tests deselected by '-kinventory' =================
======== 4 passed, 4 skipped, 104 deselected in 0.51 seconds ==========
```

**Important caveat:** If you specify the same test file multiple times on the
command line (say, to specify multiple tests in that file), any module-scoped
test fixtures will run once for each time the file is listed, which may not be
what was expected.  This is because pytest sees each item on the command line
as a separate run of the module, even though really it's the same file listed
mulitple times.  Instead, avoid the problem by using `-k` to specify tests.

Writing Unit Tests with Mocking
===============================
First, reading about fixtures is especially recommended as the GIPS test suite
uses them substantially:

http://pytest.org/latest/fixture.html

Automated testing can be difficult due to the code's interaction with the
outside.  Some interactions may be undesirable for testing purposes, such as
access to an RNG or the network.  Others may be important to observe for
testing purposes, but it may be difficult to do so.  For instance, if a
function makes a library call, it may be useful to know what the arguments
were, but difficult to measure without special tools.

One such special tool is python's mock library.  `t_auth_settings` in
`gips/test/unit/t_modis_fetch.py` is a good example:  Due to `fetch_mocks`, no
real I/O is permitted, and instead, every outside interaction in
`modis.modisAsset.fetch` is carefully monitored.  The goal of the test is to
confirm that `fetch` only asks for auth credentials when circumstances warrant,
so calls to `get_setting` are intercepted and checked accordingly.

Mocking is a complex subject; read about it here:

http://www.voidspace.org.uk/python/mock/

And here, for the pytest version: https://pypi.python.org/pypi/pytest-mock

Testing in Conjunction with the Django ORM
==========================================
Mark unit tests that will interact with the database with
`@pytest.mark.django_db`.  That causes the test to be isolated from the
configured GIPS database, and instead work with a cleanly instantiated test
database.  Usually the application of this mark is all that is required for the
test; no other special code is needed.

That mark is from pytest-django, a special plugin to glue the Django testing
framework to pytest.  Django's testing framework:

https://docs.djangoproject.com/en/1.10/topics/testing/

Docs for the plugin:

https://pytest-django.readthedocs.io/en/latest/

Running System Tests
====================
Each test runs `gips_something` commands, usually just one, as subprocesses.
The test harness observes the filesystem before and after the test, and any
created files are observed.  These observations are then compared with known
correct values to see if the test ought to pass.

System tests require a little setup, unfortunately:  Edit `settings.py` and
set `GIPS_OVERRIDE_VERSION` to the version the system tests expect.  You can
check this by looking in `gips/test/sys/expected/modis.py` and checking on the
version that is expected to be output.  You should also have a correct
`pytest.ini` file (see above).  Back up any data files you want to retain in
your data repo directory; some system tests need to operate destructively on
it.

System tests check gips' ability to process input files into output files, and
ultimately depend on data downloaded from official sources, such as landsat
images.  To avoid excess fetching from official servers, the test suite uses a
shared artifact store, which the gips system tests know to access if required:

```
# be sure to set artifact-store-path in pytest.ini; see above.
py.test --sys              # run tests without emplacing artifacts first
py.test --sys --setup-repo # emplace artifacts then run tests
py.test --sys              # artifacts are retained for subsequent runs
# a more realistic system test run, with several useful options specified:
# (see py.test --help for details; several are GIPS-custom options):
py.test -s -x -vv --sys --setup-repo -k prism
```

If you don't have access to the artifact store, it can be built by running
gips commands and copying artifacts into place, eg:

```
$ gips_inventory $DRIVER -d $DATES -s $SHAPEFILE --fetch # see driver_setup.py
$ grep artifact-store-path pytest.ini # to know where to put artifacts
$ # repeat as necessary:
$ cp /path/to/gips/repo/$DRIVER/tiles/$TILE/$DATE/$ARTIFACT \
> $ARTIFACT_STORE_PATH/$DRIVER
```

Also some specially-marked tests are skipped unless command-line options are
given; this is for performance and safety reasons.  The repo-altering tests,
mostly tests of `gips_inventory --fetch`, will always be skipped without the
`--src-altering` option.  Some other tests may not run unless `--slow` is
given.  Note also that the source-altering tests may leave the repo in a state
that requires `--setup-repo` or `--clear-repo` for the other tests to pass.

Testing Within Docker Containers
--------------------------------
Gips can be built into a docker container; crib the approach in
`docker/README.md` and see also `.gitlab-ci.yml`.  Note exposing the artifact
store to the container:

```
$ docker run --rm -it \
> -v /net/cluster/projects/gips-dev/sys-test-assets:/artifact-store \
> gips_test /bin/bash
gips@c6fa60790073:/gips$ pytest -k aod --sys --setup-repo -s -vv
```

The working copy of gips can be tested without rebuilding the docker image by
adding `-v /path/to/src/gips:/gips`.  This is also useful for saving
recordings of new expectations; see `--record` below.

Writing System Tests:  Testing a New Driver
===========================================
A new driver should have system tests for `gips_process`, `gips_project`, and
`gips_stats`, though in the future minimum test coverage standards may evolve
further.

Thanks to pytest's parametrization, one test function can support many
combinations of drivers and products.  See docs for details:

https://docs.pytest.org/en/latest/parametrize.html

In particular, the three tests live here, but shouldn't need to be modified
to establish system testing for a new driver:

* `gips/test/sys/t_process.py`
* `gips/test/sys/t_project.py`
* `gips/test/sys/t_stats.py`

Instead, these files should be modified:

* `gips/test/sys/expected/*_process.py`:  Known-good outcomes for `t_process`
* `gips/test/sys/expected/*_project.py`:  Known-good outcomes for `t_project`
* `gips/test/sys/expected/std_stats.py`:  Known-good outcomes for `t_stats`
* `gips/test/sys/driver_setup.py`:  Configuration & any special code the
  driver may need.

Be aware that an older infrastructure may exist in the gips system test suite,
that exists alongside this one.  They interact minimally or not at all.

Recipe for Testing a New Driver
-------------------------------
Say we're testing the new `granitesat` driver, which has the products `snow`
and `ice`.  Open the file `gips/test/sys/driver_setup.py`, and add a line to
`STD_ARGS` to tell the test suite what scene(s) to operate on:

```
STD_ARGS = {
    # . . . various drivers listed here already . . .
    'granitesat': ('granitesat', '-s', nh_shp, '-d', '2018-001,2018-005', '-v4'),
}
```

Then open the file `gips/test/sys/expected/std_process.py` and add these
lines; this tells the test suite what products to test:

```
expectations['granitesat'] = {
    'snow': [], # the expectation list is intentionally empty for now . . .
    'ice': [],
}
```

Now record expectations for the new driver's process testing:

```
$ pytest -s -vv gips/test/sys/t_process.py --sys -k granitesat --record=rec.py
```

You should observe your `snow` and `ice` tests passing; in this case it means
a recording was made successfully for each product.  These recordings are
saved to `rec.py`; open it and see what files were created during the
recording.  Confirm that the right files were created, and remove any entries
that aren't important to the test (such as `.index` files).  Then copy the
contents of `rec.py` to `gips/test/sys/expected/std_process.py`, replacing the
content of `expectations['granitesat']`.  Then re-run process testing and
observe that the tests pass:

```
$ # Test runs presently don't clean up after themselves, so we have to do it:
$ find your-data-repo/granitesat/ -name '*.tif' -delete # vary as needed
$ # note no --record=rec.py this time:
$ pytest -s -vv gips/test/sys/t_process.py --sys -k granitesat
```

The process can be repeated for `t_project` and `t_stats`.  Again, the test
suite doesn't perform cleanup, so remove your `OUTPUT_DIR` between test runs.

If your new driver has many products, follow the pattern of `modis` and place
your expectations in a separate file, and import its content into eg
`std_process.py`.

If your driver needs additional system tests that don't follow the standard
parttern, you can place these in their own test file, eg:
`gips/test/sys/t_granitesat.py`

Caveats & Tips
==============
If you want to view `print` statements, or if you want to run the debugger
(`import pdb; pdb.set_trace()`) you _must_ specify `py.test -s`. This is due to
pytest's somewhat draconian defaults regarding the brevity of test run output
by default.

Quick Start
===========
```
py.test # run unit tests (after activating your virtualenv)

# realistically, a system test run for a specific driver looks like this:
py.test -s -x -vv --sys --setup-repo -k prism

# the help message for pytest includes help for custom options, such as
# --sys, and --setup-repo:
py.test --help
```
