#!/usr/bin/env python
###############################################################################
#    GIPS: Geospatial Image Processing System
#
#    AUTHOR: Matthew Hanson
#    EMAIL:  mhanson@ags.io
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
###############################################################################

import os

from multiprocessing import Pool
from gippy import GeoImage, GeoFeature, GeoImages, GeoVector
from gippy.algorithms import CookieCutter
from gips.inventory import ProjectInventory
from gips.utils import VerboseOut


VALID_STATS = [
    'min',
    'max',
    'mean',
    'sd',
    'skew',
    'count'
]

def cookie_cutter_worker(args):
    try:
        inimg = GeoImage(args['tif'])
        if args['no_data']:
            inimg.SetNoData(args['no_data'])

        gv = GeoVector(args['shp'])
        feat = gv[args['index']]
        
        at = False
        if args['alltouch']:
            at = True

        CookieCutter(
            GeoImages([args['tif']]),
            feat,
            args['new_name'],
            abs(inimg.Affine()[1]),
            abs(inimg.Affine()[5]),
            True,
            1,
            {},
            at
        )
    except Exception as e:
        if not args['coe']:
            print "Error cutting FID {}".format(args['index'])
            raise e
        

def stats_worker(args):
    try:
        passthrough = args['passthrough']
        attr_list = args['attribute_list']
        attrs = args['attributes']
        proj_dir = args['proj_dir']
        bands = args['bands']
        percentiles = args['percentiles']
        date = args['date']
        product = args['product']
        key = args['key']
        req_stats = args['req_stats']

        inv = ProjectInventory(proj_dir)
        date_str = date.strftime('%Y-%j')

        VerboseOut('Calculating statistics for {}'.format(date_str), 2)
        img = inv[date].open(product)
        results = {}

        if passthrough:
            attributes = {}
            for att in attr_list:
                attributes[att] = attrs[att]
            results['passthrough'] = attributes

        band_name_list = []
        for i in range(img.NumBands()):
            band = img[i]
            if len(bands) > 0 and str(i) not in bands:
                continue
            stats = band.Stats()
            stat_arr = build_stat_array(req_stats, stats)
            band_name = band.Description().strip()
            if not band_name:
                band_name = "Band" + str(i)
            band_name_list.append(band_name)
            results[band_name] = stat_arr
            if percentiles:
                percen_arr = []
                ############################################################
                # DO NOT REMOVE THIS LINE OF CODE OR THE WORLD WILL END!!!!!
                print band.Histogram(100, True) * 100
                # 
                ############################################################
                for percen in percentiles:
                    percen_arr.append(band.Percentile(percen))
                results[band_name] += percen_arr
        return (key, results, band_name_list)
    except Exception as e:
        key = args['key']
        if args['coe']:
            results = {}
            if passthrough:
                results['passthrough'] = ['err' for i in attr_list]
            results['BandErr'] = ['err' for i in req_stats].extend(
                ['err' for i in percentiles]
            )
            return (key, results, ['BandErr'])
        else:
           msg = 'FID {}, date {}, prod {}: '.format(key[0], key[1], key[2])
           msg += e
           print msg
           raise e


def get_attributes_list(shp):
    try:
        gv = GeoVector(shp)
    except:
        raise Exception("Invalid shapefile \"{}\"".format(shp))

    attribute_list = gv.Attributes()    
    return attribute_list


def get_features_list(shp, filt=None):
    try:
        gv = GeoVector(shp)
    except:
        raise Exception("Invalid shapefile \"{}\"".format(shp))

    num_features = int(gv.NumFeatures())

    # Set attributes list for possible passthrough
    attribute_list = gv.Attributes()    
    if filt:
        if filt[0] not in attribute_list:
            raise Exception(
                "Invalid attribute {}. Valid attributes are: {}"
                .format(filt[0], attribute_list)
            )
        gfeatures = gv.where(str(filt[0]), str(filt[1]))
    else:
        gfeatures = []
        for gf in gv:
            gfeatures.append(gf)

    return gfeatures


def cut_shp(
    shp, rasters, rasterdates, filt, no_data, num_procs, alltouch, coe,
    invdir
):
    gfeats = get_features_list(shp, filt)

    # Create a spatial_aggregator specific project directory
    proj_dir = os.path.join(invdir, 'spatial_aggregator')
    num_features = len(gfeats)

    work_args = []

    # For feature in the shapefile, cookie cut every image
    for feat in gfeats:
        fid = feat.FID()
        VerboseOut("Cutting feature with FID {}".format(fid), 2)
        fid_dir = os.path.join(proj_dir, str(fid))

        if not os.path.exists(fid_dir):
            os.makedirs(fid_dir)

        workers = []
        for i, tif in enumerate(rasters):

            if rasterdates:
                new_name = os.path.join(
                    fid_dir, "{}_user_ukwn{}".format(rasterdates[i], i)
                )
            else:
                new_name = os.path.join(
                    fid_dir, "1970001_user_ukwn{}".format(i)
                )
            args = {}
            args['tif'] = tif
            args['index'] = feat.Value()
            args['no_data'] = no_data
            args['shp'] = shp
            args['new_name'] = new_name
            args['alltouch'] = alltouch
            args['coe'] = coe

            work_args.append(args)

    try:
        if num_procs == 1:
            mapper = map
        else:
            pool = Pool(processes=num_procs)
            mapper = pool.map
        mapper(cookie_cutter_worker, work_args)
    except Exception as e:
        raise e
        if not coe:
            exit(1)


