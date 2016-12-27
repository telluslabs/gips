# -*- coding: utf-8 -*-
"""
-------------------------------------------------------------------------------
 Open ASTER L1T HDF-EOS and Export as Geotiff Tool
 How To Tutorial
 This tool imports ASTER L1T HDF-EOS files, georeferences, and  exports files 
 as geotiffs.
-------------------------------------------------------------------------------
 Author: Cole Krehbiel
 Contact: LPDAAC@usgs.gov  
 Organization: Land Processes Distributed Active Archive Center
 Date last modified: 8-25-2016
-------------------------------------------------------------------------------
 OBJECTIVE:
 The Advanced Spaceborne Thermal Emission and Reflection Radiometer (ASTER) 
 Level 1 Precision Terrain Corrected Registered At-Sensor Radiance  Dataset 
 (AST_L1T) provides calibrated and geometrically corrected at-sensor radiance 
 for ASTER VNIR (bands 1-3N), SWIR (bands 4-9), and TIR (bands 10-14). 
 ASTER L1T files can be downloaded from the Datapool in HDF-EOS format (.hdf). 
 ASTER L1T is derived from ASTER Level 1A data that has been geometrically 
 corrected and reprojected to a north-up UTM projection. However, when brought
 into GIS or Remote Sensing software programs such as ArcMap or QGIS, the data
 appears to be missing a correctly defined coordinate reference system (CRS). 
 This tutorial demonstrates how a Python script can be used to open ASTER L1T 
 HDF-EOS files, correctly define the CRS, and export each VNIR/SWIR/TIR band
 (14 total) as a GeoTiff that can be loaded with spatial reference into the
 aforementioned GIS/Remote Sensing software programs.

 The tutorials take an ASTER L1T HDF-EOS file (.hdf) as an input and outputs 
 georeferenced tagged image file format (GeoTiff) files for each of the VNIR,
 SWIR, and TIR science datasets contained in the original ASTER L1T file.

 Results from this tutorial are output in Universal Transverse Mercator (UTM)
 with WGS84 as GeoTiff files. The output GeoTiffs for each band include:
 1. Original_AST_L1T_Filename_ImageDataband#.tif
Data is At-Sensor radiance stored as DN.

 This tool was specifically developed for ASTER L1T HDF-EOS files and should 
 only be used for those data products.
-------------------------------------------------------------------------------
 PREREQUISITES
 Python software program version 3.4 or 2.7
 
 Python Packages/Modules:
 osgeo with gdal and osr – 1.11.1 
 numpy – 1.11.0
 os
 glob
datetime
re
-------------------------------------------------------------------------------
 ESTIMATED TIME TO COMPLETE
 Time to complete processing for a single file has typically been < 1 minute 

 NOTE: Estimated completion times will vary by OS and/or machine specifications 
-------------------------------------------------------------------------------
 ADDITIONAL INFORMATION
 LP DAAC ASTER L1T Product Page: 
 https://lpdaac.usgs.gov/dataset_discovery/aster/aster_products_table/ast_l1t
 LP DAAC ASTER L1T User Guide: 
 https://lpdaac.usgs.gov/sites/default/files/public/product_documentation/
 aster_l1t_users_guide.pdf

 This tool will batch process ASTER L1T files if more than 1 is located in the
 working directory.
 Output file directory will be 'inputfiledirectory'+'/output/'
-------------------------------------------------------------------------------
 RELATED TUTORIALS
  ASTERL1T_DN2REF.py --Converts ASTER L1T Radiance (stored as DN) to 
 Top of Atmosphere Reflectance
 
 ASTERL1T_DN2REF.R --Converts ASTER L1T Radiance (stored as DN) to 
 Top of Atmosphere Reflectance
 
 ASTERL1T_hdf2tif.R --Imports ASTER L1T HDF-EOS files, georeferences and
 exports as geotiffs (R equivalent of this script)

 Search for other tools at https://lpdaac.usgs.gov/
-------------------------------------------------------------------------------
 LABELS
 ASTER L1T, Georeference, GeoTiff, HDF-EOS, LP DAAC, Python
-------------------------------------------------------------------------------
"""
#------------------------------------------------------------------------------
# PROCEDURES:
#         IMPORTANT:
# User needs to change the 'in_dir' (working directory) below, denoted by #***

# Load necessary packages into Python
from osgeo import gdal, osr
import numpy as np
import os
import glob
from datetime import datetime
import re
#------------------------------------------------------------------------------
#|                    Batch Process files from directory:                     |
#------------------------------------------------------------------------------

