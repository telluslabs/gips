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

Several settings are needed for this; docs are TODO.  Example calls:

    gips_zs submit modis_indices_satvi /path/to/NHseacoast.shp 2012-12-01,2012-12-03
    gips_zs status 937

The shapefile and output file paths are in terms of the remote worker
context; no file transport is supported.  A gips_zs invocation will
result in these remote tasks as needed:
  query:  determine which assets and products are needed
  fetch:  download assets from the data provider, if needed
  process:  generate products from the assets (ndvi in this case), if needed
  export:  export products into the given shape
  aggregate:  compute summary values for the exported data
"""

from __future__ import print_function

import sys
import os
import argparse
import xmlrpclib

from gips import __version__ as gipsversion
from gips import utils as gips_utils
from gips.scripts import util
from gips.scripts.util import vprint

title = 'GIPS Zonal Summary (v' + gipsversion + ')'


def rpc_conn():
    """Return a connection to the RPC server; uses gips setting DH_API_SERVER."""
    return xmlrpclib.ServerProxy(gips_utils.settings().DH_API_SERVER, use_datetime=True)


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
        ('site_name', 'User-specified keyword or nickname; no computational purpose'),
        ('data_spec', 'Combination of driver, product, and band'),
        ('site',      'Define geographic boundaries for the summary'),
        ('dates',     'Range of dates (YYYY-MM-DD,YYYY-MM-DD)'),
    )]

    # set up for 'status' command
    status_p = sp.add_parser('status', help='Show status of an existing job')
    status_p.add_argument('job_id', help='ID of the job to check up on')

    # both commands need --verbose; for this simple case parents=[..] isn't worthy
    for p in submit_p, status_p:
        p.add_argument('-v', '--verbose', help='Verbosity - 0: quiet, 1: normal, 2+: debug',
                       default=1, type=int, choices=range(0, 7))

    # parse, report, return
    args = cmd_parser.parse_args()
    util.set_verbosity(args.verbose)
    vprint(2, 'Verbosity level:', args.verbose)
    vprint(3, 'Arguments & options:')
    vprint(3, '  command:', args.cmd)
    if args.cmd == 'submit':
        vprint(3, '  site_name:', args.site_name)
        vprint(3, '  data_spec:', args.data_spec)
        vprint(3, '  site:', args.site)
        vprint(3, '  dates:', args.dates)
    elif args.cmd == 'status':
        vprint('  job_id:', args.job_id)
    else:
        raise RuntimeError('Unreachable line reached')
    return args


def submit(site_name, data_spec, site, dates):
    """Performs job submissions, returns the job id."""
    job_id = rpc_conn().submit_job(site_name, data_spec,
                                   {'site': site, 'key': 'shaid'}, {'dates': dates})
    vprint(0, 'Job submitted; job ID:', job_id)


def status(job_id):
    """Performs status check; returns current status."""
    # TODO handle cases(?):
    #   no such job
    #   finished & succeeded - and show the outcome data
    #   finished & failed
    #   job is ongoing
    results = rpc_conn().stats_request_results({'job': job_id})
    # expected results:
    '''
    [
        { . . . }, # one dict per day
        {
            'count': 10118,
            'skew': -4.1808,
            'maximum': 0.7466,
            'site': '',
            'job': 68,
            'minimum': -1.0002,
            `date': datetime.datetime(2013, 4, 28, 0, 0),
            'mean': 0.541821,
            'shaid': '1',
            'id': 1487043,
            'sd': 0.105745,
        },
    ]
    '''
    vprint(results)


def main():
    vprint(1, title)
    a = parse_args()

    if a.cmd == 'submit':
        submit(a.site_name, a.data_spec, a.site, a.dates)
    elif a.cmd == 'status':
        status(a.job_id)
    else:
        raise RuntimeError('Unreachable line reached')


if __name__ == "__main__":
    main()
