#!/usr/bin/env python
################################################################################
#    GIPS: Geospatial Image Processing System
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

"""Submit a zonal summary job to the gips data handler for remote execution.

Several settings are needed for this; docs are TODO.  Example call:

    gips_zs modis ndvi /path/to/NHseacoast.shp 2012-12-01,2012-12-03 some.csv

The shapefile and output file paths are in terms of the remote worker
context; no file transport is supported.  A gips_zs invocation will
result in these remote tasks as needed:
  query:  determine which assets and products are needed
  fetch:  download assets from the data provider, if needed
  process:  generate products from the assets (ndvi in this case), if needed
  export:  export products into the given shape
  aggregate:  compute summary values for the exported data, save in CSV
"""

from __future__ import print_function

import sys
import os
import argparse

from gips import __version__ as gipsversion

title = 'GIPS Zonal Summary (v' + gipsversion + ')'

def parse_args():
    """Parse command-line arguments via argparse."""
    # not using gips.parsers due to semantic mismatch and correctness issues
    epilog = 'For help on each command: {} {{submit,status}} -h'.format(
            os.path.basename(sys.argv[0]))
    cmd_parser = argparse.ArgumentParser(description=title, epilog=epilog)
    sp = cmd_parser.add_subparsers(dest='cmd', help='Whether to submit or check on job')

    # set up for 'submit' command
    submit_p = sp.add_parser('submit', help='Submit a new job')
    [submit_p.add_argument(arg, help=desc) for arg, desc in (
        ('provider', 'Choose the data source for the summary'),
        ('product',  'Choose a product'),
        ('site',     'Define geographic boundaries for the summary'),
        ('dates',    'Range of dates (YYYY-MM-DD,YYYY-MM-DD)'),
        ('outfile',  'Name of file in which to save CSV output'),
    )]

    # set up for 'status' command
    status_p = sp.add_parser('status', help='Show status of an existing job')
    status_p.add_argument('jobid', help='ID of the job to check up on')

    # both commands need --verbose; for this simple case parents=[..] isn't worthy
    for p in submit_p, status_p:
        p.add_argument('-v', '--verbose', help='Verbosity - 0: quiet, 1: normal, 2+: debug',
                       default=1, type=int, choices=range(0, 7))

    return cmd_parser.parse_args()


def main():
    args = parse_args()

    print(title)

    if args.verbose > 1:
        print('Arguments & options:')
        print('  command:', args.cmd)
        if args.cmd == 'submit':
            print('  provider:', args.provider)
            print('  product:', args.product)
            print('  site:', args.site)
            print('  dates:', args.dates)
            print('  outfile:', args.outfile)
        elif args.cmd == 'status':
            print('  jobid:', args.jobid)
        else:
            raise RuntimeError('Unreachable line reached')
        print('  verbose:', args.verbose)

    # TODO:
    #   submit:  no blocking on job completion; it outputs a job id
    #   status:  input job id, output is status report

    raise NotImplementedError('UX framing is ready but implementation is not.')


if __name__ == "__main__":
    main()
