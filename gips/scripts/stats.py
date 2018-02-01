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

import os
import csv

import gippy
from gips.parsers import GIPSParser
from gips.inventory import ProjectInventory
from gips.utils import Colors, VerboseOut, basename
from gips import utils

__version__ = '0.1.0'

def main():
    title = Colors.BOLD + 'GIPS Image Statistics (v%s)' % __version__ + Colors.OFF

    parser0 = GIPSParser(datasources=False, description=title)
    parser0.add_projdir_parser()
    group = parser0.add_argument_group('masking options')
    args = parser0.parse_args()

    utils.gips_script_setup(stop_on_error=args.stop_on_error)
    print title

    # TODO - check that at least 1 of filemask or pmask is supplied
    header = ['date', 'band', 'min', 'max', 'mean', 'sd', 'skew', 'count']

    with utils.error_handler():
        for projdir in args.projdir:
            VerboseOut('Stats for Project directory: %s' % projdir, 1)
            inv = ProjectInventory(projdir, args.products)

            p_dates = {} # map each product to its list of valid dates
            for date in inv.dates:
                for p in inv.products(date):
                    p_dates.setdefault(p, []).append(date)
            p_dates = {p: sorted(dl) for p, dl in p_dates.items()}

            for p_type, valid_dates in p_dates.items():
                stats_fn = os.path.join(projdir, p_type + '_stats.txt')
                with open(stats_fn, 'w') as stats_fo:
                    # TODO configurable options:
                    # spamwriter = csv.writer(csvfile, delimiter=' ',
                    #         quotechar='|', quoting=csv.QUOTE_MINIMAL)
                    # use utils.settings().STATS_CONF
                    writer = csv.writer(stats_fo)

                    # print header
                    writer.writerow(header)

                    # print date, band description, and stats
                    for date in valid_dates:
                        print '  date: {}'.format(date)
                        img = inv[date].open(p_type)
                        date_str = date.strftime('%Y-%j')
                        for b in img:
                            stats = [str(s) for s in b.Stats()]
                            writer.writerow(
                                    [date_str, b.Description()] + stats)
                        img = None

    utils.gips_exit() # produce a summary error report then quit with a proper exit status


if __name__ == "__main__":
    main()
