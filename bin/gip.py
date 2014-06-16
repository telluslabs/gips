#!/usr/bin/env python
################################################################################
#    GIPPY: Geospatial Image Processing library for Python
#
#    Copyright (C) 2014 Matthew A Hanson
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
import sys
import argparse
import commands
import datetime
import shutil
import tempfile

import gippy
from gipif.inventory import project_inventory
from gipif.utils import VerboseOut
from pdb import set_trace

__version__ = '0.6.0'


if __name__ == "__main__":
    dhf = argparse.ArgumentDefaultsHelpFormatter
    parser0 = argparse.ArgumentParser(description='Geospatial Image Processing', formatter_class=dhf)
    subparser = parser0.add_subparsers(dest='command')

    genparser = argparse.ArgumentParser(add_help=False, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    genparser.add_argument('datadir', help='GIPIF Project directory')
    genparser.add_argument('-v', '--verbose', help='Verbosity - 0: quiet, 1: normal, 2: debug', default=1, type=int)

    parser = subparser.add_parser('mask', parents=[genparser], help='Mask files with a product OR file')
    parser.add_argument('-f', '--file', help='Mask files with this file (must have matching dimensions)', default='')
    parser.add_argument('-p', '--product', help='Mask files with this product (in data directory)', default='')
    parser.add_argument('--overwrite', help='Overwrite existing files', default=False, action='store_true')

    #parser = subparser.add_parser('crop', help='Crop raster files to vector extents')
    #parser.add_argument('files', nargs='*', help='Imagery files to extract site area from')
    #parser.add_argument('-v', '--vector', help='Shapefile of site to be extracted from files', required=True)

    args = parser0.parse_args()
    gippy.Options.SetVerbose(args.verbose)

    inv = project_inventory(args.datadir)

    VerboseOut('GIP Utility v%s' % __version__)

    if not os.path.exists(args.datadir):
        raise Exception('Invalid data directory!')

    if args.command == 'mask':
        if args.file == '' and args.product == '':
            raise Exception('No masks supplied!')
        if args.file != '':
            mask_file = gippy.GeoImage(args.file)
        for date in sorted(inv):
            VerboseOut('%s' % date)
            if args.product != '':
                mask_product = gippy.GeoImage(inv[date][args.product])
            for p in inv[date]:
                if args.product != p:
                    fname = inv[date][p]
                    img = gippy.GeoImage(fname)
                    maskit = False
                    if args.file != '':
                        img.AddMask(mask_file[0])
                        maskit = True
                    if args.product != '':
                        img.AddMask(mask_product[0])
                        maskit = True
                    if maskit:
                        VerboseOut('Masking %s' % fname, 2)
                        if args.overwrite:
                            img.Process()
                        else:
                            fout = os.path.splitext(fname)[0]
                            img.Process(fout+'_masked')
                    img.ClearMasks()
                    img = None
            mask_product = None
        mask_file = None

    elif args.command == 'crop':
        for f in args.files:
            start = datetime.datetime.now()
            fbase, ext = os.path.splitext(os.path.basename(f))
            fout = fbase + '_' + os.path.splitext(os.path.basename(args.vector))[0] + ext
            # update to get no data value from source....for that matter do this whole thing with API not cmdline utils
            cmd = 'gdalwarp %s %s -cutline %s -crop_to_cutline -srcnodata 0 -dstnodata -32768' % (f, fout, args.vector)
            if args.resolution:
                cmd = cmd+' -tr %s %s' % (args.resolution, args.resolution)
            if args.overwrite:
                cmd = cmd + ' -overwrite'
            if args.alpha:
                cmd = cmd + ' -dstalpha'
            out = commands.getstatusoutput(cmd)
            print '%s -> %s: %s' % (os.path.basename(f), os.path.basename(fout), datetime.datetime.now()-start)