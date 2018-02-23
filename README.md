
## General

Geokit Data Handler (GIPS) was developed by Applied Geosolutions, LLC (AGS) with support from a NASA
Small Business Innovative Research grant (SBIR), in two grant Phases, beginning
January 2014. For more information about the company please contact info@ags.io,
for more information about Geokit open source development contact
developers@ags.io

## Installation

After cloning this git repo & changing to its directory, run `install.sh`,
which only officially supports recent versions of Ubuntu.  It will use `sudo`
to install system packages, and may ask for authentication accordingly.  It
runs apt-get, which may prompt you for confirmation of its actions.
Finally, the script will show you how to set GIPS system settings with
`gips_config`.

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

## Environment

`GIPS_ORM` controls whether or not the GIPS ORM is activated.  The ORM is
enabled by default, and if `GIPS_ORM` is set to either "true" (regardless of
case) or any non-zero number.  Setting it to "false", 0, or any other value
disables the ORM.

## Authors and Contributors
The following have been authors or contributers to GIPS

    Matthew Hanson, matt.a.hanson@gmail.com
    Bobby Braswell (Rob), rbraswell@appliedgeosolutions.com
    Ian Cooke, icooke@appliedgeosolutions.com
    Tom Olson, tolson@appliedgeosolutions.com

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
