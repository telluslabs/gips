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

# Loop through all ASTER L1T hdf files in the directory
for k in range(len(file_list)):
    
    # Maintains original filename convention    
    file_name = file_list[k]    
    
    # Read in the file and metadata
    aster = gdal.Open(file_name)
    aster_sds = aster.GetSubDatasets()
    meta = aster.GetMetadata()
    
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
    # Loop through all ASTER L1T SDS (bands)    
    for i in range(len(aster_sds)):

        # Maintain original dataset name    
        gname = str(aster_sds[i])
        aster_sd = gname.split(',')[0]
        
        # Only process VNIR, SWIR, and TIR datasets        
        if len(aster_sd) > 80:        
            
            # Generate output name for tif            
            aster_sd2 = aster_sd.split('(')[1]
            aster_sd3 = aster_sd2[1:-1]
            band = aster_sd3.split(':')[-1]
            band_3N =  band.split('N')[0]           
            band_num = np.int(band_3N.split('ta')[-1])
            out_filename = out_dir + file_name.split('.hdf')[0] + '_' + band \
            + '.tif'
            
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
                
           # Open SDS and create array            
            band_ds = gdal.Open(aster_sd3, gdal.GA_ReadOnly)
            
            if band_num < 10:
                sds = band_ds.ReadAsArray().astype(np.byte)
    
                # Query raster dimensions and calculate raster x and y resolution            
                ncol, nrow = sds.shape            
                y_res = -1 * round((max(ul_y, lr_y)-min(ul_y, lr_y))/ncol)
                x_res = round((max(ul_x, lr_x)-min(ul_x, lr_x))/nrow)
            
                # Define UL x and y coordinates based on spatial resolution           
                ul_yy = ul_y - (y_res/2)
                ul_xx = ul_x - (x_res/2)                
                # Generate output Geotiff file
                driver = gdal.GetDriverByName('GTiff')
                ds = driver.Create(out_filename, nrow, ncol, 1, gdal.GDT_Byte)
          
            else:
                sds = band_ds.ReadAsArray().astype(np.uint16)
    
                # Query raster dimensions and calculate raster x and y resolution            
                ncol, nrow = sds.shape            
                y_res = -1 * round((max(ul_y, lr_y)-min(ul_y, lr_y))/ncol)
                x_res = round((max(ul_x, lr_x)-min(ul_x, lr_x))/nrow)
            
                # Define UL x and y coordinates based on spatial resolution           
                ul_yy = ul_y - (y_res/2)
                ul_xx = ul_x - (x_res/2)                    
                # Generate output Geotiff file
                driver = gdal.GetDriverByName('GTiff')
                ds = driver.Create(out_filename, nrow, ncol, 1, 
                                   gdal.GDT_UInt16)            
            # Define output GeoTiff CRS and extent properties
            srs = osr.SpatialReference()
            srs.ImportFromEPSG(utm_zone)
            ds.SetProjection(srs.ExportToWkt())
            ds.SetGeoTransform((ul_xx, x_res, 0., ul_yy, 0., y_res))
            
            # Write SDS array to output GeoTiff
            outband = ds.GetRasterBand(1)
            outband.WriteArray(sds)
            ds = None
            del aster_sd, aster_sd2, aster_sd3, band, band_3N, band_num, gname
###############################################################################





















