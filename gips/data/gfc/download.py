#!/usr/bin/python
'''
getGFCdata.py
-------------
Utility for downloading 10x10 latXlon tiles of forest change data
from Hansen et al Global Forest Change 2013 dataset*.


 * Source: Hansen/UMD/Google/USGS/NASA
'''


import urllib
import os
import argparse
from math import floor, ceil


__version__ = "0.8"
__email__ = "icooke@appliedgeosolutions.com"

_products = ['treecover2000', 'loss', 'gain', 'lossyear',
             'datamask', 'first', 'last']

_datadir = '/titan/data/GFC2015/tiles'

DEBUG = False


class GFCError(Exception):
    pass


def download(products=_products,
             lats=[30, 40, 50],
             lons=[-80, -90, -100, -110, -120, -130],
             outdir='.', force=False):
    """
    getGFCdata
    ----------
    Download the specified products over the lat,lon tiles specified
    """
    global _products
    bad_products = [p for p in products if p not in _products ]
    if len(bad_products) != 0:
        err_str = 'I don''t know the following products: '
        for p in bad_products:
            err_str += '\n    {}'.format(p)
        raise GFCError(err_str)

    if not all(map(lambda x: (x % 10) == 0 and x >= -180 and x < 180, lons)):
        raise GFCError(
            'Longitude must be multiples of 10 within [-180,180):\n' +
            '[' + str(min(lons)) + ', ' + str(max(lons)) + ']\n')
    if not all(map(lambda x: (x % 10) == 0 and x > -60 and x <= 80, lats)):
        raise GFCError(
            'Latitudes must be multiples of 10 within (-60,80]:\n' +
            '[' + str(min(lats)) + ', ' + str(max(lats)) + ']\n')

    prefix = ('http://commondatastorage.googleapis.com/'
              'earthenginepartners-hansen/GFC2015/Hansen_GFC2015_')
    Nlats = filter(lambda x: x >= 0, lats)
    Slats = filter(lambda x: x < 0, lats)
    Elons = filter(lambda x: x >= 0, lons)
    Wlons = filter(lambda x: x < 0, lons)
    urls = map(lambda x: prefix + ('%s_%02dN_%03dW.tif' % x),
               [(prod, la, abs(lo))
                for prod in products
                for la in Nlats
                for lo in Wlons])
    urls += map(lambda x: prefix + ('%s_%02dN_%03dE.tif' % x),
                [(prod, la, lo)
                 for prod in products
                 for la in Nlats
                 for lo in Elons])
    urls += map(lambda x: prefix + ('%s_%02dS_%03dE.tif' % x),
                [(prod, abs(la), lo)
                 for prod in products
                 for la in Slats
                 for lo in Elons])
    urls += map(lambda x: prefix + ('%s_%02dS_%03dW.tif' % x),
                [(prod, abs(la), abs(lo))
                 for prod in products
                 for la in Slats
                 for lo in Wlons])

    report = []
    for url in urls:
        pfx, bn = os.path.split(url)
        ofile = os.path.join(outdir, bn)
        if DEBUG: print('Getting ' + ofile + '\nfrom "' + url + '".' )
        if force or not os.path.exists(ofile):
            urllib.urlretrieve(url, ofile)
        else:
            if DEBUG: print(' ... Already got it.')
        b = os.path.getsize(ofile)
        if b <= 1:
            raise GFCError('Tiny file: {} {}'.format(ofile, b))
        report.append((bn, b))
        if DEBUG: print('{} {} bytes.'.format(ofile, b))
    return report

if __name__ == "__main__":
    prog = os.path.split(__file__)[1]
    parser = argparse.ArgumentParser(
        prog=prog, description='Hansen GFC2015 Downloader',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    ## python getGFCdata.py min_lat max_lat min_lon max_lon prod0 [prod1 ...]
    parser.add_argument(
        '-o', '--out_dir', metavar='dir', nargs=1, type=str,
        default=_datadir,
        help='output directory'
    )
    parser.add_argument(
        '-v', '--verbose', action='store_true',
        default=False,
        help='verbose downloading output'
    )
    parser.add_argument(
        '-f', '--force', action='store_true',
        default=False,
        help='force download, ignore local file if it exists.'
    )
    parser.add_argument(
        '--min_lat', type=float,
        help='lowest latitude of area to download'
    )
    parser.add_argument(
        '--max_lat', type=float,
        help='highest latitude of area to download'
    )
    parser.add_argument(
        '--min_lon', type=float,
        help='lowest longitude of area to download'
    )
    parser.add_argument(
        '--max_lon', type=float,
        help='highest longitude of area to download'
    )
    parser.add_argument(
        'prod', nargs='+', type=str,
        help='GFC2015 products to be downloaded'
    )
    args = parser.parse_args()

    print args

    DEBUG = args.verbose
    min_lat = args.min_lat
    max_lat = args.max_lat
    min_lon = args.min_lon
    max_lon = args.max_lon

    def hansonGridLat(z):
        return int(ceil(z / 10)) * 10

    def hansonGridLon(z):
        return int(floor(z / 10)) * 10

    lats = range(hansonGridLat(min_lat + 10),
                 hansonGridLat(max_lat + 10),
                 10)
    lons = range(hansonGridLon(min_lon),
                 hansonGridLon(max_lon),
                 10)
    if len(lats) == 0 or len(lons) == 0:
        print('Empty range:')
        print 'lats: ', (min(lats), max(lats))
        print 'lons: ', (min(lons), max(lons))
    else:
        try:
            r = download(products=args.prod,
                         lats=lats, lons=lons,
                         outdir=args.out_dir,
                         force=args.force)
            from pprint import pprint as pp
            pp(r)
        except GFCError as gfce:
            print gfce