# Set input/current working directory, user NEEDS to change to directory where 
# files will be downloaded to.
in_dir = '/PATH_TO_INPUT_FILE_DIRECTORY/' #***Change, be sure to include '/' 
# at the end of final directory location
os.chdir(in_dir)

# Create and set output directory
out_dir = os.path.normpath((os.path.split(in_dir)[0] + os.sep + 
	'output_python/' ))+ '\\'
if not os.path.exists(out_dir):
    os.makedirs(out_dir)
        
# Create a list of ASTER L1T HDF files in the directory
file_list = glob.glob('AST_L1T_**.hdf')
#------------------------------------------------------------------------------
# Set up calculations
# 1. DN to Radiance (Abrams, 1999)
# Radiance = (DN-1)* Unit Conversion Coefficient

# 2. Radiance to TOA Reflectance
# Reflectance_TOA = (pi*Lrad*d2)/(esuni*COS(z))

# Define the following:
# Unit Conversion Coefficient = ucc
# pi = pi
# Radiance,Lrad  = rad
# esuni = esun 
# z = solare

# Order for ucc (Abrams, 1999) is: Band 1 high, normal, low, low2; 
# Band 2 h, n, l1, l2; b3 h, n, l1, l2 (3N & 3B the same) 
# Construct a dataframe for the UCC values:
ucc = np.matrix(([[0.676, 1.688, 2.25, 0.0],\
                [0.708, 1.415, 1.89, 0.0],\
                [0.423, 0.862, 1.15, 0.0],\
                [0.1087, 0.2174, 0.2900, 0.2900],\
                [0.0348, 0.0696, 0.0925, 0.4090],\
                [0.0313, 0.0625, 0.0830, 0.3900],\
                [0.0299, 0.0597, 0.0795, 0.3320],\
                [0.0209, 0.0417, 0.0556, 0.2450],\
                [0.0159, 0.0318, 0.0424, 0.2650]]))

# Thome et al. is used, which uses spectral irradiance values from MODTRAN
# Ordered b1, b2, b3N, b4, b5...b9
irradiance = [1848, 1549, 1114, 225.4, 86.63, 81.85, 74.85, 66.49, 59.85]

def dn2rad (x):
    rad = (x-1.)*ucc1
    return rad

def rad2ref (rad):
    ref = (np.pi * rad * (esd * esd)) / (irradiance1 * np.sin(np.pi * sza / 
    180))
    return ref
#------------------------------------------------------------------------------
# Loop through all ASTER L1T hdf files in the directory
for k in range(len(file_list)):
    
    # Maintains original filename convention    
    file_name = file_list[k]    

    # Read in the file and metadata
    aster = gdal.Open(file_name)
    aster_sds = aster.GetSubDatasets()
    meta = aster.GetMetadata()
    date = meta['CALENDARDATE']
    dated = datetime.strptime(date, '%Y%m%d')
    day = dated.timetuple()
    doy = day.tm_yday
    
    # Calculate Earth-Sun Distance    
    esd = 1.0 - 0.01672 * np.cos(np.radians(0.9856 * (doy - 4)))    
    
    del date, dated, day, doy    
    
    # Need SZA--calculate by grabbing solar elevation info     
    sza = [np.float(x) for x in meta['SOLARDIRECTION'].split(', ')][1]
   
    # Query gain data for each  band, needed for UCC     
    gain_01 = meta['GAIN.1'].split(', ')[1]
    gain_02 = meta['GAIN.2'].split(', ')[1]
    gain_03b = meta['GAIN.3'].split(', ')[1]
    gain_03n = meta['GAIN.3'].split(', ')[1]
    gain_04 = meta['GAIN.4'].split(', ')[1]
    gain_05 = meta['GAIN.5'].split(', ')[1]
    gain_06 = meta['GAIN.6'].split(', ')[1]
    gain_07 = meta['GAIN.7'].split(', ')[1]
    gain_08 = meta['GAIN.8'].split(', ')[1]
    gain_09 = meta['GAIN.9'].split(', ')[1]

    # Define UL, LR, UTM zone    
    ul = [np.float(x) for x in meta['UPPERLEFTM'].split(', ')]
    lr = [np.float(x) for x in meta['LOWERRIGHTM'].split(', ')]
    utm = np.int(meta['UTMZONENUMBER'])
    n_s = np.float(meta['NORTHBOUNDINGCOORDINATE'])
    
    # Create UTM zone code numbers    
    utm_n = [i+32600 for i in range(60)]
    utm_s = [i+32700 for i in range(60)]
    
    # Define UTM zone based on North or South
    if n_s < 0:
        utm_zone = utm_s[utm]
    else:
        utm_zone = utm_n[utm]
        
    del utm_n, utm_s, utm, meta
