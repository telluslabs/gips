# GIPS

See http://gipit.github.io/gips/ for documentation, but know it is not
necessarily current.

## Installation

After cloning this git repo & changing to its directory, run `install.sh`,
which only officially supports recent versions of Ubuntu.  It will use `sudo`
to install system packages, and may ask for authentication accordingly.  It
runs apt-get, which may prompt you for confirmation of its actions.

To permit automated testing, create a file named `pytest.ini` in the project
directory, and use it to set the `data-repo` and `output-dir` settings to full
paths to the respective directories.

```
[pytest]
# GIPS' configured data repository:
data-repo = /home/your-user-name-here/src/gips/data-repo
# a directory of your choice, used for output from, e.g., gips_project
output-dir = /home/your-user-name-here/src/gips/testout
# These should remain as they are (placing them in a config file is a TODO):
python_functions =  t_ test_
python_files =      t_*.py test_*.py
```

## Running Automated tests

The test suite is based on pytest:  https://pytest.org/latest/contents.html

```
#!bash
# to run all tests (after activating your virtualenv):
py.test --setup-repo # only needed for the first run
py.test --clear-repo # destroy and recreate the repo if it's in a bad state
py.test              # save time without --setup-repo
py.test -s           # echo stdout & stderr to console (not shown by default)
```

Select specific tests per usual for pytest:

https://pytest.org/latest/usage.html#specifying-tests-selecting-tests

You can also select tests based on mark (marks are tags for tests):

https://pytest.org/latest/example/markers.html

If you specify the same test file multiple times on the command line (say, to
specify multiple tests in that file), any module-scoped test fixtures will run
once for each time the file is listed, which may not be what was expected.
This is because pytest sees each item on the command line as a separate run of
the module, even though really it's the same file listed mulitple times.
Instead, avoid the problem by using `-k` to specify tests.

## Authors and Contributors
The following have been authors or contributers to GIPS

    Matthew Hanson, matt.a.hanson@gmail.com
    Bobby Braswell (Rob), rbraswell@appliedgeosolutions.com
    Ian Cooke, icooke@appliedgeosolutions.com
    Pavel Dorovskoy, pavel@appliedgeosolutions.com

## License (GPL v2)

    Copyright (C) 2014 Applied Geosolutions, oss@appliedgeosolutions.com

    This program is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 2 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

   You should have received a copy of the GNU General Public License
   along with this program. If not, see <http://www.gnu.org/licenses/>
