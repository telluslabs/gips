#!/usr/bin/env python
################################################################################
#    GIPS: Geospatial Image Processing System
#
#    AUTHOR: Matthew Hanson
#    EMAIL:  matt.a.hanson@gmail.com
#
#    Copyright (C) 2014-2018 Applied Geosolutions
#
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program. If not, see <http://www.gnu.org/licenses/>
################################################################################

import sys
from gips.utils import verbose_out
from . import export

def main():
    verbose_out(
        "\n\n\n    DEPRECATION WARNING\n"
        "   ----------------------\n"
        "   'gips_project' has moved.\n"
        "   It is now called 'gips_export',\n"
        "   and 'gips_project' will be \n"
        "   removed in a future release.\n\n\n",
        0,
        stream=sys.stderr,
    )
    export.main()


if __name__ == "__main__":
    main()
