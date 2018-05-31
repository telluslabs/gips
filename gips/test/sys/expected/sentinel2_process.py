# TODO acolite products; should use --acolite flag
# acoflags    0 = water 1 = no data 2 = land
# fai         Floating Algae Index
# oc2chl      Blue-Green Ratio Chlorophyll Algorithm using bands 483 & 561
# oc3chl      Blue-Green Ratio Chlorophyll Algorithm using bands 443, 483, & 561
# rhow        Water-Leaving Radiance-Reflectance
# spm655      Suspended Sediment Concentration 655nm
# turbidity   Blended Turbidity

# all the index products are made by the same gippy call so given how
# slow sentinel2 is, skip most of them; it probably exercises the code
# well enough.  How to know if you're exercising the bands:
# https://github.com/gipit/gippy/blob/6d201870e55a7855814b3bdd3d30b05a889c24ed/GIP/GeoAlgorithms.cpp#L458
# for now we're doing these, which exercise 6 bands and both toa and surface:
#('evi-toa', # nir, red, blue, TOA version
#('crcm', # swir1, swir2, green, surface version


import collections

expectations = collections.OrderedDict([
 # regarding ref-toa, see:
 # ('aod/tiles/2017/183/MOD08_D3.A2017183.006.2017187184344.hdf',
 # https://gitlab.com/appliedgeosolutions/gips/issues/522

 # t_process[sentinel2-cfmask] recording:
 ('cfmask',
  [('sentinel2/tiles/19TCH/2017183/19TCH_2017183_S2A_cfmask.tif',
    'raster',
    'gdalinfo-stats',
    ['Driver: GTiff/GeoTIFF',
     'Size is 5490, 5490',
     'Coordinate System is:',
     'PROJCS["WGS 84 / UTM zone 19N",',
     '    GEOGCS["WGS 84",',
     '        DATUM["WGS_1984",',
     '            SPHEROID["WGS 84",6378137,298.25722356,',
     '                AUTHORITY["EPSG","7030"]],',
     '            AUTHORITY["EPSG","6326"]],',
     '        PRIMEM["Greenwich",0,',
     '            AUTHORITY["EPSG","8901"]],',
     '        UNIT["degree",0.01745329,',
     '            AUTHORITY["EPSG","9122"]],',
     '        AUTHORITY["EPSG","4326"]],',
     '    PROJECTION["Transverse_Mercator"],',
     '    PARAMETER["latitude_of_origin",0],',
     '    PARAMETER["central_meridian",-69],',
     '    PARAMETER["scale_factor",0.9996],',
     '    PARAMETER["false_easting",500000],',
     '    PARAMETER["false_northing",0],',
     '    UNIT["metre",1,',
     '        AUTHORITY["EPSG","9001"]],',
     '    AXIS["Easting",EAST],',
     '    AXIS["Northing",NORTH],',
     '    AUTHORITY["EPSG","32619"]]',
     'Origin = (300000.00000000,4800000.00000000)',
     'Pixel Size = (20.00000000,-20.00000000)',
     'Metadata:',
     '  AREA_OR_POINT=Area',
     '  FMASK_0=nodata',
     '  FMASK_1=valid',
     '  FMASK_2=cloud',
     '  FMASK_3=cloud shadow',
     '  FMASK_4=snow',
     '  FMASK_5=water',
     '  GIPS_Sentinel2_Version=0.1.1',
     '  GIPS_Source_Assets=S2A_MSIL1C_20170702T154421_N0205_R011_T19TCH_20170702T154703.zip',
     '  GIPS_Version=0.0.0-dev',
     'Image Structure Metadata:',
     '  INTERLEAVE=BAND',
     'Corner Coordinates:',
     'Upper Left  (  300000.000, 4800000.000) ( 71d28\' 0.42"W, 43d19\'34.49"N)',
     'Lower Left  (  300000.000, 4690200.000) ( 71d25\'40.01"W, 42d20\'18.10"N)',
     'Upper Right (  409800.000, 4800000.000) ( 70d 6\'46.52"W, 43d20\'50.79"N)',
     'Lower Right (  409800.000, 4690200.000) ( 70d 5\'43.11"W, 42d21\'31.82"N)',
     'Center      (  354900.000, 4745100.000) ( 70d46\'32.52"W, 42d50\'40.97"N)',
     'Band 1 Block=5490x1 Type=Byte, ColorInterp=Gray',
     '  Description = Layer_1',
     '  Min=1.000 Max=5.000 ',
     '  Minimum=1.000, Maximum=5.000, Mean=1.641, StdDev=0.814',
     '  NoData Value=0',
     '  Metadata:',
     '    LAYER_TYPE=thematic',
     '    STATISTICS_HISTOBINFUNCTION=direct',
     '    STATISTICS_HISTOBINVALUES=0|11916861|8046768|2468906|3776|410561|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|',
     '    STATISTICS_HISTOMAX=255',
     '    STATISTICS_HISTOMIN=0',
     '    STATISTICS_HISTONUMBINS=256',
     '    STATISTICS_MAXIMUM=5',
     '    STATISTICS_MEAN=1.64070705',
     '    STATISTICS_MEDIAN=1',
     '    STATISTICS_MINIMUM=1',
     '    STATISTICS_MODE=1',
     '    STATISTICS_SKIPFACTORX=1',
     '    STATISTICS_SKIPFACTORY=1',
     '    STATISTICS_STDDEV=0.81422416'])]),

 # t_process[sentinel2-crcm] recording:
 ('crcm',
  [('sentinel2/tiles/19TCH/2017183/19TCH_2017183_S2A_crcm.tif',
    'raster',
    'gdalinfo-stats',
    ['Driver: GTiff/GeoTIFF',
     'Size is 5490, 5490',
     'Coordinate System is:',
     'PROJCS["WGS 84 / UTM zone 19N",',
     '    GEOGCS["WGS 84",',
     '        DATUM["WGS_1984",',
     '            SPHEROID["WGS 84",6378137,298.25722356,',
     '                AUTHORITY["EPSG","7030"]],',
     '            AUTHORITY["EPSG","6326"]],',
     '        PRIMEM["Greenwich",0,',
     '            AUTHORITY["EPSG","8901"]],',
     '        UNIT["degree",0.01745329,',
     '            AUTHORITY["EPSG","9122"]],',
     '        AUTHORITY["EPSG","4326"]],',
     '    PROJECTION["Transverse_Mercator"],',
     '    PARAMETER["latitude_of_origin",0],',
     '    PARAMETER["central_meridian",-69],',
     '    PARAMETER["scale_factor",0.9996],',
     '    PARAMETER["false_easting",500000],',
     '    PARAMETER["false_northing",0],',
     '    UNIT["metre",1,',
     '        AUTHORITY["EPSG","9001"]],',
     '    AXIS["Easting",EAST],',
     '    AXIS["Northing",NORTH],',
     '    AUTHORITY["EPSG","32619"]]',
     'Origin = (300000.00000000,4800000.00000000)',
     'Pixel Size = (20.00000000,-20.00000000)',
     'Metadata:',
     '  AOD Source=MODIS (MOD08_D3)',
     '  AOD Value=0.065',
     '  AREA_OR_POINT=Area',
     '  GIPS_Sentinel2_Version=0.1.1',
     '  GIPS_Source_Assets=S2A_MSIL1C_20170702T154421_N0205_R011_T19TCH_20170702T154703.zip',
     '  GIPS_Version=0.0.0-dev',
     'Image Structure Metadata:',
     '  INTERLEAVE=BAND',
     'Corner Coordinates:',
     'Upper Left  (  300000.000, 4800000.000) ( 71d28\' 0.42"W, 43d19\'34.49"N)',
     'Lower Left  (  300000.000, 4690200.000) ( 71d25\'40.01"W, 42d20\'18.10"N)',
     'Upper Right (  409800.000, 4800000.000) ( 70d 6\'46.52"W, 43d20\'50.79"N)',
     'Lower Right (  409800.000, 4690200.000) ( 70d 5\'43.11"W, 42d21\'31.82"N)',
     'Center      (  354900.000, 4745100.000) ( 70d46\'32.52"W, 42d50\'40.97"N)',
     'Band 1 Block=5490x1 Type=Int16, ColorInterp=Gray',
     '  Description = crcm',
     '  Minimum=-8652.000, Maximum=32767.000, Mean=2377.147, StdDev=3342.997',
     '  NoData Value=-32768',
     '  Unit Type: other',
     '  Offset: 0,   Scale:0.0001',
     '  Metadata:',
     '    STATISTICS_MAXIMUM=32767',
     '    STATISTICS_MEAN=2377.14651595',
     '    STATISTICS_MINIMUM=-8652',
     '    STATISTICS_STDDEV=3342.99664128'])]),

 # t_process[sentinel2-evi-toa] recording:
 ('evi-toa',
  [('sentinel2/tiles/19TCH/2017183/19TCH_2017183_S2A_evi-toa.tif',
    'raster',
    'gdalinfo-stats',
    ['Driver: GTiff/GeoTIFF',
     'Size is 5490, 5490',
     'Coordinate System is:',
     'PROJCS["WGS 84 / UTM zone 19N",',
     '    GEOGCS["WGS 84",',
     '        DATUM["WGS_1984",',
     '            SPHEROID["WGS 84",6378137,298.25722356,',
     '                AUTHORITY["EPSG","7030"]],',
     '            AUTHORITY["EPSG","6326"]],',
     '        PRIMEM["Greenwich",0,',
     '            AUTHORITY["EPSG","8901"]],',
     '        UNIT["degree",0.01745329,',
     '            AUTHORITY["EPSG","9122"]],',
     '        AUTHORITY["EPSG","4326"]],',
     '    PROJECTION["Transverse_Mercator"],',
     '    PARAMETER["latitude_of_origin",0],',
     '    PARAMETER["central_meridian",-69],',
     '    PARAMETER["scale_factor",0.9996],',
     '    PARAMETER["false_easting",500000],',
     '    PARAMETER["false_northing",0],',
     '    UNIT["metre",1,',
     '        AUTHORITY["EPSG","9001"]],',
     '    AXIS["Easting",EAST],',
     '    AXIS["Northing",NORTH],',
     '    AUTHORITY["EPSG","32619"]]',
     'Origin = (300000.00000000,4800000.00000000)',
     'Pixel Size = (20.00000000,-20.00000000)',
     'Metadata:',
     '  AREA_OR_POINT=Area',
     '  GIPS_Sentinel2_Version=0.1.1',
     '  GIPS_Source_Assets=S2A_MSIL1C_20170702T154421_N0205_R011_T19TCH_20170702T154703.zip',
     '  GIPS_Version=0.0.0-dev',
     'Image Structure Metadata:',
     '  INTERLEAVE=BAND',
     'Corner Coordinates:',
     'Upper Left  (  300000.000, 4800000.000) ( 71d28\' 0.42"W, 43d19\'34.49"N)',
     'Lower Left  (  300000.000, 4690200.000) ( 71d25\'40.01"W, 42d20\'18.10"N)',
     'Upper Right (  409800.000, 4800000.000) ( 70d 6\'46.52"W, 43d20\'50.79"N)',
     'Lower Right (  409800.000, 4690200.000) ( 70d 5\'43.11"W, 42d21\'31.82"N)',
     'Center      (  354900.000, 4745100.000) ( 70d46\'32.52"W, 42d50\'40.97"N)',
     'Band 1 Block=5490x1 Type=Int16, ColorInterp=Gray',
     '  Description = evi',
     '  Minimum=-30779.000, Maximum=32767.000, Mean=4000.952, StdDev=3638.430',
     '  NoData Value=-32768',
     '  Unit Type: other',
     '  Offset: 0,   Scale:0.0001',
     '  Metadata:',
     '    STATISTICS_MAXIMUM=32767',
     '    STATISTICS_MEAN=4000.95244021',
     '    STATISTICS_MINIMUM=-30779',
     '    STATISTICS_STDDEV=3638.43034509'])]),

 # t_process[sentinel2-mtci] recording:
 ('mtci',
  [('sentinel2/tiles/19TCH/2017183/19TCH_2017183_S2A_mtci.tif',
    'raster',
    'gdalinfo-stats',
    ['Driver: GTiff/GeoTIFF',
     'Size is 5490, 5490',
     'Coordinate System is:',
     'PROJCS["WGS 84 / UTM zone 19N",',
     '    GEOGCS["WGS 84",',
     '        DATUM["WGS_1984",',
     '            SPHEROID["WGS 84",6378137,298.25722356,',
     '                AUTHORITY["EPSG","7030"]],',
     '            AUTHORITY["EPSG","6326"]],',
     '        PRIMEM["Greenwich",0,',
     '            AUTHORITY["EPSG","8901"]],',
     '        UNIT["degree",0.01745329,',
     '            AUTHORITY["EPSG","9122"]],',
     '        AUTHORITY["EPSG","4326"]],',
     '    PROJECTION["Transverse_Mercator"],',
     '    PARAMETER["latitude_of_origin",0],',
     '    PARAMETER["central_meridian",-69],',
     '    PARAMETER["scale_factor",0.9996],',
     '    PARAMETER["false_easting",500000],',
     '    PARAMETER["false_northing",0],',
     '    UNIT["metre",1,',
     '        AUTHORITY["EPSG","9001"]],',
     '    AXIS["Easting",EAST],',
     '    AXIS["Northing",NORTH],',
     '    AUTHORITY["EPSG","32619"]]',
     'Origin = (300000.00000000,4800000.00000000)',
     'Pixel Size = (20.00000000,-20.00000000)',
     'Metadata:',
     '  AREA_OR_POINT=Area',
     '  GIPS_Sentinel2_Version=0.1.1',
     '  GIPS_Source_Assets=S2A_MSIL1C_20170702T154421_N0205_R011_T19TCH_20170702T154703.zip',
     '  GIPS_Version=0.0.0-dev',
     'Image Structure Metadata:',
     '  INTERLEAVE=BAND',
     'Corner Coordinates:',
     'Upper Left  (  300000.000, 4800000.000) ( 71d28\' 0.42"W, 43d19\'34.49"N)',
     'Lower Left  (  300000.000, 4690200.000) ( 71d25\'40.01"W, 42d20\'18.10"N)',
     'Upper Right (  409800.000, 4800000.000) ( 70d 6\'46.52"W, 43d20\'50.79"N)',
     'Lower Right (  409800.000, 4690200.000) ( 70d 5\'43.11"W, 42d21\'31.82"N)',
     'Center      (  354900.000, 4745100.000) ( 70d46\'32.52"W, 42d50\'40.97"N)',
     'Band 1 Block=5490x1 Type=Int16, ColorInterp=Gray',
     '  Minimum=-30000.000, Maximum=29998.000, Mean=12389.005, StdDev=11309.426',
     '  NoData Value=-32768',
     '  Offset: 0,   Scale:0.0002',
     '  Metadata:',
     '    STATISTICS_MAXIMUM=29998',
     '    STATISTICS_MEAN=12389.00474024',
     '    STATISTICS_MINIMUM=-30000',
     '    STATISTICS_STDDEV=11309.42559945'])]),

 # t_process[sentinel2-mtci-toa] recording:
 ('mtci-toa',
  [('sentinel2/tiles/19TCH/2017183/19TCH_2017183_S2A_mtci-toa.tif',
    'raster',
    'gdalinfo-stats',
    ['Driver: GTiff/GeoTIFF',
     'Size is 5490, 5490',
     'Coordinate System is:',
     'PROJCS["WGS 84 / UTM zone 19N",',
     '    GEOGCS["WGS 84",',
     '        DATUM["WGS_1984",',
     '            SPHEROID["WGS 84",6378137,298.25722356,',
     '                AUTHORITY["EPSG","7030"]],',
     '            AUTHORITY["EPSG","6326"]],',
     '        PRIMEM["Greenwich",0,',
     '            AUTHORITY["EPSG","8901"]],',
     '        UNIT["degree",0.01745329,',
     '            AUTHORITY["EPSG","9122"]],',
     '        AUTHORITY["EPSG","4326"]],',
     '    PROJECTION["Transverse_Mercator"],',
     '    PARAMETER["latitude_of_origin",0],',
     '    PARAMETER["central_meridian",-69],',
     '    PARAMETER["scale_factor",0.9996],',
     '    PARAMETER["false_easting",500000],',
     '    PARAMETER["false_northing",0],',
     '    UNIT["metre",1,',
     '        AUTHORITY["EPSG","9001"]],',
     '    AXIS["Easting",EAST],',
     '    AXIS["Northing",NORTH],',
     '    AUTHORITY["EPSG","32619"]]',
     'Origin = (300000.00000000,4800000.00000000)',
     'Pixel Size = (20.00000000,-20.00000000)',
     'Metadata:',
     '  AREA_OR_POINT=Area',
     '  GIPS_Sentinel2_Version=0.1.1',
     '  GIPS_Source_Assets=S2A_MSIL1C_20170702T154421_N0205_R011_T19TCH_20170702T154703.zip',
     '  GIPS_Version=0.0.0-dev',
     'Image Structure Metadata:',
     '  INTERLEAVE=BAND',
     'Corner Coordinates:',
     'Upper Left  (  300000.000, 4800000.000) ( 71d28\' 0.42"W, 43d19\'34.49"N)',
     'Lower Left  (  300000.000, 4690200.000) ( 71d25\'40.01"W, 42d20\'18.10"N)',
     'Upper Right (  409800.000, 4800000.000) ( 70d 6\'46.52"W, 43d20\'50.79"N)',
     'Lower Right (  409800.000, 4690200.000) ( 70d 5\'43.11"W, 42d21\'31.82"N)',
     'Center      (  354900.000, 4745100.000) ( 70d46\'32.52"W, 42d50\'40.97"N)',
     'Band 1 Block=5490x1 Type=Int16, ColorInterp=Gray',
     '  Minimum=-7.000, Maximum=6.000, Mean=-0.635, StdDev=5.246',
     '  NoData Value=0',
     '  Metadata:',
     '    STATISTICS_MAXIMUM=6',
     '    STATISTICS_MEAN=-0.63534817',
     '    STATISTICS_MINIMUM=-7',
     '    STATISTICS_STDDEV=5.24645284'])]),

 # t_process[sentinel2-s2rep] recording:
 ('s2rep',
  [('sentinel2/tiles/19TCH/2017183/19TCH_2017183_S2A_s2rep.tif',
    'raster',
    'gdalinfo-stats',
    ['Driver: GTiff/GeoTIFF',
     'Size is 5490, 5490',
     'Coordinate System is:',
     'PROJCS["WGS 84 / UTM zone 19N",',
     '    GEOGCS["WGS 84",',
     '        DATUM["WGS_1984",',
     '            SPHEROID["WGS 84",6378137,298.25722356,',
     '                AUTHORITY["EPSG","7030"]],',
     '            AUTHORITY["EPSG","6326"]],',
     '        PRIMEM["Greenwich",0,',
     '            AUTHORITY["EPSG","8901"]],',
     '        UNIT["degree",0.01745329,',
     '            AUTHORITY["EPSG","9122"]],',
     '        AUTHORITY["EPSG","4326"]],',
     '    PROJECTION["Transverse_Mercator"],',
     '    PARAMETER["latitude_of_origin",0],',
     '    PARAMETER["central_meridian",-69],',
     '    PARAMETER["scale_factor",0.9996],',
     '    PARAMETER["false_easting",500000],',
     '    PARAMETER["false_northing",0],',
     '    UNIT["metre",1,',
     '        AUTHORITY["EPSG","9001"]],',
     '    AXIS["Easting",EAST],',
     '    AXIS["Northing",NORTH],',
     '    AUTHORITY["EPSG","32619"]]',
     'Origin = (300000.00000000,4800000.00000000)',
     'Pixel Size = (20.00000000,-20.00000000)',
     'Metadata:',
     '  AREA_OR_POINT=Area',
     '  GIPS_Sentinel2_Version=0.1.1',
     '  GIPS_Source_Assets=S2A_MSIL1C_20170702T154421_N0205_R011_T19TCH_20170702T154703.zip',
     '  GIPS_Version=0.0.0-dev',
     'Image Structure Metadata:',
     '  INTERLEAVE=BAND',
     'Corner Coordinates:',
     'Upper Left  (  300000.000, 4800000.000) ( 71d28\' 0.42"W, 43d19\'34.49"N)',
     'Lower Left  (  300000.000, 4690200.000) ( 71d25\'40.01"W, 42d20\'18.10"N)',
     'Upper Right (  409800.000, 4800000.000) ( 70d 6\'46.52"W, 43d20\'50.79"N)',
     'Lower Right (  409800.000, 4690200.000) ( 70d 5\'43.11"W, 42d21\'31.82"N)',
     'Center      (  354900.000, 4745100.000) ( 70d46\'32.52"W, 42d50\'40.97"N)',
     'Band 1 Block=5490x1 Type=Int16, ColorInterp=Gray',
     '  Minimum=-1.000, Maximum=17498.000, Mean=8163.092, StdDev=1365.082',
     '  NoData Value=-32768',
     '  Offset: 400,   Scale:0.04',
     '  Metadata:',
     '    STATISTICS_MAXIMUM=17498',
     '    STATISTICS_MEAN=8163.09175864',
     '    STATISTICS_MINIMUM=-1',
     '    STATISTICS_STDDEV=1365.08225823'])]),

    # t_process[sentinel2-cloudmask] recording:
 ('cloudmask',
  [('sentinel2/tiles/19TCH/2017183/19TCH_2017183_S2A_cloudmask.tif',
    'raster',
    'gdalinfo-stats',
    ['Driver: GTiff/GeoTIFF',
    'Size is 5490, 5490',
    'Coordinate System is:',
    'PROJCS["WGS 84 / UTM zone 19N",',
    '    GEOGCS["WGS 84",',
    '        DATUM["WGS_1984",',
    '            SPHEROID["WGS 84",6378137,298.25722356,',
    '                AUTHORITY["EPSG","7030"]],',
    '            AUTHORITY["EPSG","6326"]],',
    '        PRIMEM["Greenwich",0,',
    '            AUTHORITY["EPSG","8901"]],',
    '        UNIT["degree",0.01745329,',
    '            AUTHORITY["EPSG","9122"]],',
    '        AUTHORITY["EPSG","4326"]],',
    '    PROJECTION["Transverse_Mercator"],',
    '    PARAMETER["latitude_of_origin",0],',
    '    PARAMETER["central_meridian",-69],',
    '    PARAMETER["scale_factor",0.9996],',
    '    PARAMETER["false_easting",500000],',
    '    PARAMETER["false_northing",0],',
    '    UNIT["metre",1,',
    '        AUTHORITY["EPSG","9001"]],',
    '    AXIS["Easting",EAST],',
    '    AXIS["Northing",NORTH],',
    '    AUTHORITY["EPSG","32619"]]',
    'Origin = (300000.00000000,4800000.00000000)',
    'Pixel Size = (20.00000000,-20.00000000)',
    'Metadata:',
    '  AREA_OR_POINT=Area',
    '  GIPS_Sentinel2_Version=0.1.1',
    '  GIPS_Source_Assets=S2A_MSIL1C_20170702T154421_N0205_R011_T19TCH_20170702T154703.zip',
    '  GIPS_Version=0.0.0-dev',
    'Image Structure Metadata:',
    '  INTERLEAVE=BAND',
    'Corner Coordinates:',
    'Upper Left  (  300000.000, 4800000.000) ( 71d28\' 0.42"W, 43d19\'34.49"N)',
    'Lower Left  (  300000.000, 4690200.000) ( 71d25\'40.01"W, 42d20\'18.10"N)',
    'Upper Right (  409800.000, 4800000.000) ( 70d 6\'46.52"W, 43d20\'50.79"N)',
    'Lower Right (  409800.000, 4690200.000) ( 70d 5\'43.11"W, 42d21\'31.82"N)',
    'Center      (  354900.000, 4745100.000) ( 70d46\'32.52"W, 42d50\'40.97"N)',
    'Band 1 Block=5490x1 Type=Byte, ColorInterp=Gray',
    '  Minimum=1.000, Maximum=1.000, Mean=1.000, StdDev=0.000',
    '  NoData Value=0',
    '  Metadata:',
    '    STATISTICS_MAXIMUM=1',
    '    STATISTICS_MEAN=1',
    '    STATISTICS_MINIMUM=1',
    '    STATISTICS_STDDEV=0'])]),

 # t_process[sentinel2-s2rep-toa] recording:
 ('s2rep-toa',
  [('sentinel2/tiles/19TCH/2017183/19TCH_2017183_S2A_s2rep-toa.tif',
    'raster',
    'gdalinfo-stats',
    ['Driver: GTiff/GeoTIFF',
     'Size is 5490, 5490',
     'Coordinate System is:',
     'PROJCS["WGS 84 / UTM zone 19N",',
     '    GEOGCS["WGS 84",',
     '        DATUM["WGS_1984",',
     '            SPHEROID["WGS 84",6378137,298.25722356,',
     '                AUTHORITY["EPSG","7030"]],',
     '            AUTHORITY["EPSG","6326"]],',
     '        PRIMEM["Greenwich",0,',
     '            AUTHORITY["EPSG","8901"]],',
     '        UNIT["degree",0.01745329,',
     '            AUTHORITY["EPSG","9122"]],',
     '        AUTHORITY["EPSG","4326"]],',
     '    PROJECTION["Transverse_Mercator"],',
     '    PARAMETER["latitude_of_origin",0],',
     '    PARAMETER["central_meridian",-69],',
     '    PARAMETER["scale_factor",0.9996],',
     '    PARAMETER["false_easting",500000],',
     '    PARAMETER["false_northing",0],',
     '    UNIT["metre",1,',
     '        AUTHORITY["EPSG","9001"]],',
     '    AXIS["Easting",EAST],',
     '    AXIS["Northing",NORTH],',
     '    AUTHORITY["EPSG","32619"]]',
     'Origin = (300000.00000000,4800000.00000000)',
     'Pixel Size = (20.00000000,-20.00000000)',
     'Metadata:',
     '  AREA_OR_POINT=Area',
     '  GIPS_Sentinel2_Version=0.1.1',
     '  GIPS_Source_Assets=S2A_MSIL1C_20170702T154421_N0205_R011_T19TCH_20170702T154703.zip',
     '  GIPS_Version=0.0.0-dev',
     'Image Structure Metadata:',
     '  INTERLEAVE=BAND',
     'Corner Coordinates:',
     'Upper Left  (  300000.000, 4800000.000) ( 71d28\' 0.42"W, 43d19\'34.49"N)',
     'Lower Left  (  300000.000, 4690200.000) ( 71d25\'40.01"W, 42d20\'18.10"N)',
     'Upper Right (  409800.000, 4800000.000) ( 70d 6\'46.52"W, 43d20\'50.79"N)',
     'Lower Right (  409800.000, 4690200.000) ( 70d 5\'43.11"W, 42d21\'31.82"N)',
     'Center      (  354900.000, 4745100.000) ( 70d46\'32.52"W, 42d50\'40.97"N)',
     'Band 1 Block=5490x1 Type=Int16, ColorInterp=Gray',
     '  Minimum=-911.000, Maximum=1100.000, Mean=301.864, StdDev=724.321',
     '  NoData Value=0',
     '  Metadata:',
     '    STATISTICS_MAXIMUM=1100',
     '    STATISTICS_MEAN=301.86356505',
     '    STATISTICS_MINIMUM=-911',
     '    STATISTICS_STDDEV=724.32105270'])]),

])
