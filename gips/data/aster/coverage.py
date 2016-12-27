#!/usr/bin/env python

""" Compile comprehensive tabular database of ASTER scenes """

import os
import re
import datetime
import time
import random

import wget
import xml.etree.ElementTree as ET

import fiona
from shapely.geometry import Polygon
from functools import partial
import pyproj
from shapely.ops import transform

from pdb import set_trace


ROOTURL = "http://e4ftl01.cr.usgs.gov/ASTT/AST_L1T.003"
STARTDATE = datetime.date(2000, 3, 6)
#ENDDATE = datetime.date(2016, 6, 30)
ENDDATE = datetime.datetime.now().date()
OUTDIR = "/data/aster/db"
TIMEOUT = 60
SLEEP = 0.1
AUTH = ('bobbyhbraswell', 'Coffeedog_2')


def main():

    ndays = (ENDDATE - STARTDATE).days + 1
    
    for nday in range(ndays):
        date = STARTDATE + datetime.timedelta(nday)
        datestr = date.strftime('%Y.%m.%d')
        outpath = os.path.join(OUTDIR, datestr + ".csv")
        if os.path.exists(outpath):
            continue

        print "trying", outpath
        
        mainurl = ROOTURL + "/" + datestr
        pattern = '(AST_L1T_\d{17}_\d{14}_\d+.hdf)'
        cpattern = re.compile(pattern)

        listing = wget.get(mainurl, auth=AUTH).split('\n')
        
        if listing == '':            
            continue

        print "there is a listing"
        
        opened = False
        for item in listing:            
            if cpattern.search(item):
                if 'xml' not in item:

                    name = cpattern.findall(item)[0]
                    url = mainurl + "/" + name
                    xmlname = name + ".xml"
                    xmlurl = mainurl + "/" + xmlname
                    print xmlname, xmlurl
                    
                    data = wget.get(xmlurl, auth=AUTH)                    

                    tries = 0
                    done = False
                    while not done:
                        try:
                            root = ET.fromstring(data)
                            done = True
                        except:
                            print "failed to read from", xmlurl
                            tries += 1
                            time.sleep(5)
                        if tries > 9:
                            done = True

                    boundary = root.findall('./GranuleURMetaData/SpatialDomainContainer/HorizontalSpatialDomainContainer/GPolygon/Boundary')
                    coords = []
                    for point in boundary[0].findall('Point'):                        
                        coords.append((float(point.find('PointLongitude').text), float(point.find('PointLatitude').text)))
                    poly = Polygon(coords)
                    polystr = "'%s'" % poly.wkt                    
                    daynight = root.findall('GranuleURMetaData/ECSDataGranule/DayNightFlag')[0].text
                    psas = root.findall('GranuleURMetaData/PSAs/PSA')
                    for psa in psas:
                        if psa.find('PSAName').text == "UTMZoneNumber":
                            utmzone = psa.find('PSAValue').text
                            break
                    outstr =  ','.join([url, polystr, daynight, utmzone])

                    print outstr

                    if opened == False:
                        outfile = open(outpath, 'w')
                        opened = True
                    outfile.write(outstr+'\n')

        if opened == True:
            outfile.close()
        
if __name__ == "__main__":
    main()