def write_file(outfile, results, passthrough, req_stats, percentiles, shp):
    bands_list = []
    # First loop: collect band names
    for result in results:
        bands = result[2]
        bands_list.extend(bands)
    # Remove duplicates and sort
    bands_list = sorted(list(set(bands_list)))

    out_file = open(outfile, 'w')
    header = "date,product,fid"

    attribute_list = get_attribute_list(shp)
    if passthrough:
        for att in attribute_list:
            header += ",{}".format(att)

    for b in bands_list:
        if 'min' in req_stats:
            header += ',{0}_min'
        if 'max' in req_stats:
            header += ',{0}_max'
        if 'mean' in req_stats:
            header += ',{0}_mean'
        if 'sd' in req_stats:
            header += ',{0}_sd'
        if 'skew' in req_stats:
            header += ',{0}_skew'
        if 'count' in req_stats:
            header += ',{0}_count'
        for percen in percentiles:
            p_string = '{}_percentile'.format(percen)
            header += ',{0}_' + p_string
        header = header.format(b)

    out_file.write(header + "\n")

    
    # Second loop: write stats
    for result in results:
        key = result[0]
        stats = result[1]

        if 'passthrough' in stats.keys():
            attrs = stats.pop('passthrough')

        key_str = "{},{},{}".format(key[0], key[1], key[2])

        if passthrough:
            for att in attribute_list:
                key_str += ",{}".format(attrs[att])

        band_str = ""
        for band in bands_list:
            if band in stats:
                b_stats = stats.get(band)
                for stat in b_stats:
                    band_str += "," + stat
            else:
                band_str
                band_str += "".join([',' for i in req_stats])
                band_str +="".join([',' for i in percentiles])
        out_file.write(key_str + band_str + "\n")
    out_file.close()


def aggregate(feature_worker=stats_worker, fworker_args=None, **kwargs):
    rasters = kwargs.get('rasterpaths', [])
    shapefile = kwargs.get('shapefile', None)
    req_stats = kwargs.get('stats', VALID_STATS)
    filt = kwargs.get('filter', None)
    percentiles = kwargs.get('percentiles', [])
    passthrough = kwargs.get('passthrough', False)
    bands = kwargs.get('bands', [])
    nodata = kwargs.get('nodata', None)
    rasterdates = kwargs.get('raster_dates', [])
    num_procs = kwargs.get('processes', 1)
    products = kwargs.get('products', [])
    alltouch = kwargs.get('alltouch', False)
    continue_on_error = kwargs.get('continue', False)
    projdir = kwargs.get('projdir')

    if passthrough and not shapefile:
        raise Exception("passthrough requires a shapefile")
    elif rasters and not shapefile:
        raise Exception("rasterpaths requires shapefile")

    if rasterdates and (len(rasterdates) != len(rasters)):
        raise argparse.ArgumentTypeError(
            "There must be one raster date for ever raster"
        )

    features_list = get_features_list(shapefile, filt)

    if not rasters:
        features_list = [
            o for o in os.listdir(projdir) if os.path.isdir(
                os.path.join(projdir, o)
            )
        ]

    attributes_list = get_attributes_list(shapefile)

    table = {}
    max_bands = 0
    if shapefile:
        gfeats = get_features_list(shapefile, filt)
        if rasters:
            cut_shp(
                shapefile, rasters, rasterdates, filt, nodata, num_procs,
                alltouch, continue_on_error, projdir
            )
    num_features = len(features_list)
    worker_args = []
    for feat in features_list:
        if shapefile and rasters:
            fid = feat.FID()
            inv = ProjectInventory(
                os.path.join(
                    projdir, 'spatial_aggregator', str(fid)
                )
            )
        elif shapefile:
            fid = feat.FID()
            inv = ProjectInventory(os.path.join(projdir, str(fid)))
        else:
            fid = feat
            inv = ProjectInventory(os.path.join(projdir, str(fid)))

        attributes = {}
        if passthrough:
            for attribute in attributes_list:
                attributes[attribute] = feat[attribute]

        for date in inv.dates:

            #date_str = date.strftime('%Y-%j')
            #VerboseOut('Calculating statistics for {}'.format(date))
            for product in inv.products(date):
                if products and product not in products:
                    continue
                if fworker_args is not None:
                    args = {}
                    for key in fworker_args:
                        args[key] = fworker_args[key]
                else:
                    args = {}
                args['passthrough'] = passthrough
                args['attribute_list'] = attributes_list
                args['attributes'] = attributes
                args['proj_dir'] = inv.projdir
                args['bands'] = bands
                args['percentiles'] = percentiles
                args['date'] = date
                args['product'] = product
                args['key'] = (date, product,fid)
                args['req_stats'] = req_stats
                args['coe'] = continue_on_error

                worker_args.append(args)

    if num_procs == 1:
        mapper = map
    else:
        pool = Pool(num_procs, maxtasksperchild=1)
        mapper = pool.map


    mapper = map
    try:
        results = mapper(feature_worker, worker_args)
    except:
        if not continue_on_error:
            exit(1)

    return results


def build_stat_array(requested_stats, stat_array):
        stat_arr = []
        if 'min' in requested_stats:
            stat_arr.append(str(stat_array[0]))
        if 'max' in requested_stats:
            stat_arr.append(str(stat_array[1]))
        if 'mean' in requested_stats:
            stat_arr.append(str(stat_array[2]))
        if 'sd' in requested_stats:
            stat_arr.append(str(stat_array[3]))
        if 'skew' in requested_stats:
            stat_arr.append(str(stat_array[4]))
        if 'count' in requested_stats:
            stat_arr.append(str(stat_array[5]))
        return stat_arr