#------------------------------------------------------------------------------   
    # Loop through all ASTER L1T SDS (bands)    
    for i in range(len(aster_sds)):
    
        # Maintain original dataset name    
        gname = str(aster_sds[i])
        aster_sd = gname.split(',')[0]
        
        vnir = re.search("(VNIR.*)", aster_sd)
        swir = re.search("(SWIR.*)", aster_sd)
        if vnir or swir:
            # Generate output name for tif            
            aster_sd2 = aster_sd.split('(')[1]
            aster_sd3 = aster_sd2[1:-1]
            band = aster_sd3.split(':')[-1]
            out_filename = out_dir + file_name.split('.hdf')[0] + '_' + band \
            + '.tif'
            out_filename_rad = out_filename.split('.tif')[0] + '_radiance.tif'
            out_filename_ref = out_filename.split('.tif')[0] + \
            '_reflectance.tif'
            # Open SDS and create array            
            band_ds = gdal.Open(aster_sd3, gdal.GA_ReadOnly)
            sds = band_ds.ReadAsArray().astype(np.uint16)
            
            del aster_sd, aster_sd2, aster_sd3
           
           # Define extent and provide offset for UTM South zones            
            if n_s < 0:
                ul_y = ul[0] + 10000000
                ul_x = ul[1]
            
                lr_y = lr[0] + 10000000
                lr_x = lr[1]
    
            # Define extent for UTM North zones            
            else:
                ul_y = ul[0] 
                ul_x = ul[1]
            
                lr_y = lr[0] 
                lr_x = lr[1]
            
            # Query raster dimensions and calculate raster x and y resolution            
            ncol, nrow = sds.shape            
            y_res = -1 * round((max(ul_y, lr_y)-min(ul_y, lr_y))/ncol)
            x_res = round((max(ul_x, lr_x)-min(ul_x, lr_x))/nrow)
            
            # Define UL x and y coordinates based on spatial resolution           
            ul_yy = ul_y - (y_res/2)
            ul_xx = ul_x - (x_res/2)
#------------------------------------------------------------------------------
            # Start conversions by band (1-9)        
            if band == 'ImageData1':
                bn = -1 + 1                
                # Query for gain specified in file metadata (by band)            
                if gain_01 == 'HGH':
                    ucc1 = ucc[bn, 0] 
                elif gain_01 == 'NOR':
                    ucc1 = ucc[bn, 1] 
                else:
                    ucc1 = ucc[bn, 2] 
                    
            if band == 'ImageData2':
                bn = -1 + 2                
                # Query for gain specified in file metadata (by band)            
                if gain_02 == 'HGH':
                    ucc1 = ucc[bn, 0] 
                elif gain_02 == 'NOR':
                    ucc1 = ucc[bn, 1] 
                else:
                    ucc1 = ucc[bn, 2] 
                    
            if band == 'ImageData3N':
                bn = -1 + 3                
                # Query for gain specified in file metadata (by band)            
                if gain_03n == 'HGH':
                    ucc1 = ucc[bn, 0] 
                elif gain_03n == 'NOR':
                    ucc1 = ucc[bn, 1] 
                else:
                    ucc1 = ucc[bn, 2] 
                    
            if band == 'ImageData4':
                bn = -1 + 4                
                # Query for gain specified in file metadata (by band)            
                if gain_04 == 'HGH':
                    ucc1 = ucc[bn, 0] 
                elif gain_04 == 'NOR':
                    ucc1 = ucc[bn, 1] 
                else:
                    ucc1 = ucc[bn, 2] 
                    
            if band == 'ImageData5':
                bn = -1 + 5                
                # Query for gain specified in file metadata (by band)            
                if gain_05 == 'HGH':
                    ucc1 = ucc[bn, 0] 
                elif gain_05 == 'NOR':
                    ucc1 = ucc[bn, 1] 
                else:
                    ucc1 = ucc[bn, 2] 
                    
            if band == 'ImageData6':
                bn = -1 + 6                
                # Query for gain specified in file metadata (by band)            
                if gain_06 == 'HGH':
                    ucc1 = ucc[bn, 0] 
                elif gain_06 == 'NOR':
                    ucc1 = ucc[bn, 1] 
                else:
                    ucc1 = ucc[bn, 2] 
                    
            if band == 'ImageData7':
                bn = -1 + 7                
                # Query for gain specified in file metadata (by band)            
                if gain_07 == 'HGH':
                    ucc1 = ucc[bn, 0] 
                elif gain_07 == 'NOR':
                    ucc1 = ucc[bn, 1] 
                else:
                    ucc1 = ucc[bn, 2] 
                    
            if band == 'ImageData8':
                bn = -1 + 8                
                # Query for gain specified in file metadata (by band)            
                if gain_08 == 'HGH':
                    ucc1 = ucc[bn, 0] 
                elif gain_08 == 'NOR':
                    ucc1 = ucc[bn, 1] 
                else:
                    ucc1 = ucc[bn, 2] 
                    
            if band == 'ImageData9':
                bn = -1 + 9                
                # Query for gain specified in file metadata (by band)            
                if gain_09 == 'HGH':
                    ucc1 = ucc[bn, 0] 
                elif gain_09 == 'NOR':
                    ucc1 = ucc[bn, 1] 
                else:
                    ucc1 = ucc[bn, 2] 
