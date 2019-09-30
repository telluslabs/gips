[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.1289915.svg)](https://doi.org/10.5281/zenodo.1289915)

# GIPS

See http://gipit.github.io/gips/ for documentation, but know it is not
~~necessarily~~ current.

## Installation

After cloning this git repo & changing to its directory, run `install.sh`,
which only officially supports recent versions of Ubuntu.  It will use `sudo`
to install system packages, and may ask for authentication accordingly.  It
runs apt-get, which may prompt you for confirmation of its actions.
Finally, the script will show you how to set GIPS system settings with
`gips_config`.

## Configuration

### GIPS Settings

`STATS_FORMAT` controls the way `gips_stats` formats its output, and is passed
in to python's `cvs.writer` as a dict of keyword options.

`GIPS_ORM` controls whether the ORM is activated, and whether gips will keep
an inventory of its content in the database configured in `DATABASES`.

### MODIS configuration note

If you wish to work with modis data, edit `~/.gips/settings.py` (if
that file doesn't exist, run `gips_config user` to create it) and
alter the `'modis'` entry in the `REPOS` dict by adding the following
to the end of that file:

```
REPOS['modis'].update(
    {
        'username': 'YOUR-EARTHDATA-USERNAME',
        'password': 'YOUR-EARTHDATA-PASSWORD', # Use os.environ to avoid saving
                                               # a password in a file.
    }
)
```

This username and password must match your Earthdata credentials; for more
information on obtaining credentials:

https://lpdaac.usgs.gov/about/news_archive/important_changes_lp_daac_data_access

For information on setting up automated testing, see `gips/test/README.md`.

### Landsat S3 Configuration Note

GIPS supports Landsat data access via AWS S3:

https://aws.amazon.com/public-datasets/landsat/

Most GIPS products are supported if you have API access to AWS:

https://aws.amazon.com/premiumsupport/knowledge-center/create-access-key/

Provide the special access tokens via environment variable:

```
export AWS_ACCESS_KEY_ID='your-id'
export AWS_SECRET_ACCESS_KEY='your-key'
```

Finally set `settings.py` to tell gips to fetch C1 assets from S3:

```
REPOS = {
    'landsat': {
        # . . .
        'source': 's3', # default is 'usgs'
    }
}
```

After this is done, `gips_inventory --fetch`, `gips_inventory`, and
`gips_process -p <product-list-here>` should work for S3 assets.

Contributor & Developer Guide
-----------------------------
We're grateful for any contributions to GIPS.  Guidelines:

* New code should be based on branch 'dev'; we use 'master' for official
  releases.
* Keep your diff to about 500 lines or less, breaking up your PRs if needed
  (use feature toggles etc to keep the dev branch clean).
* Style:  For new code, follow PEP8, but know that we're loose about some of
  its rules (such as two spaces before a comment).  Also, don't reformat files
  for compliance alone.
* Testing:  New code should be covered by unit tests.  Know also that we use
  an internal CI pipeline to run our suite of system tests and won't generally
  merge code that breaks them.  See `gips/test/README.md` for details.
* These rules aren't absolute; ask if you feel an exception is warranted.


## Authors and Contributors
The following have been authors or contributers to GIPS

    Bobby Braswell (Rob), rbraswell@appliedgeosolutions.com
    Ian Cooke, icooke@appliedgeosolutions.com
    Rick Emery, remery@appliedgeosolutions.com
    Justin Fisk, jfisk@appliedgeosolutions.com
    Matthew Hanson, matt.a.hanson@gmail.com
    Tom Olson, tolson@appliedgeosolutions.com
    Nate Rubin, nrubing@appliedgeosolutions.com

## License (GPL v3)

    Copyright (C) 2014-2018 Applied Geosolutions, oss@appliedgeosolutions.com

    This program is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

   You should have received a copy of the GNU General Public License
   along with this program. If not, see <http://www.gnu.org/licenses/>
