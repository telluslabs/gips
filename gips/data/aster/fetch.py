#!/usr/bin/env python

""" Download ASTER data matching a prescribed polygon """

import os
import re
import datetime
import urllib, urllib2
import xml.etree.ElementTree as ET

import fiona
from shapely.geometry import Polygon

from functools import partial
import pyproj
from shapely.ops import transform


from pdb import set_trace


ROOTURL = "http://e4ftl01.cr.usgs.gov/ASTT/AST_L1T.003"
# http://e4ftl01.cr.usgs.gov/ASTT/AST_L1T.003/2013.10.03/AST_L1T_00310032013031653_20150618010058_108124.hdf
# http://e4ftl01.cr.usgs.gov/ASTT/AST_L1T.003/2013.10.03/AST_L1T_00310032013031653_20150618010058_108124.hdf.xml

STARTDATE = datetime.date(2003, 1, 1)
ENDDATE = datetime.date(2015, 12, 31)

MODISTILES = "/home/braswell/gips/gips/data/modis/tiles.shp"
TILEID = "h12v03"
PROJ = "+proj=sinu +lon_0=0 +x_0=0 +y_0=0 +a=6371007.181 +b=6371007.181 +units=m +no_defs"


def getgeom_by_attr(filename, attrname, attrval):
    """ Return matching feature geometry """
    collection = fiona.open(filename)
    for feature in collection:
        if feature['properties'][attrname] == attrval:
            return Polygon(feature['geometry']['coordinates'][0])
        
        
def main():

    tilepoly = getgeom_by_attr(MODISTILES, 'tileid', TILEID)

    project = partial(
        pyproj.transform,
        pyproj.Proj(init='epsg:4326'),
        pyproj.Proj(PROJ))

    ndays = (ENDDATE - STARTDATE).days

    for nday in range(ndays):
        date = STARTDATE + datetime.timedelta(nday)
        datestr = date.strftime('%Y.%m.%d')        
        mainurl = ROOTURL + "/" + datestr
        pattern = '(AST_L1T_\d{17}_\d{14}_\d{6}.hdf)'
        cpattern = re.compile(pattern)                                
        listing = urllib.urlopen(mainurl).readlines()
        
        for item in listing:
            if cpattern.search(item):
                if 'xml' not in item:
                    name = cpattern.findall(item)[0]
                    outpath = os.path.join('/data/aster', name)
                    if os.path.exists(outpath):
                        print "skipping"
                        continue
                    xmlname = name + ".xml"
                    xmlurl = mainurl + "/" + xmlname
                    connection = urllib2.urlopen(xmlurl) 
                    data = connection.read()
                    root = ET.fromstring(data)                    
                    boundary = root.findall('./GranuleURMetaData/SpatialDomainContainer/HorizontalSpatialDomainContainer/GPolygon/Boundary')
                    coords = []
                    for point in boundary[0].findall('Point'):                        
                        coords.append((float(point.find('PointLongitude').text), float(point.find('PointLatitude').text)))
                    poly = Polygon(coords)
                    polysin = transform(project, poly)                    
                    if polysin.intersects(tilepoly):
                        print xmlname                    
                        url = mainurl + "/" + name
                        connection = urllib2.urlopen(url)
                        output = open(outpath, 'wb')
                        output.write(connection.read())
                        output.close()

if __name__ == "__main__":
    main()
