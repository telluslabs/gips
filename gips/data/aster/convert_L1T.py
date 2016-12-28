# -*- coding: utf-8 -*-

""" 
Based on code provided by NASA
See docstring in docs/ASTERL1T_DN2REF.py
"""

from osgeo import gdal, osr
import numpy as np
import os
import glob
from datetime import datetime
import re

from pdb import set_trace


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


def convert(file_path):
    
    # Read in the file and metadata
    aster = gdal.Open(file_path)
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

    # work around metadata bug
    meta_list = aster.GetMetadata_List()
    meta.update(dict([i.replace('=','.').split(',') for i in meta_list if i.startswith('GAIN')]))
    
    # Query gain data for each  band, needed for UCC     
    gain_01 = meta['GAIN.01'].strip()
    gain_02 = meta['GAIN.02'].strip()
    gain_03b = meta['GAIN.3B'].strip()
    gain_03n = meta['GAIN.3N'].strip()
    gain_04 = meta['GAIN.04'].strip()
    gain_05 = meta['GAIN.05'].strip()
    gain_06 = meta['GAIN.06'].strip()
    gain_07 = meta['GAIN.07'].strip()
    gain_08 = meta['GAIN.08'].strip()
    gain_09 = meta['GAIN.09'].strip()

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
        
        vnir = re.search("(VNIR.*)", aster_sd)
        swir = re.search("(SWIR.*)", aster_sd)
        if vnir or swir:
            # Generate output name for tif            
            aster_sd2 = aster_sd.split('(')[1]
            aster_sd3 = aster_sd2[1:-1]
            band = aster_sd3.split(':')[-1]

            out_dir, file_name = os.path.split(file_path)
            base_filename = file_name.split('.hdf')[0] + '_' + band + '.tif'
            out_filename = os.path.join(out_dir, base_filename)
            out_filename_rad = out_filename.split('.tif')[0] + '_rad.tif'
            out_filename_ref = out_filename.split('.tif')[0] + '_ref.tif'

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

            #Set irradiance value for specific band
            irradiance1 = irradiance[bn]
            
            # Convert from DN to Radiance        
            #rad = dn2rad(sds)
            rad = (sds-1.)*ucc1

            # Convert from Radiance to TOA Reflectance
            #ref = rad2ref(rad)
            ref = (np.pi * rad * (esd * esd)) / (irradiance1 * np.sin(np.pi * sza / 180.))

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


if __name__ == "__main__":

    file_path  = os.path.join('/data/aster/test/AST_L1T_00303172004174949_20150503164011_38074.hdf')
    convert(file_path)
