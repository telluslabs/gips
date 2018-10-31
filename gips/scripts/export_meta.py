#!/usr/bin/env python
################################################################################
#    GIPS: Geospatial Image Processing System
#
#    AUTHOR: Matthew Hanson
#    EMAIL:  matt.a.hanson@gmail.com
#
#    Copyright (C) 2014 Applied Geosolutions
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

# Modified from gips_export script -- fetches metadata and that is all. Input
# parameters reduced accordingly.

import os
from gips import __version__
from gips.parsers import GIPSParser
from gips.core import SpatialExtent, TemporalExtent
from gips import utils
from gips.inventory import DataInventory

def main():

    title = 'GIPS Metadata Export (v%s)' % __version__

    # argument parsing
    parser0 = GIPSParser(description=title)
    parser0.add_inventory_parser(site_required=True)
    args = parser0.parse_args()

    # set fetch argument to True, this is the whole point of the script
    args_dict = vars(args)
    args_dict['fetch'] = True

    cls = utils.gips_script_setup(args.command, args.stop_on_error)

    with utils.error_handler():
        extents = SpatialExtent.factory(
            cls, site=args.site, rastermask=args.rastermask,
            key=args.key, where=args.where, tiles=args.tiles,
            pcov=args.pcov, ptile=args.ptile
        )

        for extent in extents:
            t_extent = TemporalExtent(args.dates, args.days)
            inv = DataInventory(cls, extent, t_extent, **vars(args))

    utils.gips_exit() # produce a summary error report then quit with a proper exit status


if __name__ == "__main__":
    main()
