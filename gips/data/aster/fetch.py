#!/usr/bin/env python

""" Download ASTER data matching a prescribed polygon using the db """

import os
import csv
import datetime
#import urllib, urllib2
import requests
from functools import partial

import fiona
from shapely.geometry import Polygon
from shapely.wkt import loads
from shapely.ops import transform
import pyproj



from pdb import set_trace


DBDIR = "/data/aster/db"
OUTDIR = "/data/aster/test"

USERNAME = "bobbyhbraswell"
PASSWORD = "Coffeedog_2"


# Test times
STARTDATE = datetime.date(2003, 1, 1)
ENDDATE = datetime.date(2016, 12, 31)
#STARTDATE = datetime.date(2010, 6, 1)
#ENDDATE = datetime.date(2010, 6, 30)

# Test locations
SHPFILE = "/home/braswell/gips/gips/data/modis/tiles.shp"
FEATURE = ('cat', 517)
PROJ = "+proj=sinu +lon_0=0 +x_0=0 +y_0=0 +a=6371007.181 +b=6371007.181 +units=m +no_defs"


def getgeom_by_attr(filename, attrname, attrval):
    """ Return matching feature geometry """
    collection = fiona.open(filename)
    for feature in collection:
        if feature['properties'][attrname] == attrval:
            return Polygon(feature['geometry']['coordinates'][0])

        
def main():

    targetpoly = getgeom_by_attr(SHPFILE, FEATURE[0], FEATURE[1])

    reproject = partial(
        pyproj.transform,
        pyproj.Proj(init='epsg:4326'),
        pyproj.Proj(PROJ))

    ndays = (ENDDATE - STARTDATE).days

    for nday in range(ndays):
        date = STARTDATE + datetime.timedelta(nday)
        datestr = date.strftime('%Y.%m.%d')
        
        dbfile = os.path.join(DBDIR, datestr + ".csv")

        try:
            reader = csv.reader(open(dbfile, 'r'), delimiter=",", quotechar="'")
        except IOError:
            print "NO DB FILE", dbfile
            continue
        
        for row in reader:    
            url, polystr, daynight, utmzone = row
            if daynight != 'Day':
                continue
            astpoly_orig = loads(polystr)
            astpoly = transform(reproject, astpoly_orig)
            if astpoly.intersects(targetpoly):
                filename = url.split('/')[-1]
                outpath = os.path.join(OUTDIR, filename)
                if os.path.exists(outpath):
                    print "file already exists"
                    continue
                print "{} -> {}".format(url, outpath)
                kw = {'timeout': 20, 'auth': (USERNAME, PASSWORD)}
                response = requests.get(url, **kw)
                with open(outpath, 'wb') as fd:
                    for chunk in response.iter_content():
                        fd.write(chunk)
                
                #connection = urllib2.urlopen(url)
                #output = open(outpath, 'wb')
                #output.write(connection.read())
                #output.close()
                break

if __name__ == "__main__":
    main()