#------------------------------------------------------------------------------
            #Set irradiance value for specific band
            irradiance1 = irradiance[bn]
            
            # Convert from DN to Radiance        
            rad = dn2rad(sds)
            
            # Convert from Radiance to TOA Reflectance
            ref = rad2ref(rad)
         
            # Generate output Geotiff files
            # First, Radiance (stored as DN)
            driver = gdal.GetDriverByName('GTiff')
            dn = driver.Create(out_filename, nrow, ncol, 1, gdal.GDT_UInt16)
            
            # Define output GeoTiff CRS and extent properties
            srs = osr.SpatialReference()
            srs.ImportFromEPSG(utm_zone)
            dn.SetProjection(srs.ExportToWkt())
            dn.SetGeoTransform((ul_xx, x_res, 0., ul_yy, 0., y_res))
            
            # Write SDS array to output GeoTiff
            outband = dn.GetRasterBand(1)
            outband.WriteArray(sds)
            dn = None
            
            # Next, Radiance (w/m2/sr/µm)
            out_rad = driver.Create(out_filename_rad, nrow, ncol, 1, \
                                    gdal.GDT_Float32)
            
            # Define output GeoTiff CRS and extent properties
            out_rad.SetProjection(srs.ExportToWkt())
            out_rad.SetGeoTransform((ul_xx, x_res, 0., ul_yy, 0., y_res))
            
            # Write SDS array to output GeoTiff
            outband = out_rad.GetRasterBand(1)
            outband.WriteArray(rad)
            out_rad = None
            
            # Lastly, Reflectance (w/m2/sr/µm)
            out_ref = driver.Create(out_filename_ref, nrow, ncol, 1, \
                                    gdal.GDT_Float32)
            
            # Define output GeoTiff CRS and extent properties
            out_ref.SetProjection(srs.ExportToWkt())
            out_ref.SetGeoTransform((ul_xx, x_res, 0., ul_yy, 0., y_res))
            
            # Write SDS array to output GeoTiff
            outband = out_ref.GetRasterBand(1)
            outband.WriteArray(ref)
            out_ref = None
            
            del band, bn, gname, irradiance1, out_filename, \
            out_filename_rad, out_filename_ref, rad, ref, sds, ucc1
#------------------------------------------------------------------------------
# References
# ABRAMS, M., HOOK, S., and RAMACHANDRAN, B., 1999, Aster user handbook,
# Version 2, NASA/Jet Propulsion Laboratory, Pasadena, CA, at 
# https://asterweb.jpl.nasa.gov/content/03_data/04_Documents/
# aster_user_guide_v2.pdf

# ARCHARD, F., AND D’SOUZA, G., 1994, Collection and pre-processing of 
# NOAA-AVHRR 1km resolution data for tropical forest resource assessment. 
# Report EUR 16055, European Commission, Luxembourg, at 
# http://bookshop.europa.eu/en/collection-and-pre-processing-of-noaa-avhrr-1-km
# -resolution-data-for-tropical-forest-resource-assessment-pbCLNA16055/

# EVA, H., AND LAMBIN, E.F., 1998, Burnt area mapping in Central Africa using 
# ATSR data, International Journal of Remote Sensing, v. 19, no. 18, 3473-3497, 
# at http://dx.doi.org/10.1080/014311698213768

# Thome, K.J., Biggar, S.F., and Slater, P.N., 2001, Effects of assumed solar
# spectral irradiance on intercomparisons of earth-observing sensors. In 
# International Symposium on Remote Sensing, International Society for Optics
# and Photonics, pp. 260-269, at http://dx.doi.org/10.1117/12.450668.
#------------------------------------------------------------------------------