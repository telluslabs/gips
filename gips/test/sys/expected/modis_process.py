import collections

expectations = collections.OrderedDict([
 # t_process[modis-bi] recording:
 ('bi',
  [('modis/tiles/h12v04/2012337/h12v04_2012337_MCD_bi.tif',
    'raster',
    'gdalinfo-stats',
    ['Driver: GTiff/GeoTIFF',
     'Size is 2400, 2400',
     'Coordinate System is:',
     'PROJCS["unnamed",',
     '    GEOGCS["Unknown datum based upon the custom spheroid",',
     '        DATUM["Not_specified_based_on_custom_spheroid",',
     '            SPHEROID["Custom spheroid",6371007.181,0]],',
     '        PRIMEM["Greenwich",0],',
     '        UNIT["degree",0.01745329]],',
     '    PROJECTION["Sinusoidal"],',
     '    PARAMETER["longitude_of_center",0],',
     '    PARAMETER["false_easting",0],',
     '    PARAMETER["false_northing",0],',
     '    UNIT["metre",1,',
     '        AUTHORITY["EPSG","9001"]]]',
     'Origin = (-6671703.11799999,5559752.59833300)',
     'Pixel Size = (463.31271652,-463.31271652)',
     'Metadata:',
     '  add_offset=0',
     '  add_offset_err=0',
     '  ALBEDOFILEID=06121997',
     '  AREA_OR_POINT=Area',
     '  ASSOCIATEDINSTRUMENTSHORTNAME.1=MODIS',
     '  ASSOCIATEDINSTRUMENTSHORTNAME.2=MODIS',
     '  ASSOCIATEDPLATFORMSHORTNAME.1=Terra',
     '  ASSOCIATEDPLATFORMSHORTNAME.2=Aqua',
     '  ASSOCIATEDSENSORSHORTNAME.1=MODIS',
     '  ASSOCIATEDSENSORSHORTNAME.2=MODIS',
     '  AUTOMATICQUALITYFLAG.1=Passed',
     '  AUTOMATICQUALITYFLAGEXPLANATION.1=Passed was set as a default value. '
     'More algorithm will be developed',
     '  AVERAGENUMBEROBS=1',
     '  BRDFCODEID=AMBRALS_V4.0R1',
     '  BRDFDATABASEVERSION=v1.0500m',
     '  calibrated_nt=5',
     '  CHARACTERISTICBINANGULARSIZE=15.0',
     '  CHARACTERISTICBINSIZE=463.31271652',
     '  COVERAGECALCULATIONMETHOD=volume',
     '  DATACOLUMNS=2400',
     '  DATAROWS=2400',
     '  DAYNIGHTFLAG=Day',
     '  DESCRREVISION=6.1',
     '  EASTBOUNDINGCOORDINATE=-65.25948606',
     '  EXCLUSIONGRINGFLAG.1=N',
     '  GEOANYABNORMAL=False',
     '  GEOESTMAXRMSERROR=75.0',
     '  GIPS_Modis_Version=1.0.0',
     '  GIPS_Source_Assets=MCD43A4.A2012337.h12v04.006.20161120.hdf',
     '  GIPS_Version=0.0.0-dev',
     '  GLOBALGRIDCOLUMNS=86400',
     '  GLOBALGRIDROWS=43200',
     '  GRINGPOINTLATITUDE.1=39.78578782, 49.99719181, 50.07541801, 39.84112776',
     '  GRINGPOINTLONGITUDE.1=-78.20833299, -93.38216574, -77.75056839, '
     '-65.07807811',
     '  GRINGPOINTSEQUENCENO.1=1, 2, 3, 4',
     '  HDFEOSVersion=HDFEOS_V2.17',
     '  HORIZONTALTILENUMBER=12',
     '  identifier_product_doi=10.5067/MODIS/MCD43A4.006',
     '  identifier_product_doi_authority=http://dx.doi.org',
     '  INPUTPOINTER=MYD09GA.A2012329.h12v04.006.20152510.hdf, '
     'MYD09GA.A2012330.h12v04.006.20152511.hdf, '
     'MYD09GA.A2012331.h12v04.006.20152511.hdf, '
     'MYD09GA.A2012332.h12v04.006.20152511.hdf, '
     'MYD09GA.A2012333.h12v04.006.20152521.hdf, '
     'MYD09GA.A2012334.h12v04.006.20152521.hdf, '
     'MYD09GA.A2012335.h12v04.006.20152521.hdf, '
     'MYD09GA.A2012336.h12v04.006.20152522.hdf, '
     'MYD09GA.A2012337.h12v04.006.20152521.hdf, '
     'MYD09GA.A2012338.h12v04.006.20152511.hdf, '
     'MYD09GA.A2012339.h12v04.006.20152521.hdf, '
     'MYD09GA.A2012340.h12v04.006.20152521.hdf, '
     'MYD09GA.A2012341.h12v04.006.20152521.hdf, '
     'MYD09GA.A2012342.h12v04.006.20152522.hdf, '
     'MYD09GA.A2012343.h12v04.006.20152522.hdf, '
     'MYD09GA.A2012344.h12v04.006.20152522.hdf, '
     'MOD09GA.A2012329.h12v04.006.20152511.hdf, '
     'MOD09GA.A2012330.h12v04.006.20152510.hdf, '
     'MOD09GA.A2012331.h12v04.006.20152511.hdf, '
     'MOD09GA.A2012332.h12v04.006.20152512.hdf, '
     'MOD09GA.A2012333.h12v04.006.20152521.hdf, '
     'MOD09GA.A2012334.h12v04.006.20152522.hdf, '
     'MOD09GA.A2012335.h12v04.006.20152522.hdf, '
     'MOD09GA.A2012336.h12v04.006.20152522.hdf, '
     'MOD09GA.A2012337.h12v04.006.20152522.hdf, '
     'MOD09GA.A2012338.h12v04.006.20152511.hdf, '
     'MOD09GA.A2012339.h12v04.006.20152512.hdf, '
     'MOD09GA.A2012340.h12v04.006.20152522.hdf, '
     'MOD09GA.A2012341.h12v04.006.20152522.hdf, '
     'MOD09GA.A2012342.h12v04.006.20152522.hdf, '
     'MOD09GA.A2012343.h12v04.006.20152530.hdf, '
     'MOD09GA.A2012344.h12v04.006.20152530.hdf, MCD43DB.A2012336.6.h12v04.hdf',
     '  LOCALGRANULEID=MCD43A4.A2012337.h12v04.006.20161120.hdf',
     '  LOCALVERSIONID=6.1.34',
     '  LONGNAME=MODIS/Terra+Aqua BRDF/Albedo Nadir BRDF-Adjusted Ref Daily L3 '
     'Global - 500m',
     '  long_name=Nadir_Reflectance_Band1',
     '  MAXIMUMOBSERVATIONS=0',
     '  NADIRDATARESOLUTION=500m',
     '  NORTHBOUNDINGCOORDINATE=49.99999999',
     '  NUMBEROFGRANULES=1',
     '  PARAMETERNAME.1=NOT SET',
     '  PERCENTLANDINTILE=35',
     '  PERCENTNEWBRDFS=0',
     '  PERCENTPROCESSEDINTILE=41',
     '  PERCENTSHAPEFIXEDBRDFS=99',
     '  PERCENTSUBSTITUTEBRDFS=0',
     '  PGEVERSION=6.0.34',
     '  PROCESSINGCENTER=MODAPS',
     '  PROCESSINGENVIRONMENT=Linux minion5709 2.6.18-408.el5 #1 SMP Tue Jan 19 '
     '09:14:52 EST 2016 x86_64 x86_64 x86_64 GNU/Linux',
     '  PRODUCTIONDATETIME=2016-04-21T01:37:46.000Z',
     '  QAPERCENTGOODQUALITY=0',
     '  QAPERCENTNOTPRODUCEDCLOUD=36',
     '  QAPERCENTNOTPRODUCEDOTHER=25',
     '  QAPERCENTOTHERQUALITY=38',
     '  RANGEBEGINNINGDATE=2012-11-24',
     '  RANGEBEGINNINGTIME=00:00:00.000000',
     '  RANGEENDINGDATE=2012-12-10',
     '  RANGEENDINGTIME=23:59:59.999999',
     '  REPROCESSINGACTUAL=reprocessed',
     '  REPROCESSINGPLANNED=further update is anticipated',
     '  scale_factor=0.0001',
     '  scale_factor_err=0',
     '  SCIENCEQUALITYFLAG.1=Not Investigated',
     '  SCIENCEQUALITYFLAGEXPLANATION.1=See '
     'http://landweb.nascom/nasa.gov/cgi-bin/QA_WWW/qaFlagPage.cgi?sat=aqua the '
     'product Science Quality status.',
     '  SETUPFILEID=06121997',
     '  SHORTNAME=MCD43A4',
     '  SOUTHBOUNDINGCOORDINATE=39.99999999',
     '  SPSOPARAMETERS=2015',
     '  TileID=51012004',
     '  units=reflectance, no units',
     '  valid_range=0, 32767',
     '  VERSION=1.0',
     '  VERSIONID=6',
     '  VERTICALTILENUMBER=4',
     '  WESTBOUNDINGCOORDINATE=-93.34342959',
     '  _FillValue=32767',
     'Image Structure Metadata:',
     '  INTERLEAVE=BAND',
     'Corner Coordinates:',
     'Upper Left  (-6671703.118, 5559752.598) ( 93d20\'36.35"W, 50d 0\' 0.00"N)',
     'Lower Left  (-6671703.118, 4447802.079) ( 78d19\'27.97"W, 40d 0\' 0.00"N)',
     'Upper Right (-5559752.598, 5559752.598) ( 77d47\'10.29"W, 50d 0\' 0.00"N)',
     'Lower Right (-5559752.598, 4447802.079) ( 65d16\'13.31"W, 40d 0\' 0.00"N)',
     'Center      (-6115727.858, 5003777.339) ( 77d46\'54.29"W, 45d 0\' 0.00"N)',
     'Band 1 Block=2400x1 Type=Int16, ColorInterp=Gray',
     '  Description = bi',
     '  Minimum=0.000, Maximum=7876.000, Mean=1238.853, StdDev=852.915',
     '  NoData Value=-32768',
     '  Offset: 0,   Scale:0.0001',
     '  Metadata:',
     '    STATISTICS_MAXIMUM=7876',
     '    STATISTICS_MEAN=1238.85316778',
     '    STATISTICS_MINIMUM=0',
     '    STATISTICS_STDDEV=852.91483071',
     '    STATISTICS_VALID_PERCENT=39.34'])]),

 # t_process[modis-brgt] recording:
 ('brgt',
  [('modis/tiles/h12v04/2012337/h12v04_2012337_MCD_brgt.tif',
    'raster',
    'gdalinfo-stats',
    ['Driver: GTiff/GeoTIFF',
     'Size is 2400, 2400',
     'Coordinate System is:',
     'PROJCS["unnamed",',
     '    GEOGCS["Unknown datum based upon the custom spheroid",',
     '        DATUM["Not_specified_based_on_custom_spheroid",',
     '            SPHEROID["Custom spheroid",6371007.181,0]],',
     '        PRIMEM["Greenwich",0],',
     '        UNIT["degree",0.01745329]],',
     '    PROJECTION["Sinusoidal"],',
     '    PARAMETER["longitude_of_center",0],',
     '    PARAMETER["false_easting",0],',
     '    PARAMETER["false_northing",0],',
     '    UNIT["metre",1,',
     '        AUTHORITY["EPSG","9001"]]]',
     'Origin = (-6671703.11799999,5559752.59833300)',
     'Pixel Size = (463.31271652,-463.31271652)',
     'Metadata:',
     '  add_offset=0',
     '  add_offset_err=0',
     '  ALBEDOFILEID=06121997',
     '  AREA_OR_POINT=Area',
     '  ASSOCIATEDINSTRUMENTSHORTNAME.1=MODIS',
     '  ASSOCIATEDINSTRUMENTSHORTNAME.2=MODIS',
     '  ASSOCIATEDPLATFORMSHORTNAME.1=Terra',
     '  ASSOCIATEDPLATFORMSHORTNAME.2=Aqua',
     '  ASSOCIATEDSENSORSHORTNAME.1=MODIS',
     '  ASSOCIATEDSENSORSHORTNAME.2=MODIS',
     '  AUTOMATICQUALITYFLAG.1=Passed',
     '  AUTOMATICQUALITYFLAGEXPLANATION.1=Passed was set as a default value. '
     'More algorithm will be developed',
     '  AVERAGENUMBEROBS=1',
     '  BRDFCODEID=AMBRALS_V4.0R1',
     '  BRDFDATABASEVERSION=v1.0500m',
     '  calibrated_nt=5',
     '  CHARACTERISTICBINANGULARSIZE=15.0',
     '  CHARACTERISTICBINSIZE=463.31271652',
     '  COVERAGECALCULATIONMETHOD=volume',
     '  DATACOLUMNS=2400',
     '  DATAROWS=2400',
     '  DAYNIGHTFLAG=Day',
     '  DESCRREVISION=6.1',
     '  EASTBOUNDINGCOORDINATE=-65.25948606',
     '  EXCLUSIONGRINGFLAG.1=N',
     '  GEOANYABNORMAL=False',
     '  GEOESTMAXRMSERROR=75.0',
     '  GIPS_Modis_Version=1.0.0',
     '  GIPS_Source_Assets=MCD43A4.A2012337.h12v04.006.20161120.hdf',
     '  GIPS_Version=0.0.0-dev',
     '  GLOBALGRIDCOLUMNS=86400',
     '  GLOBALGRIDROWS=43200',
     '  GRINGPOINTLATITUDE.1=39.78578782, 49.99719181, 50.07541801, 39.84112776',
     '  GRINGPOINTLONGITUDE.1=-78.20833299, -93.38216574, -77.75056839, '
     '-65.07807811',
     '  GRINGPOINTSEQUENCENO.1=1, 2, 3, 4',
     '  HDFEOSVersion=HDFEOS_V2.17',
     '  HORIZONTALTILENUMBER=12',
     '  identifier_product_doi=10.5067/MODIS/MCD43A4.006',
     '  identifier_product_doi_authority=http://dx.doi.org',
     '  INPUTPOINTER=MYD09GA.A2012329.h12v04.006.20152510.hdf, '
     'MYD09GA.A2012330.h12v04.006.20152511.hdf, '
     'MYD09GA.A2012331.h12v04.006.20152511.hdf, '
     'MYD09GA.A2012332.h12v04.006.20152511.hdf, '
     'MYD09GA.A2012333.h12v04.006.20152521.hdf, '
     'MYD09GA.A2012334.h12v04.006.20152521.hdf, '
     'MYD09GA.A2012335.h12v04.006.20152521.hdf, '
     'MYD09GA.A2012336.h12v04.006.20152522.hdf, '
     'MYD09GA.A2012337.h12v04.006.20152521.hdf, '
     'MYD09GA.A2012338.h12v04.006.20152511.hdf, '
     'MYD09GA.A2012339.h12v04.006.20152521.hdf, '
     'MYD09GA.A2012340.h12v04.006.20152521.hdf, '
     'MYD09GA.A2012341.h12v04.006.20152521.hdf, '
     'MYD09GA.A2012342.h12v04.006.20152522.hdf, '
     'MYD09GA.A2012343.h12v04.006.20152522.hdf, '
     'MYD09GA.A2012344.h12v04.006.20152522.hdf, '
     'MOD09GA.A2012329.h12v04.006.20152511.hdf, '
     'MOD09GA.A2012330.h12v04.006.20152510.hdf, '
     'MOD09GA.A2012331.h12v04.006.20152511.hdf, '
     'MOD09GA.A2012332.h12v04.006.20152512.hdf, '
     'MOD09GA.A2012333.h12v04.006.20152521.hdf, '
     'MOD09GA.A2012334.h12v04.006.20152522.hdf, '
     'MOD09GA.A2012335.h12v04.006.20152522.hdf, '
     'MOD09GA.A2012336.h12v04.006.20152522.hdf, '
     'MOD09GA.A2012337.h12v04.006.20152522.hdf, '
     'MOD09GA.A2012338.h12v04.006.20152511.hdf, '
     'MOD09GA.A2012339.h12v04.006.20152512.hdf, '
     'MOD09GA.A2012340.h12v04.006.20152522.hdf, '
     'MOD09GA.A2012341.h12v04.006.20152522.hdf, '
     'MOD09GA.A2012342.h12v04.006.20152522.hdf, '
     'MOD09GA.A2012343.h12v04.006.20152530.hdf, '
     'MOD09GA.A2012344.h12v04.006.20152530.hdf, MCD43DB.A2012336.6.h12v04.hdf',
     '  LOCALGRANULEID=MCD43A4.A2012337.h12v04.006.20161120.hdf',
     '  LOCALVERSIONID=6.1.34',
     '  LONGNAME=MODIS/Terra+Aqua BRDF/Albedo Nadir BRDF-Adjusted Ref Daily L3 '
     'Global - 500m',
     '  long_name=Nadir_Reflectance_Band1',
     '  MAXIMUMOBSERVATIONS=0',
     '  NADIRDATARESOLUTION=500m',
     '  NORTHBOUNDINGCOORDINATE=49.99999999',
     '  NUMBEROFGRANULES=1',
     '  PARAMETERNAME.1=NOT SET',
     '  PERCENTLANDINTILE=35',
     '  PERCENTNEWBRDFS=0',
     '  PERCENTPROCESSEDINTILE=41',
     '  PERCENTSHAPEFIXEDBRDFS=99',
     '  PERCENTSUBSTITUTEBRDFS=0',
     '  PGEVERSION=6.0.34',
     '  PROCESSINGCENTER=MODAPS',
     '  PROCESSINGENVIRONMENT=Linux minion5709 2.6.18-408.el5 #1 SMP Tue Jan 19 '
     '09:14:52 EST 2016 x86_64 x86_64 x86_64 GNU/Linux',
     '  PRODUCTIONDATETIME=2016-04-21T01:37:46.000Z',
     '  QAPERCENTGOODQUALITY=0',
     '  QAPERCENTNOTPRODUCEDCLOUD=36',
     '  QAPERCENTNOTPRODUCEDOTHER=25',
     '  QAPERCENTOTHERQUALITY=38',
     '  RANGEBEGINNINGDATE=2012-11-24',
     '  RANGEBEGINNINGTIME=00:00:00.000000',
     '  RANGEENDINGDATE=2012-12-10',
     '  RANGEENDINGTIME=23:59:59.999999',
     '  REPROCESSINGACTUAL=reprocessed',
     '  REPROCESSINGPLANNED=further update is anticipated',
     '  scale_factor=0.0001',
     '  scale_factor_err=0',
     '  SCIENCEQUALITYFLAG.1=Not Investigated',
     '  SCIENCEQUALITYFLAGEXPLANATION.1=See '
     'http://landweb.nascom/nasa.gov/cgi-bin/QA_WWW/qaFlagPage.cgi?sat=aqua the '
     'product Science Quality status.',
     '  SETUPFILEID=06121997',
     '  SHORTNAME=MCD43A4',
     '  SOUTHBOUNDINGCOORDINATE=39.99999999',
     '  SPSOPARAMETERS=2015',
     '  TileID=51012004',
     '  units=reflectance, no units',
     '  valid_range=0, 32767',
     '  VERSION=1.0',
     '  VERSIONID=6',
     '  VERTICALTILENUMBER=4',
     '  WESTBOUNDINGCOORDINATE=-93.34342959',
     '  _FillValue=32767',
     'Image Structure Metadata:',
     '  INTERLEAVE=BAND',
     'Corner Coordinates:',
     'Upper Left  (-6671703.118, 5559752.598) ( 93d20\'36.35"W, 50d 0\' 0.00"N)',
     'Lower Left  (-6671703.118, 4447802.079) ( 78d19\'27.97"W, 40d 0\' 0.00"N)',
     'Upper Right (-5559752.598, 5559752.598) ( 77d47\'10.29"W, 50d 0\' 0.00"N)',
     'Lower Right (-5559752.598, 4447802.079) ( 65d16\'13.31"W, 40d 0\' 0.00"N)',
     'Center      (-6115727.858, 5003777.339) ( 77d46\'54.29"W, 45d 0\' 0.00"N)',
     'Band 1 Block=2400x1 Type=Int16, ColorInterp=Gray',
     '  Description = brgt',
     '  Minimum=1.000, Maximum=8012.000, Mean=884.508, StdDev=836.901',
     '  NoData Value=-32768',
     '  Offset: 0,   Scale:0.0001',
     '  Metadata:',
     '    STATISTICS_MAXIMUM=8012',
     '    STATISTICS_MEAN=884.50837310',
     '    STATISTICS_MINIMUM=1',
     '    STATISTICS_STDDEV=836.90107585',
     '    STATISTICS_VALID_PERCENT=39.25'])]),

 # t_process[modis-clouds] recording:
 ('clouds',
  [('modis/tiles/h12v04/2012337/h12v04_2012337_MOD_clouds.tif',
    'raster',
    'gdalinfo-stats',
    ['Driver: GTiff/GeoTIFF',
     'Size is 2400, 2400',
     'Coordinate System is:',
     'PROJCS["unnamed",',
     '    GEOGCS["Unknown datum based upon the custom spheroid",',
     '        DATUM["Not_specified_based_on_custom_spheroid",',
     '            SPHEROID["Custom spheroid",6371007.181,0]],',
     '        PRIMEM["Greenwich",0],',
     '        UNIT["degree",0.01745329]],',
     '    PROJECTION["Sinusoidal"],',
     '    PARAMETER["longitude_of_center",0],',
     '    PARAMETER["false_easting",0],',
     '    PARAMETER["false_northing",0],',
     '    UNIT["metre",1,',
     '        AUTHORITY["EPSG","9001"]]]',
     'Origin = (-6671703.11799999,5559752.59833300)',
     'Pixel Size = (463.31271652,-463.31271652)',
     'Metadata:',
     '  ALGORITHMPACKAGEACCEPTANCEDATE=12-2005',
     '  ALGORITHMPACKAGEMATURITYCODE=Normal',
     '  ALGORITHMPACKAGENAME=MOD_PR10A1',
     '  ALGORITHMPACKAGEVERSION=5',
     '  AREA_OR_POINT=Area',
     '  ASSOCIATEDINSTRUMENTSHORTNAME.1=MODIS',
     '  ASSOCIATEDPLATFORMSHORTNAME.1=Terra',
     '  ASSOCIATEDSENSORSHORTNAME.1=MODIS',
     '  AUTOMATICQUALITYFLAG.1=Passed',
     '  AUTOMATICQUALITYFLAG.2=Passed',
     '  AUTOMATICQUALITYFLAGEXPLANATION.1=No automatic quality assessment done '
     'in the PGE',
     '  AUTOMATICQUALITYFLAGEXPLANATION.2=No automatic quality assessment done '
     'in the PGE',
     '  AVAILABLE_ASSETS=MOD10A1',
     '  CHARACTERISTICBINANGULARSIZE=15.0',
     '  CHARACTERISTICBINSIZE=463.31271652',
     '  DATACOLUMNS=2400',
     '  DATAROWS=2400',
     '  DAYNIGHTFLAG=Day',
     '  DESCRREVISION=6.1',
     '  EASTBOUNDINGCOORDINATE=-65.25948606',
     '  EQUATORCROSSINGDATE.1=2012-12-02',
     '  EQUATORCROSSINGDATE.2=2012-12-02',
     '  EQUATORCROSSINGDATE.3=2012-12-02',
     '  EQUATORCROSSINGLONGITUDE.1=-67.61842541',
     '  EQUATORCROSSINGLONGITUDE.2=-92.34022247',
     '  EQUATORCROSSINGLONGITUDE.3=-117.06220722',
     '  EQUATORCROSSINGTIME.1=15:00:18.332032',
     '  EQUATORCROSSINGTIME.2=16:39:11.504411',
     '  EQUATORCROSSINGTIME.3=18:18:04.685793',
     '  EXCLUSIONGRINGFLAG.1=N',
     '  GEOANYABNORMAL=False',
     '  GEOESTMAXRMSERROR=50.0',
     '  GIPS_Modis_Version=1.0.0',
     '  GIPS_Source_Assets=MOD10A1.A2012337.h12v04.006.20161352.hdf',
     '  GIPS_Version=0.0.0-dev',
     '  GLOBALGRIDCOLUMNS=86400',
     '  GLOBALGRIDROWS=43200',
     '  GRANULEBEGINNINGDATETIMEARRAY=2012-12-02T14:45:00.000000Z, '
     '2012-12-02T16:20:00.000000Z, 2012-12-02T16:25:00.000000Z, '
     '2012-12-02T18:00:00.000000Z, 2012-12-02T18:05:00.000000Z',
     '  GRANULEDAYNIGHTFLAGARRAY=Day, Both, Day, Day, Day',
     '  GRANULEENDINGDATETIMEARRAY=2012-12-02T14:50:00.000000Z, '
     '2012-12-02T16:25:00.000000Z, 2012-12-02T16:30:00.000000Z, '
     '2012-12-02T18:05:00.000000Z, 2012-12-02T18:10:00.000000Z',
     '  GRANULENUMBERARRAY=179, 198, 199, 218, 219, -1, -1, -1, -1, -1, -1, -1, '
     '-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, '
     '-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, '
     '-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, '
     '-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, '
     '-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1',
     '  GRANULEPOINTERARRAY=0, -1, 1, 2, -1, -1, -1, -1, -1, -1, -1, -1, -1, '
     '-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, '
     '-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, '
     '-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, '
     '-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, '
     '-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1',
     '  GRINGPOINTLATITUDE.1=39.78578782, 49.99719181, 50.07541801, 39.84112776',
     '  GRINGPOINTLONGITUDE.1=-78.20833299, -93.38216574, -77.75056839, '
     '-65.07807811',
     '  GRINGPOINTSEQUENCENO.1=1, 2, 3, 4',
     '  HDFEOSVersion=HDFEOS_V2.17',
     '  HORIZONTALTILENUMBER=12',
     '  identifier_product_doi=10.5067/MODIS/MOD10A1.006',
     '  identifier_product_doi_authority=http://dx.doi.org',
     '  INPUTPOINTER=MOD10GA.A2012337.h12v04.006.20161320.hdf',
     '  INSTRUMENTNAME=Moderate Resolution Imaging Spectroradiometer',
     '  Key=0-100=NDSI snow, 200=missing data, 201=no decision, 211=night, '
     '237=inland water, 239=ocean, 250=cloud, 254=detector saturated, 255=fill',
     '  L2GCoverageCalculationMethod=volume',
     '  L2GFirstLayerSelectionCriteria=order of input pointer',
     '  L2GNumberOfOverlapGranules=3',
     '  LOCALGRANULEID=MOD10A1.A2012337.h12v04.006.20161352.hdf',
     '  LOCALINPUTGRANULEID=MOD10GA.A2012337.h12v04.006.20161320.hdf',
     '  LOCALVERSIONID=SCF V6.0.1',
     '  LONGNAME=MODIS/Terra Snow Cover Daily L3 Global 500m SIN Grid',
     '  long_name=NDSI snow cover from best observation of the day',
     '  missing_value=200',
     '  NADIRDATARESOLUTION=500m',
     '  NORTHBOUNDINGCOORDINATE=49.99999999',
     '  NUMBEROFINPUTGRANULES=5',
     '  NUMBEROFORBITS=3',
     '  NUMBEROFOVERLAPGRANULES=3',
     '  ORBITNUMBER.1=68928',
     '  ORBITNUMBER.2=68929',
     '  ORBITNUMBER.3=68930',
     '  ORBITNUMBERARRAY=68928, -1, 68929, 68930, -1, -1, -1, -1, -1, -1, -1, '
     '-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, '
     '-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, '
     '-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, '
     '-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, '
     '-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1',
     '  PARAMETERNAME.1=NDSI_Snow_Cover',
     '  PARAMETERNAME.2=Snow_Albedo_Daily_Tile',
     '  PGEVERSION=6.0.11',
     '  PLATFORMSHORTNAME=Terra',
     '  PROCESSINGCENTER=MODAPS',
     '  PROCESSINGDATETIME=2016-05-14T20:08:51.000Z',
     '  PROCESSINGENVIRONMENT=Linux minion5711 2.6.18-408.el5 #1 SMP Tue Jan 19 '
     '09:14:52 EST 2016 x86_64',
     '  PRODUCTIONDATETIME=2016-05-14T20:08:57.000Z',
     '  QAPERCENTCLOUDCOVER.1=98',
     '  QAPERCENTCLOUDCOVER.2=98',
     '  QAPERCENTGOODQUALITY=58',
     '  QAPERCENTMISSINGDATA.1=0',
     '  QAPERCENTMISSINGDATA.2=0',
     '  QAPERCENTOTHERQUALITY=42',
     '  RANGEBEGINNINGDATE=2012-12-02',
     '  RANGEBEGINNINGTIME=14:45:00.000000',
     '  RANGEENDINGDATE=2012-12-02',
     '  RANGEENDINGTIME=18:05:00.000000',
     '  REPROCESSINGACTUAL=reprocessed',
     '  REPROCESSINGPLANNED=further update is anticipated',
     '  SCIENCEQUALITYFLAG.1=Not Investigated',
     '  SCIENCEQUALITYFLAG.2=Not Investigated',
     '  SCIENCEQUALITYFLAGEXPLANATION.1=See '
     'http://landweb.nascom.nasa.gov/cgi-bin/QA_WWW/qaFlagPage.cgi?sat=terra '
     'for the product Science Quality status.',
     '  SCIENCEQUALITYFLAGEXPLANATION.2=See '
     'http://landweb.nascom.nasa.gov/cgi-bin/QA_WWW/qaFlagPage.cgi?sat=terra '
     'for the product Science Quality status.',
     '  SHORTNAME=MOD10A1',
     '  SNOWCOVERPERCENT=1',
     '  SOUTHBOUNDINGCOORDINATE=39.99999999',
     '  SPSOPARAMETERS=none',
     '  TileID=51012004',
     '  units=none',
     '  valid_range=0, 100',
     '  VERSION=1.0',
     '  VERSIONID=6',
     '  VERTICALTILENUMBER=4',
     '  WESTBOUNDINGCOORDINATE=-93.34342959',
     '  _FillValue=255',
     'Image Structure Metadata:',
     '  INTERLEAVE=BAND',
     'Corner Coordinates:',
     'Upper Left  (-6671703.118, 5559752.598) ( 93d20\'36.35"W, 50d 0\' 0.00"N)',
     'Lower Left  (-6671703.118, 4447802.079) ( 78d19\'27.97"W, 40d 0\' 0.00"N)',
     'Upper Right (-5559752.598, 5559752.598) ( 77d47\'10.29"W, 50d 0\' 0.00"N)',
     'Lower Right (-5559752.598, 4447802.079) ( 65d16\'13.31"W, 40d 0\' 0.00"N)',
     'Center      (-6115727.858, 5003777.339) ( 77d46\'54.29"W, 45d 0\' 0.00"N)',
     'Band 1 Block=2400x3 Type=Byte, ColorInterp=Gray',
     '  Description = Cloud Cover',
     '  Minimum=0.000, Maximum=1.000, Mean=0.859, StdDev=0.348',
     '  NoData Value=127',
     '  Metadata:',
     '    STATISTICS_MAXIMUM=1',
     '    STATISTICS_MEAN=0.85926757',
     '    STATISTICS_MINIMUM=0',
     '    STATISTICS_STDDEV=0.34774532',
     '    STATISTICS_VALID_PERCENT=99.999'])]),

 # t_process[modis-crc] recording:
 ('crc',
  [('modis/tiles/h12v04/2012337/h12v04_2012337_MCD_crc.tif',
    'raster',
    'gdalinfo-stats',
    ['Driver: GTiff/GeoTIFF',
     'Size is 2400, 2400',
     'Coordinate System is:',
     'PROJCS["unnamed",',
     '    GEOGCS["Unknown datum based upon the custom spheroid",',
     '        DATUM["Not_specified_based_on_custom_spheroid",',
     '            SPHEROID["Custom spheroid",6371007.181,0]],',
     '        PRIMEM["Greenwich",0],',
     '        UNIT["degree",0.01745329]],',
     '    PROJECTION["Sinusoidal"],',
     '    PARAMETER["longitude_of_center",0],',
     '    PARAMETER["false_easting",0],',
     '    PARAMETER["false_northing",0],',
     '    UNIT["metre",1,',
     '        AUTHORITY["EPSG","9001"]]]',
     'Origin = (-6671703.11799999,5559752.59833300)',
     'Pixel Size = (463.31271652,-463.31271652)',
     'Metadata:',
     '  add_offset=0',
     '  add_offset_err=0',
     '  ALBEDOFILEID=06121997',
     '  AREA_OR_POINT=Area',
     '  ASSOCIATEDINSTRUMENTSHORTNAME.1=MODIS',
     '  ASSOCIATEDINSTRUMENTSHORTNAME.2=MODIS',
     '  ASSOCIATEDPLATFORMSHORTNAME.1=Terra',
     '  ASSOCIATEDPLATFORMSHORTNAME.2=Aqua',
     '  ASSOCIATEDSENSORSHORTNAME.1=MODIS',
     '  ASSOCIATEDSENSORSHORTNAME.2=MODIS',
     '  AUTOMATICQUALITYFLAG.1=Passed',
     '  AUTOMATICQUALITYFLAGEXPLANATION.1=Passed was set as a default value. '
     'More algorithm will be developed',
     '  AVERAGENUMBEROBS=1',
     '  BRDFCODEID=AMBRALS_V4.0R1',
     '  BRDFDATABASEVERSION=v1.0500m',
     '  calibrated_nt=5',
     '  CHARACTERISTICBINANGULARSIZE=15.0',
     '  CHARACTERISTICBINSIZE=463.31271652',
     '  COVERAGECALCULATIONMETHOD=volume',
     '  DATACOLUMNS=2400',
     '  DATAROWS=2400',
     '  DAYNIGHTFLAG=Day',
     '  DESCRREVISION=6.1',
     '  EASTBOUNDINGCOORDINATE=-65.25948606',
     '  EXCLUSIONGRINGFLAG.1=N',
     '  GEOANYABNORMAL=False',
     '  GEOESTMAXRMSERROR=75.0',
     '  GIPS_Modis_Version=1.0.0',
     '  GIPS_Source_Assets=MCD43A4.A2012337.h12v04.006.20161120.hdf',
     '  GIPS_Version=0.0.0-dev',
     '  GLOBALGRIDCOLUMNS=86400',
     '  GLOBALGRIDROWS=43200',
     '  GRINGPOINTLATITUDE.1=39.78578782, 49.99719181, 50.07541801, 39.84112776',
     '  GRINGPOINTLONGITUDE.1=-78.20833299, -93.38216574, -77.75056839, '
     '-65.07807811',
     '  GRINGPOINTSEQUENCENO.1=1, 2, 3, 4',
     '  HDFEOSVersion=HDFEOS_V2.17',
     '  HORIZONTALTILENUMBER=12',
     '  identifier_product_doi=10.5067/MODIS/MCD43A4.006',
     '  identifier_product_doi_authority=http://dx.doi.org',
     '  INPUTPOINTER=MYD09GA.A2012329.h12v04.006.20152510.hdf, '
     'MYD09GA.A2012330.h12v04.006.20152511.hdf, '
     'MYD09GA.A2012331.h12v04.006.20152511.hdf, '
     'MYD09GA.A2012332.h12v04.006.20152511.hdf, '
     'MYD09GA.A2012333.h12v04.006.20152521.hdf, '
     'MYD09GA.A2012334.h12v04.006.20152521.hdf, '
     'MYD09GA.A2012335.h12v04.006.20152521.hdf, '
     'MYD09GA.A2012336.h12v04.006.20152522.hdf, '
     'MYD09GA.A2012337.h12v04.006.20152521.hdf, '
     'MYD09GA.A2012338.h12v04.006.20152511.hdf, '
     'MYD09GA.A2012339.h12v04.006.20152521.hdf, '
     'MYD09GA.A2012340.h12v04.006.20152521.hdf, '
     'MYD09GA.A2012341.h12v04.006.20152521.hdf, '
     'MYD09GA.A2012342.h12v04.006.20152522.hdf, '
     'MYD09GA.A2012343.h12v04.006.20152522.hdf, '
     'MYD09GA.A2012344.h12v04.006.20152522.hdf, '
     'MOD09GA.A2012329.h12v04.006.20152511.hdf, '
     'MOD09GA.A2012330.h12v04.006.20152510.hdf, '
     'MOD09GA.A2012331.h12v04.006.20152511.hdf, '
     'MOD09GA.A2012332.h12v04.006.20152512.hdf, '
     'MOD09GA.A2012333.h12v04.006.20152521.hdf, '
     'MOD09GA.A2012334.h12v04.006.20152522.hdf, '
     'MOD09GA.A2012335.h12v04.006.20152522.hdf, '
     'MOD09GA.A2012336.h12v04.006.20152522.hdf, '
     'MOD09GA.A2012337.h12v04.006.20152522.hdf, '
     'MOD09GA.A2012338.h12v04.006.20152511.hdf, '
     'MOD09GA.A2012339.h12v04.006.20152512.hdf, '
     'MOD09GA.A2012340.h12v04.006.20152522.hdf, '
     'MOD09GA.A2012341.h12v04.006.20152522.hdf, '
     'MOD09GA.A2012342.h12v04.006.20152522.hdf, '
     'MOD09GA.A2012343.h12v04.006.20152530.hdf, '
     'MOD09GA.A2012344.h12v04.006.20152530.hdf, MCD43DB.A2012336.6.h12v04.hdf',
     '  LOCALGRANULEID=MCD43A4.A2012337.h12v04.006.20161120.hdf',
     '  LOCALVERSIONID=6.1.34',
     '  LONGNAME=MODIS/Terra+Aqua BRDF/Albedo Nadir BRDF-Adjusted Ref Daily L3 '
     'Global - 500m',
     '  long_name=Nadir_Reflectance_Band1',
     '  MAXIMUMOBSERVATIONS=0',
     '  NADIRDATARESOLUTION=500m',
     '  NORTHBOUNDINGCOORDINATE=49.99999999',
     '  NUMBEROFGRANULES=1',
     '  PARAMETERNAME.1=NOT SET',
     '  PERCENTLANDINTILE=35',
     '  PERCENTNEWBRDFS=0',
     '  PERCENTPROCESSEDINTILE=41',
     '  PERCENTSHAPEFIXEDBRDFS=99',
     '  PERCENTSUBSTITUTEBRDFS=0',
     '  PGEVERSION=6.0.34',
     '  PROCESSINGCENTER=MODAPS',
     '  PROCESSINGENVIRONMENT=Linux minion5709 2.6.18-408.el5 #1 SMP Tue Jan 19 '
     '09:14:52 EST 2016 x86_64 x86_64 x86_64 GNU/Linux',
     '  PRODUCTIONDATETIME=2016-04-21T01:37:46.000Z',
     '  QAPERCENTGOODQUALITY=0',
     '  QAPERCENTNOTPRODUCEDCLOUD=36',
     '  QAPERCENTNOTPRODUCEDOTHER=25',
     '  QAPERCENTOTHERQUALITY=38',
     '  RANGEBEGINNINGDATE=2012-11-24',
     '  RANGEBEGINNINGTIME=00:00:00.000000',
     '  RANGEENDINGDATE=2012-12-10',
     '  RANGEENDINGTIME=23:59:59.999999',
     '  REPROCESSINGACTUAL=reprocessed',
     '  REPROCESSINGPLANNED=further update is anticipated',
     '  scale_factor=0.0001',
     '  scale_factor_err=0',
     '  SCIENCEQUALITYFLAG.1=Not Investigated',
     '  SCIENCEQUALITYFLAGEXPLANATION.1=See '
     'http://landweb.nascom/nasa.gov/cgi-bin/QA_WWW/qaFlagPage.cgi?sat=aqua the '
     'product Science Quality status.',
     '  SETUPFILEID=06121997',
     '  SHORTNAME=MCD43A4',
     '  SOUTHBOUNDINGCOORDINATE=39.99999999',
     '  SPSOPARAMETERS=2015',
     '  TileID=51012004',
     '  units=reflectance, no units',
     '  valid_range=0, 32767',
     '  VERSION=1.0',
     '  VERSIONID=6',
     '  VERTICALTILENUMBER=4',
     '  WESTBOUNDINGCOORDINATE=-93.34342959',
     '  _FillValue=32767',
     'Image Structure Metadata:',
     '  INTERLEAVE=BAND',
     'Corner Coordinates:',
     'Upper Left  (-6671703.118, 5559752.598) ( 93d20\'36.35"W, 50d 0\' 0.00"N)',
     'Lower Left  (-6671703.118, 4447802.079) ( 78d19\'27.97"W, 40d 0\' 0.00"N)',
     'Upper Right (-5559752.598, 5559752.598) ( 77d47\'10.29"W, 50d 0\' 0.00"N)',
     'Lower Right (-5559752.598, 4447802.079) ( 65d16\'13.31"W, 40d 0\' 0.00"N)',
     'Center      (-6115727.858, 5003777.339) ( 77d46\'54.29"W, 45d 0\' 0.00"N)',
     'Band 1 Block=2400x1 Type=Int16, ColorInterp=Gray',
     '  Description = crc',
     '  Minimum=-10000.000, Maximum=32767.000, Mean=4153.654, StdDev=8911.807',
     '  NoData Value=-32768',
     '  Offset: 0,   Scale:0.0001',
     '  Metadata:',
     '    STATISTICS_MAXIMUM=32767',
     '    STATISTICS_MEAN=4153.65379127',
     '    STATISTICS_MINIMUM=-10000',
     '    STATISTICS_STDDEV=8911.80745287',
     '    STATISTICS_VALID_PERCENT=31.16'])]),

 # t_process[modis-crcm] recording:
 ('crcm',
  [('modis/tiles/h12v04/2012337/h12v04_2012337_MCD_crcm.tif',
    'raster',
    'gdalinfo-stats',
    ['Driver: GTiff/GeoTIFF',
     'Size is 2400, 2400',
     'Coordinate System is:',
     'PROJCS["unnamed",',
     '    GEOGCS["Unknown datum based upon the custom spheroid",',
     '        DATUM["Not_specified_based_on_custom_spheroid",',
     '            SPHEROID["Custom spheroid",6371007.181,0]],',
     '        PRIMEM["Greenwich",0],',
     '        UNIT["degree",0.01745329]],',
     '    PROJECTION["Sinusoidal"],',
     '    PARAMETER["longitude_of_center",0],',
     '    PARAMETER["false_easting",0],',
     '    PARAMETER["false_northing",0],',
     '    UNIT["metre",1,',
     '        AUTHORITY["EPSG","9001"]]]',
     'Origin = (-6671703.11799999,5559752.59833300)',
     'Pixel Size = (463.31271652,-463.31271652)',
     'Metadata:',
     '  add_offset=0',
     '  add_offset_err=0',
     '  ALBEDOFILEID=06121997',
     '  AREA_OR_POINT=Area',
     '  ASSOCIATEDINSTRUMENTSHORTNAME.1=MODIS',
     '  ASSOCIATEDINSTRUMENTSHORTNAME.2=MODIS',
     '  ASSOCIATEDPLATFORMSHORTNAME.1=Terra',
     '  ASSOCIATEDPLATFORMSHORTNAME.2=Aqua',
     '  ASSOCIATEDSENSORSHORTNAME.1=MODIS',
     '  ASSOCIATEDSENSORSHORTNAME.2=MODIS',
     '  AUTOMATICQUALITYFLAG.1=Passed',
     '  AUTOMATICQUALITYFLAGEXPLANATION.1=Passed was set as a default value. '
     'More algorithm will be developed',
     '  AVERAGENUMBEROBS=1',
     '  BRDFCODEID=AMBRALS_V4.0R1',
     '  BRDFDATABASEVERSION=v1.0500m',
     '  calibrated_nt=5',
     '  CHARACTERISTICBINANGULARSIZE=15.0',
     '  CHARACTERISTICBINSIZE=463.31271652',
     '  COVERAGECALCULATIONMETHOD=volume',
     '  DATACOLUMNS=2400',
     '  DATAROWS=2400',
     '  DAYNIGHTFLAG=Day',
     '  DESCRREVISION=6.1',
     '  EASTBOUNDINGCOORDINATE=-65.25948606',
     '  EXCLUSIONGRINGFLAG.1=N',
     '  GEOANYABNORMAL=False',
     '  GEOESTMAXRMSERROR=75.0',
     '  GIPS_Modis_Version=1.0.0',
     '  GIPS_Source_Assets=MCD43A4.A2012337.h12v04.006.20161120.hdf',
     '  GIPS_Version=0.0.0-dev',
     '  GLOBALGRIDCOLUMNS=86400',
     '  GLOBALGRIDROWS=43200',
     '  GRINGPOINTLATITUDE.1=39.78578782, 49.99719181, 50.07541801, 39.84112776',
     '  GRINGPOINTLONGITUDE.1=-78.20833299, -93.38216574, -77.75056839, '
     '-65.07807811',
     '  GRINGPOINTSEQUENCENO.1=1, 2, 3, 4',
     '  HDFEOSVersion=HDFEOS_V2.17',
     '  HORIZONTALTILENUMBER=12',
     '  identifier_product_doi=10.5067/MODIS/MCD43A4.006',
     '  identifier_product_doi_authority=http://dx.doi.org',
     '  INPUTPOINTER=MYD09GA.A2012329.h12v04.006.20152510.hdf, '
     'MYD09GA.A2012330.h12v04.006.20152511.hdf, '
     'MYD09GA.A2012331.h12v04.006.20152511.hdf, '
     'MYD09GA.A2012332.h12v04.006.20152511.hdf, '
     'MYD09GA.A2012333.h12v04.006.20152521.hdf, '
     'MYD09GA.A2012334.h12v04.006.20152521.hdf, '
     'MYD09GA.A2012335.h12v04.006.20152521.hdf, '
     'MYD09GA.A2012336.h12v04.006.20152522.hdf, '
     'MYD09GA.A2012337.h12v04.006.20152521.hdf, '
     'MYD09GA.A2012338.h12v04.006.20152511.hdf, '
     'MYD09GA.A2012339.h12v04.006.20152521.hdf, '
     'MYD09GA.A2012340.h12v04.006.20152521.hdf, '
     'MYD09GA.A2012341.h12v04.006.20152521.hdf, '
     'MYD09GA.A2012342.h12v04.006.20152522.hdf, '
     'MYD09GA.A2012343.h12v04.006.20152522.hdf, '
     'MYD09GA.A2012344.h12v04.006.20152522.hdf, '
     'MOD09GA.A2012329.h12v04.006.20152511.hdf, '
     'MOD09GA.A2012330.h12v04.006.20152510.hdf, '
     'MOD09GA.A2012331.h12v04.006.20152511.hdf, '
     'MOD09GA.A2012332.h12v04.006.20152512.hdf, '
     'MOD09GA.A2012333.h12v04.006.20152521.hdf, '
     'MOD09GA.A2012334.h12v04.006.20152522.hdf, '
     'MOD09GA.A2012335.h12v04.006.20152522.hdf, '
     'MOD09GA.A2012336.h12v04.006.20152522.hdf, '
     'MOD09GA.A2012337.h12v04.006.20152522.hdf, '
     'MOD09GA.A2012338.h12v04.006.20152511.hdf, '
     'MOD09GA.A2012339.h12v04.006.20152512.hdf, '
     'MOD09GA.A2012340.h12v04.006.20152522.hdf, '
     'MOD09GA.A2012341.h12v04.006.20152522.hdf, '
     'MOD09GA.A2012342.h12v04.006.20152522.hdf, '
     'MOD09GA.A2012343.h12v04.006.20152530.hdf, '
     'MOD09GA.A2012344.h12v04.006.20152530.hdf, MCD43DB.A2012336.6.h12v04.hdf',
     '  LOCALGRANULEID=MCD43A4.A2012337.h12v04.006.20161120.hdf',
     '  LOCALVERSIONID=6.1.34',
     '  LONGNAME=MODIS/Terra+Aqua BRDF/Albedo Nadir BRDF-Adjusted Ref Daily L3 '
     'Global - 500m',
     '  long_name=Nadir_Reflectance_Band1',
     '  MAXIMUMOBSERVATIONS=0',
     '  NADIRDATARESOLUTION=500m',
     '  NORTHBOUNDINGCOORDINATE=49.99999999',
     '  NUMBEROFGRANULES=1',
     '  PARAMETERNAME.1=NOT SET',
     '  PERCENTLANDINTILE=35',
     '  PERCENTNEWBRDFS=0',
     '  PERCENTPROCESSEDINTILE=41',
     '  PERCENTSHAPEFIXEDBRDFS=99',
     '  PERCENTSUBSTITUTEBRDFS=0',
     '  PGEVERSION=6.0.34',
     '  PROCESSINGCENTER=MODAPS',
     '  PROCESSINGENVIRONMENT=Linux minion5709 2.6.18-408.el5 #1 SMP Tue Jan 19 '
     '09:14:52 EST 2016 x86_64 x86_64 x86_64 GNU/Linux',
     '  PRODUCTIONDATETIME=2016-04-21T01:37:46.000Z',
     '  QAPERCENTGOODQUALITY=0',
     '  QAPERCENTNOTPRODUCEDCLOUD=36',
     '  QAPERCENTNOTPRODUCEDOTHER=25',
     '  QAPERCENTOTHERQUALITY=38',
     '  RANGEBEGINNINGDATE=2012-11-24',
     '  RANGEBEGINNINGTIME=00:00:00.000000',
     '  RANGEENDINGDATE=2012-12-10',
     '  RANGEENDINGTIME=23:59:59.999999',
     '  REPROCESSINGACTUAL=reprocessed',
     '  REPROCESSINGPLANNED=further update is anticipated',
     '  scale_factor=0.0001',
     '  scale_factor_err=0',
     '  SCIENCEQUALITYFLAG.1=Not Investigated',
     '  SCIENCEQUALITYFLAGEXPLANATION.1=See '
     'http://landweb.nascom/nasa.gov/cgi-bin/QA_WWW/qaFlagPage.cgi?sat=aqua the '
     'product Science Quality status.',
     '  SETUPFILEID=06121997',
     '  SHORTNAME=MCD43A4',
     '  SOUTHBOUNDINGCOORDINATE=39.99999999',
     '  SPSOPARAMETERS=2015',
     '  TileID=51012004',
     '  units=reflectance, no units',
     '  valid_range=0, 32767',
     '  VERSION=1.0',
     '  VERSIONID=6',
     '  VERTICALTILENUMBER=4',
     '  WESTBOUNDINGCOORDINATE=-93.34342959',
     '  _FillValue=32767',
     'Image Structure Metadata:',
     '  INTERLEAVE=BAND',
     'Corner Coordinates:',
     'Upper Left  (-6671703.118, 5559752.598) ( 93d20\'36.35"W, 50d 0\' 0.00"N)',
     'Lower Left  (-6671703.118, 4447802.079) ( 78d19\'27.97"W, 40d 0\' 0.00"N)',
     'Upper Right (-5559752.598, 5559752.598) ( 77d47\'10.29"W, 50d 0\' 0.00"N)',
     'Lower Right (-5559752.598, 4447802.079) ( 65d16\'13.31"W, 40d 0\' 0.00"N)',
     'Center      (-6115727.858, 5003777.339) ( 77d46\'54.29"W, 45d 0\' 0.00"N)',
     'Band 1 Block=2400x1 Type=Int16, ColorInterp=Gray',
     '  Description = crcm',
     '  Minimum=-10000.000, Maximum=32767.000, Mean=2690.752, StdDev=7364.116',
     '  NoData Value=-32768',
     '  Offset: 0,   Scale:0.0001',
     '  Metadata:',
     '    STATISTICS_MAXIMUM=32767',
     '    STATISTICS_MEAN=2690.75153974',
     '    STATISTICS_MINIMUM=-10000',
     '    STATISTICS_STDDEV=7364.11580436',
     '    STATISTICS_VALID_PERCENT=31.28'])]),

 # t_process[modis-evi] recording:
 ('evi',
  [('modis/tiles/h12v04/2012337/h12v04_2012337_MCD_evi.tif',
    'raster',
    'gdalinfo-stats',
    ['Driver: GTiff/GeoTIFF',
     'Size is 2400, 2400',
     'Coordinate System is:',
     'PROJCS["unnamed",',
     '    GEOGCS["Unknown datum based upon the custom spheroid",',
     '        DATUM["Not_specified_based_on_custom_spheroid",',
     '            SPHEROID["Custom spheroid",6371007.181,0]],',
     '        PRIMEM["Greenwich",0],',
     '        UNIT["degree",0.01745329]],',
     '    PROJECTION["Sinusoidal"],',
     '    PARAMETER["longitude_of_center",0],',
     '    PARAMETER["false_easting",0],',
     '    PARAMETER["false_northing",0],',
     '    UNIT["metre",1,',
     '        AUTHORITY["EPSG","9001"]]]',
     'Origin = (-6671703.11799999,5559752.59833300)',
     'Pixel Size = (463.31271652,-463.31271652)',
     'Metadata:',
     '  add_offset=0',
     '  add_offset_err=0',
     '  ALBEDOFILEID=06121997',
     '  AREA_OR_POINT=Area',
     '  ASSOCIATEDINSTRUMENTSHORTNAME.1=MODIS',
     '  ASSOCIATEDINSTRUMENTSHORTNAME.2=MODIS',
     '  ASSOCIATEDPLATFORMSHORTNAME.1=Terra',
     '  ASSOCIATEDPLATFORMSHORTNAME.2=Aqua',
     '  ASSOCIATEDSENSORSHORTNAME.1=MODIS',
     '  ASSOCIATEDSENSORSHORTNAME.2=MODIS',
     '  AUTOMATICQUALITYFLAG.1=Passed',
     '  AUTOMATICQUALITYFLAGEXPLANATION.1=Passed was set as a default value. '
     'More algorithm will be developed',
     '  AVERAGENUMBEROBS=1',
     '  BRDFCODEID=AMBRALS_V4.0R1',
     '  BRDFDATABASEVERSION=v1.0500m',
     '  calibrated_nt=5',
     '  CHARACTERISTICBINANGULARSIZE=15.0',
     '  CHARACTERISTICBINSIZE=463.31271652',
     '  COVERAGECALCULATIONMETHOD=volume',
     '  DATACOLUMNS=2400',
     '  DATAROWS=2400',
     '  DAYNIGHTFLAG=Day',
     '  DESCRREVISION=6.1',
     '  EASTBOUNDINGCOORDINATE=-65.25948606',
     '  EXCLUSIONGRINGFLAG.1=N',
     '  GEOANYABNORMAL=False',
     '  GEOESTMAXRMSERROR=75.0',
     '  GIPS_Modis_Version=1.0.0',
     '  GIPS_Source_Assets=MCD43A4.A2012337.h12v04.006.20161120.hdf',
     '  GIPS_Version=0.0.0-dev',
     '  GLOBALGRIDCOLUMNS=86400',
     '  GLOBALGRIDROWS=43200',
     '  GRINGPOINTLATITUDE.1=39.78578782, 49.99719181, 50.07541801, 39.84112776',
     '  GRINGPOINTLONGITUDE.1=-78.20833299, -93.38216574, -77.75056839, '
     '-65.07807811',
     '  GRINGPOINTSEQUENCENO.1=1, 2, 3, 4',
     '  HDFEOSVersion=HDFEOS_V2.17',
     '  HORIZONTALTILENUMBER=12',
     '  identifier_product_doi=10.5067/MODIS/MCD43A4.006',
     '  identifier_product_doi_authority=http://dx.doi.org',
     '  INPUTPOINTER=MYD09GA.A2012329.h12v04.006.20152510.hdf, '
     'MYD09GA.A2012330.h12v04.006.20152511.hdf, '
     'MYD09GA.A2012331.h12v04.006.20152511.hdf, '
     'MYD09GA.A2012332.h12v04.006.20152511.hdf, '
     'MYD09GA.A2012333.h12v04.006.20152521.hdf, '
     'MYD09GA.A2012334.h12v04.006.20152521.hdf, '
     'MYD09GA.A2012335.h12v04.006.20152521.hdf, '
     'MYD09GA.A2012336.h12v04.006.20152522.hdf, '
     'MYD09GA.A2012337.h12v04.006.20152521.hdf, '
     'MYD09GA.A2012338.h12v04.006.20152511.hdf, '
     'MYD09GA.A2012339.h12v04.006.20152521.hdf, '
     'MYD09GA.A2012340.h12v04.006.20152521.hdf, '
     'MYD09GA.A2012341.h12v04.006.20152521.hdf, '
     'MYD09GA.A2012342.h12v04.006.20152522.hdf, '
     'MYD09GA.A2012343.h12v04.006.20152522.hdf, '
     'MYD09GA.A2012344.h12v04.006.20152522.hdf, '
     'MOD09GA.A2012329.h12v04.006.20152511.hdf, '
     'MOD09GA.A2012330.h12v04.006.20152510.hdf, '
     'MOD09GA.A2012331.h12v04.006.20152511.hdf, '
     'MOD09GA.A2012332.h12v04.006.20152512.hdf, '
     'MOD09GA.A2012333.h12v04.006.20152521.hdf, '
     'MOD09GA.A2012334.h12v04.006.20152522.hdf, '
     'MOD09GA.A2012335.h12v04.006.20152522.hdf, '
     'MOD09GA.A2012336.h12v04.006.20152522.hdf, '
     'MOD09GA.A2012337.h12v04.006.20152522.hdf, '
     'MOD09GA.A2012338.h12v04.006.20152511.hdf, '
     'MOD09GA.A2012339.h12v04.006.20152512.hdf, '
     'MOD09GA.A2012340.h12v04.006.20152522.hdf, '
     'MOD09GA.A2012341.h12v04.006.20152522.hdf, '
     'MOD09GA.A2012342.h12v04.006.20152522.hdf, '
     'MOD09GA.A2012343.h12v04.006.20152530.hdf, '
     'MOD09GA.A2012344.h12v04.006.20152530.hdf, MCD43DB.A2012336.6.h12v04.hdf',
     '  LOCALGRANULEID=MCD43A4.A2012337.h12v04.006.20161120.hdf',
     '  LOCALVERSIONID=6.1.34',
     '  LONGNAME=MODIS/Terra+Aqua BRDF/Albedo Nadir BRDF-Adjusted Ref Daily L3 '
     'Global - 500m',
     '  long_name=Nadir_Reflectance_Band1',
     '  MAXIMUMOBSERVATIONS=0',
     '  NADIRDATARESOLUTION=500m',
     '  NORTHBOUNDINGCOORDINATE=49.99999999',
     '  NUMBEROFGRANULES=1',
     '  PARAMETERNAME.1=NOT SET',
     '  PERCENTLANDINTILE=35',
     '  PERCENTNEWBRDFS=0',
     '  PERCENTPROCESSEDINTILE=41',
     '  PERCENTSHAPEFIXEDBRDFS=99',
     '  PERCENTSUBSTITUTEBRDFS=0',
     '  PGEVERSION=6.0.34',
     '  PROCESSINGCENTER=MODAPS',
     '  PROCESSINGENVIRONMENT=Linux minion5709 2.6.18-408.el5 #1 SMP Tue Jan 19 '
     '09:14:52 EST 2016 x86_64 x86_64 x86_64 GNU/Linux',
     '  PRODUCTIONDATETIME=2016-04-21T01:37:46.000Z',
     '  QAPERCENTGOODQUALITY=0',
     '  QAPERCENTNOTPRODUCEDCLOUD=36',
     '  QAPERCENTNOTPRODUCEDOTHER=25',
     '  QAPERCENTOTHERQUALITY=38',
     '  RANGEBEGINNINGDATE=2012-11-24',
     '  RANGEBEGINNINGTIME=00:00:00.000000',
     '  RANGEENDINGDATE=2012-12-10',
     '  RANGEENDINGTIME=23:59:59.999999',
     '  REPROCESSINGACTUAL=reprocessed',
     '  REPROCESSINGPLANNED=further update is anticipated',
     '  scale_factor=0.0001',
     '  scale_factor_err=0',
     '  SCIENCEQUALITYFLAG.1=Not Investigated',
     '  SCIENCEQUALITYFLAGEXPLANATION.1=See '
     'http://landweb.nascom/nasa.gov/cgi-bin/QA_WWW/qaFlagPage.cgi?sat=aqua the '
     'product Science Quality status.',
     '  SETUPFILEID=06121997',
     '  SHORTNAME=MCD43A4',
     '  SOUTHBOUNDINGCOORDINATE=39.99999999',
     '  SPSOPARAMETERS=2015',
     '  TileID=51012004',
     '  units=reflectance, no units',
     '  valid_range=0, 32767',
     '  VERSION=1.0',
     '  VERSIONID=6',
     '  VERTICALTILENUMBER=4',
     '  WESTBOUNDINGCOORDINATE=-93.34342959',
     '  _FillValue=32767',
     'Image Structure Metadata:',
     '  INTERLEAVE=BAND',
     'Corner Coordinates:',
     'Upper Left  (-6671703.118, 5559752.598) ( 93d20\'36.35"W, 50d 0\' 0.00"N)',
     'Lower Left  (-6671703.118, 4447802.079) ( 78d19\'27.97"W, 40d 0\' 0.00"N)',
     'Upper Right (-5559752.598, 5559752.598) ( 77d47\'10.29"W, 50d 0\' 0.00"N)',
     'Lower Right (-5559752.598, 4447802.079) ( 65d16\'13.31"W, 40d 0\' 0.00"N)',
     'Center      (-6115727.858, 5003777.339) ( 77d46\'54.29"W, 45d 0\' 0.00"N)',
     'Band 1 Block=2400x1 Type=Int16, ColorInterp=Gray',
     '  Description = evi',
     '  Minimum=-32636.000, Maximum=32767.000, Mean=1999.675, StdDev=1237.395',
     '  NoData Value=-32768',
     '  Offset: 0,   Scale:0.0001',
     '  Metadata:',
     '    STATISTICS_MAXIMUM=32767',
     '    STATISTICS_MEAN=1999.67520635',
     '    STATISTICS_MINIMUM=-32636',
     '    STATISTICS_STDDEV=1237.39504694',
     '    STATISTICS_VALID_PERCENT=39.27'])]),

 # t_process[modis-isti] recording:
 ('isti',
  [('modis/tiles/h12v04/2012337/h12v04_2012337_MCD_isti.tif',
    'raster',
    'gdalinfo-stats',
    ['Driver: GTiff/GeoTIFF',
     'Size is 2400, 2400',
     'Coordinate System is:',
     'PROJCS["unnamed",',
     '    GEOGCS["Unknown datum based upon the custom spheroid",',
     '        DATUM["Not_specified_based_on_custom_spheroid",',
     '            SPHEROID["Custom spheroid",6371007.181,0]],',
     '        PRIMEM["Greenwich",0],',
     '        UNIT["degree",0.01745329]],',
     '    PROJECTION["Sinusoidal"],',
     '    PARAMETER["longitude_of_center",0],',
     '    PARAMETER["false_easting",0],',
     '    PARAMETER["false_northing",0],',
     '    UNIT["metre",1,',
     '        AUTHORITY["EPSG","9001"]]]',
     'Origin = (-6671703.11799999,5559752.59833300)',
     'Pixel Size = (463.31271652,-463.31271652)',
     'Metadata:',
     '  add_offset=0',
     '  add_offset_err=0',
     '  ALBEDOFILEID=06121997',
     '  AREA_OR_POINT=Area',
     '  ASSOCIATEDINSTRUMENTSHORTNAME.1=MODIS',
     '  ASSOCIATEDINSTRUMENTSHORTNAME.2=MODIS',
     '  ASSOCIATEDPLATFORMSHORTNAME.1=Terra',
     '  ASSOCIATEDPLATFORMSHORTNAME.2=Aqua',
     '  ASSOCIATEDSENSORSHORTNAME.1=MODIS',
     '  ASSOCIATEDSENSORSHORTNAME.2=MODIS',
     '  AUTOMATICQUALITYFLAG.1=Passed',
     '  AUTOMATICQUALITYFLAGEXPLANATION.1=Passed was set as a default value. '
     'More algorithm will be developed',
     '  AVERAGENUMBEROBS=1',
     '  BRDFCODEID=AMBRALS_V4.0R1',
     '  BRDFDATABASEVERSION=v1.0500m',
     '  calibrated_nt=5',
     '  CHARACTERISTICBINANGULARSIZE=15.0',
     '  CHARACTERISTICBINSIZE=463.31271652',
     '  COVERAGECALCULATIONMETHOD=volume',
     '  DATACOLUMNS=2400',
     '  DATAROWS=2400',
     '  DAYNIGHTFLAG=Day',
     '  DESCRREVISION=6.1',
     '  EASTBOUNDINGCOORDINATE=-65.25948606',
     '  EXCLUSIONGRINGFLAG.1=N',
     '  GEOANYABNORMAL=False',
     '  GEOESTMAXRMSERROR=75.0',
     '  GIPS_Modis_Version=1.0.0',
     '  GIPS_Source_Assets=MCD43A4.A2012337.h12v04.006.20161120.hdf',
     '  GIPS_Version=0.0.0-dev',
     '  GLOBALGRIDCOLUMNS=86400',
     '  GLOBALGRIDROWS=43200',
     '  GRINGPOINTLATITUDE.1=39.78578782, 49.99719181, 50.07541801, 39.84112776',
     '  GRINGPOINTLONGITUDE.1=-78.20833299, -93.38216574, -77.75056839, '
     '-65.07807811',
     '  GRINGPOINTSEQUENCENO.1=1, 2, 3, 4',
     '  HDFEOSVersion=HDFEOS_V2.17',
     '  HORIZONTALTILENUMBER=12',
     '  identifier_product_doi=10.5067/MODIS/MCD43A4.006',
     '  identifier_product_doi_authority=http://dx.doi.org',
     '  INPUTPOINTER=MYD09GA.A2012329.h12v04.006.20152510.hdf, '
     'MYD09GA.A2012330.h12v04.006.20152511.hdf, '
     'MYD09GA.A2012331.h12v04.006.20152511.hdf, '
     'MYD09GA.A2012332.h12v04.006.20152511.hdf, '
     'MYD09GA.A2012333.h12v04.006.20152521.hdf, '
     'MYD09GA.A2012334.h12v04.006.20152521.hdf, '
     'MYD09GA.A2012335.h12v04.006.20152521.hdf, '
     'MYD09GA.A2012336.h12v04.006.20152522.hdf, '
     'MYD09GA.A2012337.h12v04.006.20152521.hdf, '
     'MYD09GA.A2012338.h12v04.006.20152511.hdf, '
     'MYD09GA.A2012339.h12v04.006.20152521.hdf, '
     'MYD09GA.A2012340.h12v04.006.20152521.hdf, '
     'MYD09GA.A2012341.h12v04.006.20152521.hdf, '
     'MYD09GA.A2012342.h12v04.006.20152522.hdf, '
     'MYD09GA.A2012343.h12v04.006.20152522.hdf, '
     'MYD09GA.A2012344.h12v04.006.20152522.hdf, '
     'MOD09GA.A2012329.h12v04.006.20152511.hdf, '
     'MOD09GA.A2012330.h12v04.006.20152510.hdf, '
     'MOD09GA.A2012331.h12v04.006.20152511.hdf, '
     'MOD09GA.A2012332.h12v04.006.20152512.hdf, '
     'MOD09GA.A2012333.h12v04.006.20152521.hdf, '
     'MOD09GA.A2012334.h12v04.006.20152522.hdf, '
     'MOD09GA.A2012335.h12v04.006.20152522.hdf, '
     'MOD09GA.A2012336.h12v04.006.20152522.hdf, '
     'MOD09GA.A2012337.h12v04.006.20152522.hdf, '
     'MOD09GA.A2012338.h12v04.006.20152511.hdf, '
     'MOD09GA.A2012339.h12v04.006.20152512.hdf, '
     'MOD09GA.A2012340.h12v04.006.20152522.hdf, '
     'MOD09GA.A2012341.h12v04.006.20152522.hdf, '
     'MOD09GA.A2012342.h12v04.006.20152522.hdf, '
     'MOD09GA.A2012343.h12v04.006.20152530.hdf, '
     'MOD09GA.A2012344.h12v04.006.20152530.hdf, MCD43DB.A2012336.6.h12v04.hdf',
     '  LOCALGRANULEID=MCD43A4.A2012337.h12v04.006.20161120.hdf',
     '  LOCALVERSIONID=6.1.34',
     '  LONGNAME=MODIS/Terra+Aqua BRDF/Albedo Nadir BRDF-Adjusted Ref Daily L3 '
     'Global - 500m',
     '  long_name=Nadir_Reflectance_Band1',
     '  MAXIMUMOBSERVATIONS=0',
     '  NADIRDATARESOLUTION=500m',
     '  NORTHBOUNDINGCOORDINATE=49.99999999',
     '  NUMBEROFGRANULES=1',
     '  PARAMETERNAME.1=NOT SET',
     '  PERCENTLANDINTILE=35',
     '  PERCENTNEWBRDFS=0',
     '  PERCENTPROCESSEDINTILE=41',
     '  PERCENTSHAPEFIXEDBRDFS=99',
     '  PERCENTSUBSTITUTEBRDFS=0',
     '  PGEVERSION=6.0.34',
     '  PROCESSINGCENTER=MODAPS',
     '  PROCESSINGENVIRONMENT=Linux minion5709 2.6.18-408.el5 #1 SMP Tue Jan 19 '
     '09:14:52 EST 2016 x86_64 x86_64 x86_64 GNU/Linux',
     '  PRODUCTIONDATETIME=2016-04-21T01:37:46.000Z',
     '  QAPERCENTGOODQUALITY=0',
     '  QAPERCENTNOTPRODUCEDCLOUD=36',
     '  QAPERCENTNOTPRODUCEDOTHER=25',
     '  QAPERCENTOTHERQUALITY=38',
     '  RANGEBEGINNINGDATE=2012-11-24',
     '  RANGEBEGINNINGTIME=00:00:00.000000',
     '  RANGEENDINGDATE=2012-12-10',
     '  RANGEENDINGTIME=23:59:59.999999',
     '  REPROCESSINGACTUAL=reprocessed',
     '  REPROCESSINGPLANNED=further update is anticipated',
     '  scale_factor=0.0001',
     '  scale_factor_err=0',
     '  SCIENCEQUALITYFLAG.1=Not Investigated',
     '  SCIENCEQUALITYFLAGEXPLANATION.1=See '
     'http://landweb.nascom/nasa.gov/cgi-bin/QA_WWW/qaFlagPage.cgi?sat=aqua the '
     'product Science Quality status.',
     '  SETUPFILEID=06121997',
     '  SHORTNAME=MCD43A4',
     '  SOUTHBOUNDINGCOORDINATE=39.99999999',
     '  SPSOPARAMETERS=2015',
     '  TileID=51012004',
     '  units=reflectance, no units',
     '  valid_range=0, 32767',
     '  VERSION=1.0',
     '  VERSIONID=6',
     '  VERTICALTILENUMBER=4',
     '  WESTBOUNDINGCOORDINATE=-93.34342959',
     '  _FillValue=32767',
     'Image Structure Metadata:',
     '  INTERLEAVE=BAND',
     'Corner Coordinates:',
     'Upper Left  (-6671703.118, 5559752.598) ( 93d20\'36.35"W, 50d 0\' 0.00"N)',
     'Lower Left  (-6671703.118, 4447802.079) ( 78d19\'27.97"W, 40d 0\' 0.00"N)',
     'Upper Right (-5559752.598, 5559752.598) ( 77d47\'10.29"W, 50d 0\' 0.00"N)',
     'Lower Right (-5559752.598, 4447802.079) ( 65d16\'13.31"W, 40d 0\' 0.00"N)',
     'Center      (-6115727.858, 5003777.339) ( 77d46\'54.29"W, 45d 0\' 0.00"N)',
     'Band 1 Block=2400x1 Type=Int16, ColorInterp=Gray',
     '  Description = isti',
     '  Minimum=0.000, Maximum=32767.000, Mean=5623.677, StdDev=2689.560',
     '  NoData Value=-32768',
     '  Offset: 0,   Scale:0.0001',
     '  Metadata:',
     '    STATISTICS_MAXIMUM=32767',
     '    STATISTICS_MEAN=5623.67667590',
     '    STATISTICS_MINIMUM=0',
     '    STATISTICS_STDDEV=2689.56047907',
     '    STATISTICS_VALID_PERCENT=31.36'])]),

 # t_process[modis-lswi] recording:
 ('lswi',
  [('modis/tiles/h12v04/2012337/h12v04_2012337_MCD_lswi.tif',
    'raster',
    'gdalinfo-stats',
    ['Driver: GTiff/GeoTIFF',
     'Size is 2400, 2400',
     'Coordinate System is:',
     'PROJCS["unnamed",',
     '    GEOGCS["Unknown datum based upon the custom spheroid",',
     '        DATUM["Not_specified_based_on_custom_spheroid",',
     '            SPHEROID["Custom spheroid",6371007.181,0]],',
     '        PRIMEM["Greenwich",0],',
     '        UNIT["degree",0.01745329]],',
     '    PROJECTION["Sinusoidal"],',
     '    PARAMETER["longitude_of_center",0],',
     '    PARAMETER["false_easting",0],',
     '    PARAMETER["false_northing",0],',
     '    UNIT["metre",1,',
     '        AUTHORITY["EPSG","9001"]]]',
     'Origin = (-6671703.11799999,5559752.59833300)',
     'Pixel Size = (463.31271652,-463.31271652)',
     'Metadata:',
     '  add_offset=0',
     '  add_offset_err=0',
     '  ALBEDOFILEID=06121997',
     '  AREA_OR_POINT=Area',
     '  ASSOCIATEDINSTRUMENTSHORTNAME.1=MODIS',
     '  ASSOCIATEDINSTRUMENTSHORTNAME.2=MODIS',
     '  ASSOCIATEDPLATFORMSHORTNAME.1=Terra',
     '  ASSOCIATEDPLATFORMSHORTNAME.2=Aqua',
     '  ASSOCIATEDSENSORSHORTNAME.1=MODIS',
     '  ASSOCIATEDSENSORSHORTNAME.2=MODIS',
     '  AUTOMATICQUALITYFLAG.1=Passed',
     '  AUTOMATICQUALITYFLAGEXPLANATION.1=Passed was set as a default value. '
     'More algorithm will be developed',
     '  AVERAGENUMBEROBS=1',
     '  BRDFCODEID=AMBRALS_V4.0R1',
     '  BRDFDATABASEVERSION=v1.0500m',
     '  calibrated_nt=5',
     '  CHARACTERISTICBINANGULARSIZE=15.0',
     '  CHARACTERISTICBINSIZE=463.31271652',
     '  COVERAGECALCULATIONMETHOD=volume',
     '  DATACOLUMNS=2400',
     '  DATAROWS=2400',
     '  DAYNIGHTFLAG=Day',
     '  DESCRREVISION=6.1',
     '  EASTBOUNDINGCOORDINATE=-65.25948606',
     '  EXCLUSIONGRINGFLAG.1=N',
     '  GEOANYABNORMAL=False',
     '  GEOESTMAXRMSERROR=75.0',
     '  GIPS_Modis_Version=1.0.0',
     '  GIPS_Source_Assets=MCD43A4.A2012337.h12v04.006.20161120.hdf',
     '  GIPS_Version=0.0.0-dev',
     '  GLOBALGRIDCOLUMNS=86400',
     '  GLOBALGRIDROWS=43200',
     '  GRINGPOINTLATITUDE.1=39.78578782, 49.99719181, 50.07541801, 39.84112776',
     '  GRINGPOINTLONGITUDE.1=-78.20833299, -93.38216574, -77.75056839, '
     '-65.07807811',
     '  GRINGPOINTSEQUENCENO.1=1, 2, 3, 4',
     '  HDFEOSVersion=HDFEOS_V2.17',
     '  HORIZONTALTILENUMBER=12',
     '  identifier_product_doi=10.5067/MODIS/MCD43A4.006',
     '  identifier_product_doi_authority=http://dx.doi.org',
     '  INPUTPOINTER=MYD09GA.A2012329.h12v04.006.20152510.hdf, '
     'MYD09GA.A2012330.h12v04.006.20152511.hdf, '
     'MYD09GA.A2012331.h12v04.006.20152511.hdf, '
     'MYD09GA.A2012332.h12v04.006.20152511.hdf, '
     'MYD09GA.A2012333.h12v04.006.20152521.hdf, '
     'MYD09GA.A2012334.h12v04.006.20152521.hdf, '
     'MYD09GA.A2012335.h12v04.006.20152521.hdf, '
     'MYD09GA.A2012336.h12v04.006.20152522.hdf, '
     'MYD09GA.A2012337.h12v04.006.20152521.hdf, '
     'MYD09GA.A2012338.h12v04.006.20152511.hdf, '
     'MYD09GA.A2012339.h12v04.006.20152521.hdf, '
     'MYD09GA.A2012340.h12v04.006.20152521.hdf, '
     'MYD09GA.A2012341.h12v04.006.20152521.hdf, '
     'MYD09GA.A2012342.h12v04.006.20152522.hdf, '
     'MYD09GA.A2012343.h12v04.006.20152522.hdf, '
     'MYD09GA.A2012344.h12v04.006.20152522.hdf, '
     'MOD09GA.A2012329.h12v04.006.20152511.hdf, '
     'MOD09GA.A2012330.h12v04.006.20152510.hdf, '
     'MOD09GA.A2012331.h12v04.006.20152511.hdf, '
     'MOD09GA.A2012332.h12v04.006.20152512.hdf, '
     'MOD09GA.A2012333.h12v04.006.20152521.hdf, '
     'MOD09GA.A2012334.h12v04.006.20152522.hdf, '
     'MOD09GA.A2012335.h12v04.006.20152522.hdf, '
     'MOD09GA.A2012336.h12v04.006.20152522.hdf, '
     'MOD09GA.A2012337.h12v04.006.20152522.hdf, '
     'MOD09GA.A2012338.h12v04.006.20152511.hdf, '
     'MOD09GA.A2012339.h12v04.006.20152512.hdf, '
     'MOD09GA.A2012340.h12v04.006.20152522.hdf, '
     'MOD09GA.A2012341.h12v04.006.20152522.hdf, '
     'MOD09GA.A2012342.h12v04.006.20152522.hdf, '
     'MOD09GA.A2012343.h12v04.006.20152530.hdf, '
     'MOD09GA.A2012344.h12v04.006.20152530.hdf, MCD43DB.A2012336.6.h12v04.hdf',
     '  LOCALGRANULEID=MCD43A4.A2012337.h12v04.006.20161120.hdf',
     '  LOCALVERSIONID=6.1.34',
     '  LONGNAME=MODIS/Terra+Aqua BRDF/Albedo Nadir BRDF-Adjusted Ref Daily L3 '
     'Global - 500m',
     '  long_name=Nadir_Reflectance_Band1',
     '  MAXIMUMOBSERVATIONS=0',
     '  NADIRDATARESOLUTION=500m',
     '  NORTHBOUNDINGCOORDINATE=49.99999999',
     '  NUMBEROFGRANULES=1',
     '  PARAMETERNAME.1=NOT SET',
     '  PERCENTLANDINTILE=35',
     '  PERCENTNEWBRDFS=0',
     '  PERCENTPROCESSEDINTILE=41',
     '  PERCENTSHAPEFIXEDBRDFS=99',
     '  PERCENTSUBSTITUTEBRDFS=0',
     '  PGEVERSION=6.0.34',
     '  PROCESSINGCENTER=MODAPS',
     '  PROCESSINGENVIRONMENT=Linux minion5709 2.6.18-408.el5 #1 SMP Tue Jan 19 '
     '09:14:52 EST 2016 x86_64 x86_64 x86_64 GNU/Linux',
     '  PRODUCTIONDATETIME=2016-04-21T01:37:46.000Z',
     '  QAPERCENTGOODQUALITY=0',
     '  QAPERCENTNOTPRODUCEDCLOUD=36',
     '  QAPERCENTNOTPRODUCEDOTHER=25',
     '  QAPERCENTOTHERQUALITY=38',
     '  RANGEBEGINNINGDATE=2012-11-24',
     '  RANGEBEGINNINGTIME=00:00:00.000000',
     '  RANGEENDINGDATE=2012-12-10',
     '  RANGEENDINGTIME=23:59:59.999999',
     '  REPROCESSINGACTUAL=reprocessed',
     '  REPROCESSINGPLANNED=further update is anticipated',
     '  scale_factor=0.0001',
     '  scale_factor_err=0',
     '  SCIENCEQUALITYFLAG.1=Not Investigated',
     '  SCIENCEQUALITYFLAGEXPLANATION.1=See '
     'http://landweb.nascom/nasa.gov/cgi-bin/QA_WWW/qaFlagPage.cgi?sat=aqua the '
     'product Science Quality status.',
     '  SETUPFILEID=06121997',
     '  SHORTNAME=MCD43A4',
     '  SOUTHBOUNDINGCOORDINATE=39.99999999',
     '  SPSOPARAMETERS=2015',
     '  TileID=51012004',
     '  units=reflectance, no units',
     '  valid_range=0, 32767',
     '  VERSION=1.0',
     '  VERSIONID=6',
     '  VERTICALTILENUMBER=4',
     '  WESTBOUNDINGCOORDINATE=-93.34342959',
     '  _FillValue=32767',
     'Image Structure Metadata:',
     '  INTERLEAVE=BAND',
     'Corner Coordinates:',
     'Upper Left  (-6671703.118, 5559752.598) ( 93d20\'36.35"W, 50d 0\' 0.00"N)',
     'Lower Left  (-6671703.118, 4447802.079) ( 78d19\'27.97"W, 40d 0\' 0.00"N)',
     'Upper Right (-5559752.598, 5559752.598) ( 77d47\'10.29"W, 50d 0\' 0.00"N)',
     'Lower Right (-5559752.598, 4447802.079) ( 65d16\'13.31"W, 40d 0\' 0.00"N)',
     'Center      (-6115727.858, 5003777.339) ( 77d46\'54.29"W, 45d 0\' 0.00"N)',
     'Band 1 Block=2400x1 Type=Int16, ColorInterp=Gray',
     '  Description = lswi',
     '  Minimum=-10000.000, Maximum=10000.000, Mean=1115.273, StdDev=4062.251',
     '  NoData Value=-32768',
     '  Offset: 0,   Scale:0.0001',
     '  Metadata:',
     '    STATISTICS_MAXIMUM=10000',
     '    STATISTICS_MEAN=1115.27320748',
     '    STATISTICS_MINIMUM=-10000',
     '    STATISTICS_STDDEV=4062.25062924',
     '    STATISTICS_VALID_PERCENT=27.44'])]),

 # t_process[modis-msavi2] recording:
 ('msavi2',
  [('modis/tiles/h12v04/2012337/h12v04_2012337_MCD_msavi2.tif',
    'raster',
    'gdalinfo-stats',
    ['Driver: GTiff/GeoTIFF',
     'Size is 2400, 2400',
     'Coordinate System is:',
     'PROJCS["unnamed",',
     '    GEOGCS["Unknown datum based upon the custom spheroid",',
     '        DATUM["Not_specified_based_on_custom_spheroid",',
     '            SPHEROID["Custom spheroid",6371007.181,0]],',
     '        PRIMEM["Greenwich",0],',
     '        UNIT["degree",0.01745329]],',
     '    PROJECTION["Sinusoidal"],',
     '    PARAMETER["longitude_of_center",0],',
     '    PARAMETER["false_easting",0],',
     '    PARAMETER["false_northing",0],',
     '    UNIT["metre",1,',
     '        AUTHORITY["EPSG","9001"]]]',
     'Origin = (-6671703.11799999,5559752.59833300)',
     'Pixel Size = (463.31271652,-463.31271652)',
     'Metadata:',
     '  add_offset=0',
     '  add_offset_err=0',
     '  ALBEDOFILEID=06121997',
     '  AREA_OR_POINT=Area',
     '  ASSOCIATEDINSTRUMENTSHORTNAME.1=MODIS',
     '  ASSOCIATEDINSTRUMENTSHORTNAME.2=MODIS',
     '  ASSOCIATEDPLATFORMSHORTNAME.1=Terra',
     '  ASSOCIATEDPLATFORMSHORTNAME.2=Aqua',
     '  ASSOCIATEDSENSORSHORTNAME.1=MODIS',
     '  ASSOCIATEDSENSORSHORTNAME.2=MODIS',
     '  AUTOMATICQUALITYFLAG.1=Passed',
     '  AUTOMATICQUALITYFLAGEXPLANATION.1=Passed was set as a default value. '
     'More algorithm will be developed',
     '  AVERAGENUMBEROBS=1',
     '  BRDFCODEID=AMBRALS_V4.0R1',
     '  BRDFDATABASEVERSION=v1.0500m',
     '  calibrated_nt=5',
     '  CHARACTERISTICBINANGULARSIZE=15.0',
     '  CHARACTERISTICBINSIZE=463.31271652',
     '  COVERAGECALCULATIONMETHOD=volume',
     '  DATACOLUMNS=2400',
     '  DATAROWS=2400',
     '  DAYNIGHTFLAG=Day',
     '  DESCRREVISION=6.1',
     '  EASTBOUNDINGCOORDINATE=-65.25948606',
     '  EXCLUSIONGRINGFLAG.1=N',
     '  GEOANYABNORMAL=False',
     '  GEOESTMAXRMSERROR=75.0',
     '  GIPS_Modis_Version=1.0.0',
     '  GIPS_Source_Assets=MCD43A4.A2012337.h12v04.006.20161120.hdf',
     '  GIPS_Version=0.0.0-dev',
     '  GLOBALGRIDCOLUMNS=86400',
     '  GLOBALGRIDROWS=43200',
     '  GRINGPOINTLATITUDE.1=39.78578782, 49.99719181, 50.07541801, 39.84112776',
     '  GRINGPOINTLONGITUDE.1=-78.20833299, -93.38216574, -77.75056839, '
     '-65.07807811',
     '  GRINGPOINTSEQUENCENO.1=1, 2, 3, 4',
     '  HDFEOSVersion=HDFEOS_V2.17',
     '  HORIZONTALTILENUMBER=12',
     '  identifier_product_doi=10.5067/MODIS/MCD43A4.006',
     '  identifier_product_doi_authority=http://dx.doi.org',
     '  INPUTPOINTER=MYD09GA.A2012329.h12v04.006.20152510.hdf, '
     'MYD09GA.A2012330.h12v04.006.20152511.hdf, '
     'MYD09GA.A2012331.h12v04.006.20152511.hdf, '
     'MYD09GA.A2012332.h12v04.006.20152511.hdf, '
     'MYD09GA.A2012333.h12v04.006.20152521.hdf, '
     'MYD09GA.A2012334.h12v04.006.20152521.hdf, '
     'MYD09GA.A2012335.h12v04.006.20152521.hdf, '
     'MYD09GA.A2012336.h12v04.006.20152522.hdf, '
     'MYD09GA.A2012337.h12v04.006.20152521.hdf, '
     'MYD09GA.A2012338.h12v04.006.20152511.hdf, '
     'MYD09GA.A2012339.h12v04.006.20152521.hdf, '
     'MYD09GA.A2012340.h12v04.006.20152521.hdf, '
     'MYD09GA.A2012341.h12v04.006.20152521.hdf, '
     'MYD09GA.A2012342.h12v04.006.20152522.hdf, '
     'MYD09GA.A2012343.h12v04.006.20152522.hdf, '
     'MYD09GA.A2012344.h12v04.006.20152522.hdf, '
     'MOD09GA.A2012329.h12v04.006.20152511.hdf, '
     'MOD09GA.A2012330.h12v04.006.20152510.hdf, '
     'MOD09GA.A2012331.h12v04.006.20152511.hdf, '
     'MOD09GA.A2012332.h12v04.006.20152512.hdf, '
     'MOD09GA.A2012333.h12v04.006.20152521.hdf, '
     'MOD09GA.A2012334.h12v04.006.20152522.hdf, '
     'MOD09GA.A2012335.h12v04.006.20152522.hdf, '
     'MOD09GA.A2012336.h12v04.006.20152522.hdf, '
     'MOD09GA.A2012337.h12v04.006.20152522.hdf, '
     'MOD09GA.A2012338.h12v04.006.20152511.hdf, '
     'MOD09GA.A2012339.h12v04.006.20152512.hdf, '
     'MOD09GA.A2012340.h12v04.006.20152522.hdf, '
     'MOD09GA.A2012341.h12v04.006.20152522.hdf, '
     'MOD09GA.A2012342.h12v04.006.20152522.hdf, '
     'MOD09GA.A2012343.h12v04.006.20152530.hdf, '
     'MOD09GA.A2012344.h12v04.006.20152530.hdf, MCD43DB.A2012336.6.h12v04.hdf',
     '  LOCALGRANULEID=MCD43A4.A2012337.h12v04.006.20161120.hdf',
     '  LOCALVERSIONID=6.1.34',
     '  LONGNAME=MODIS/Terra+Aqua BRDF/Albedo Nadir BRDF-Adjusted Ref Daily L3 '
     'Global - 500m',
     '  long_name=Nadir_Reflectance_Band1',
     '  MAXIMUMOBSERVATIONS=0',
     '  NADIRDATARESOLUTION=500m',
     '  NORTHBOUNDINGCOORDINATE=49.99999999',
     '  NUMBEROFGRANULES=1',
     '  PARAMETERNAME.1=NOT SET',
     '  PERCENTLANDINTILE=35',
     '  PERCENTNEWBRDFS=0',
     '  PERCENTPROCESSEDINTILE=41',
     '  PERCENTSHAPEFIXEDBRDFS=99',
     '  PERCENTSUBSTITUTEBRDFS=0',
     '  PGEVERSION=6.0.34',
     '  PROCESSINGCENTER=MODAPS',
     '  PROCESSINGENVIRONMENT=Linux minion5709 2.6.18-408.el5 #1 SMP Tue Jan 19 '
     '09:14:52 EST 2016 x86_64 x86_64 x86_64 GNU/Linux',
     '  PRODUCTIONDATETIME=2016-04-21T01:37:46.000Z',
     '  QAPERCENTGOODQUALITY=0',
     '  QAPERCENTNOTPRODUCEDCLOUD=36',
     '  QAPERCENTNOTPRODUCEDOTHER=25',
     '  QAPERCENTOTHERQUALITY=38',
     '  RANGEBEGINNINGDATE=2012-11-24',
     '  RANGEBEGINNINGTIME=00:00:00.000000',
     '  RANGEENDINGDATE=2012-12-10',
     '  RANGEENDINGTIME=23:59:59.999999',
     '  REPROCESSINGACTUAL=reprocessed',
     '  REPROCESSINGPLANNED=further update is anticipated',
     '  scale_factor=0.0001',
     '  scale_factor_err=0',
     '  SCIENCEQUALITYFLAG.1=Not Investigated',
     '  SCIENCEQUALITYFLAGEXPLANATION.1=See '
     'http://landweb.nascom/nasa.gov/cgi-bin/QA_WWW/qaFlagPage.cgi?sat=aqua the '
     'product Science Quality status.',
     '  SETUPFILEID=06121997',
     '  SHORTNAME=MCD43A4',
     '  SOUTHBOUNDINGCOORDINATE=39.99999999',
     '  SPSOPARAMETERS=2015',
     '  TileID=51012004',
     '  units=reflectance, no units',
     '  valid_range=0, 32767',
     '  VERSION=1.0',
     '  VERSIONID=6',
     '  VERTICALTILENUMBER=4',
     '  WESTBOUNDINGCOORDINATE=-93.34342959',
     '  _FillValue=32767',
     'Image Structure Metadata:',
     '  INTERLEAVE=BAND',
     'Corner Coordinates:',
     'Upper Left  (-6671703.118, 5559752.598) ( 93d20\'36.35"W, 50d 0\' 0.00"N)',
     'Lower Left  (-6671703.118, 4447802.079) ( 78d19\'27.97"W, 40d 0\' 0.00"N)',
     'Upper Right (-5559752.598, 5559752.598) ( 77d47\'10.29"W, 50d 0\' 0.00"N)',
     'Lower Right (-5559752.598, 4447802.079) ( 65d16\'13.31"W, 40d 0\' 0.00"N)',
     'Center      (-6115727.858, 5003777.339) ( 77d46\'54.29"W, 45d 0\' 0.00"N)',
     'Band 1 Block=2400x1 Type=Int16, ColorInterp=Gray',
     '  Description = msavi2',
     '  Minimum=0.000, Maximum=11241.000, Mean=4068.983, StdDev=1523.852',
     '  NoData Value=-32768',
     '  Offset: 0,   Scale:0.0001',
     '  Metadata:',
     '    STATISTICS_MAXIMUM=11241',
     '    STATISTICS_MEAN=4068.98317974',
     '    STATISTICS_MINIMUM=0',
     '    STATISTICS_STDDEV=1523.85205995',
     '    STATISTICS_VALID_PERCENT=39.58'])]),

 # t_process[modis-ndsi] recording:
 ('ndsi',
  [('modis/tiles/h12v04/2012337/h12v04_2012337_MCD_ndsi.tif',
    'raster',
    'gdalinfo-stats',
    ['Driver: GTiff/GeoTIFF',
     'Size is 2400, 2400',
     'Coordinate System is:',
     'PROJCS["unnamed",',
     '    GEOGCS["Unknown datum based upon the custom spheroid",',
     '        DATUM["Not_specified_based_on_custom_spheroid",',
     '            SPHEROID["Custom spheroid",6371007.181,0]],',
     '        PRIMEM["Greenwich",0],',
     '        UNIT["degree",0.01745329]],',
     '    PROJECTION["Sinusoidal"],',
     '    PARAMETER["longitude_of_center",0],',
     '    PARAMETER["false_easting",0],',
     '    PARAMETER["false_northing",0],',
     '    UNIT["metre",1,',
     '        AUTHORITY["EPSG","9001"]]]',
     'Origin = (-6671703.11799999,5559752.59833300)',
     'Pixel Size = (463.31271652,-463.31271652)',
     'Metadata:',
     '  add_offset=0',
     '  add_offset_err=0',
     '  ALBEDOFILEID=06121997',
     '  AREA_OR_POINT=Area',
     '  ASSOCIATEDINSTRUMENTSHORTNAME.1=MODIS',
     '  ASSOCIATEDINSTRUMENTSHORTNAME.2=MODIS',
     '  ASSOCIATEDPLATFORMSHORTNAME.1=Terra',
     '  ASSOCIATEDPLATFORMSHORTNAME.2=Aqua',
     '  ASSOCIATEDSENSORSHORTNAME.1=MODIS',
     '  ASSOCIATEDSENSORSHORTNAME.2=MODIS',
     '  AUTOMATICQUALITYFLAG.1=Passed',
     '  AUTOMATICQUALITYFLAGEXPLANATION.1=Passed was set as a default value. '
     'More algorithm will be developed',
     '  AVERAGENUMBEROBS=1',
     '  BRDFCODEID=AMBRALS_V4.0R1',
     '  BRDFDATABASEVERSION=v1.0500m',
     '  calibrated_nt=5',
     '  CHARACTERISTICBINANGULARSIZE=15.0',
     '  CHARACTERISTICBINSIZE=463.31271652',
     '  COVERAGECALCULATIONMETHOD=volume',
     '  DATACOLUMNS=2400',
     '  DATAROWS=2400',
     '  DAYNIGHTFLAG=Day',
     '  DESCRREVISION=6.1',
     '  EASTBOUNDINGCOORDINATE=-65.25948606',
     '  EXCLUSIONGRINGFLAG.1=N',
     '  GEOANYABNORMAL=False',
     '  GEOESTMAXRMSERROR=75.0',
     '  GIPS_Modis_Version=1.0.0',
     '  GIPS_Source_Assets=MCD43A4.A2012337.h12v04.006.20161120.hdf',
     '  GIPS_Version=0.0.0-dev',
     '  GLOBALGRIDCOLUMNS=86400',
     '  GLOBALGRIDROWS=43200',
     '  GRINGPOINTLATITUDE.1=39.78578782, 49.99719181, 50.07541801, 39.84112776',
     '  GRINGPOINTLONGITUDE.1=-78.20833299, -93.38216574, -77.75056839, '
     '-65.07807811',
     '  GRINGPOINTSEQUENCENO.1=1, 2, 3, 4',
     '  HDFEOSVersion=HDFEOS_V2.17',
     '  HORIZONTALTILENUMBER=12',
     '  identifier_product_doi=10.5067/MODIS/MCD43A4.006',
     '  identifier_product_doi_authority=http://dx.doi.org',
     '  INPUTPOINTER=MYD09GA.A2012329.h12v04.006.20152510.hdf, '
     'MYD09GA.A2012330.h12v04.006.20152511.hdf, '
     'MYD09GA.A2012331.h12v04.006.20152511.hdf, '
     'MYD09GA.A2012332.h12v04.006.20152511.hdf, '
     'MYD09GA.A2012333.h12v04.006.20152521.hdf, '
     'MYD09GA.A2012334.h12v04.006.20152521.hdf, '
     'MYD09GA.A2012335.h12v04.006.20152521.hdf, '
     'MYD09GA.A2012336.h12v04.006.20152522.hdf, '
     'MYD09GA.A2012337.h12v04.006.20152521.hdf, '
     'MYD09GA.A2012338.h12v04.006.20152511.hdf, '
     'MYD09GA.A2012339.h12v04.006.20152521.hdf, '
     'MYD09GA.A2012340.h12v04.006.20152521.hdf, '
     'MYD09GA.A2012341.h12v04.006.20152521.hdf, '
     'MYD09GA.A2012342.h12v04.006.20152522.hdf, '
     'MYD09GA.A2012343.h12v04.006.20152522.hdf, '
     'MYD09GA.A2012344.h12v04.006.20152522.hdf, '
     'MOD09GA.A2012329.h12v04.006.20152511.hdf, '
     'MOD09GA.A2012330.h12v04.006.20152510.hdf, '
     'MOD09GA.A2012331.h12v04.006.20152511.hdf, '
     'MOD09GA.A2012332.h12v04.006.20152512.hdf, '
     'MOD09GA.A2012333.h12v04.006.20152521.hdf, '
     'MOD09GA.A2012334.h12v04.006.20152522.hdf, '
     'MOD09GA.A2012335.h12v04.006.20152522.hdf, '
     'MOD09GA.A2012336.h12v04.006.20152522.hdf, '
     'MOD09GA.A2012337.h12v04.006.20152522.hdf, '
     'MOD09GA.A2012338.h12v04.006.20152511.hdf, '
     'MOD09GA.A2012339.h12v04.006.20152512.hdf, '
     'MOD09GA.A2012340.h12v04.006.20152522.hdf, '
     'MOD09GA.A2012341.h12v04.006.20152522.hdf, '
     'MOD09GA.A2012342.h12v04.006.20152522.hdf, '
     'MOD09GA.A2012343.h12v04.006.20152530.hdf, '
     'MOD09GA.A2012344.h12v04.006.20152530.hdf, MCD43DB.A2012336.6.h12v04.hdf',
     '  LOCALGRANULEID=MCD43A4.A2012337.h12v04.006.20161120.hdf',
     '  LOCALVERSIONID=6.1.34',
     '  LONGNAME=MODIS/Terra+Aqua BRDF/Albedo Nadir BRDF-Adjusted Ref Daily L3 '
     'Global - 500m',
     '  long_name=Nadir_Reflectance_Band1',
     '  MAXIMUMOBSERVATIONS=0',
     '  NADIRDATARESOLUTION=500m',
     '  NORTHBOUNDINGCOORDINATE=49.99999999',
     '  NUMBEROFGRANULES=1',
     '  PARAMETERNAME.1=NOT SET',
     '  PERCENTLANDINTILE=35',
     '  PERCENTNEWBRDFS=0',
     '  PERCENTPROCESSEDINTILE=41',
     '  PERCENTSHAPEFIXEDBRDFS=99',
     '  PERCENTSUBSTITUTEBRDFS=0',
     '  PGEVERSION=6.0.34',
     '  PROCESSINGCENTER=MODAPS',
     '  PROCESSINGENVIRONMENT=Linux minion5709 2.6.18-408.el5 #1 SMP Tue Jan 19 '
     '09:14:52 EST 2016 x86_64 x86_64 x86_64 GNU/Linux',
     '  PRODUCTIONDATETIME=2016-04-21T01:37:46.000Z',
     '  QAPERCENTGOODQUALITY=0',
     '  QAPERCENTNOTPRODUCEDCLOUD=36',
     '  QAPERCENTNOTPRODUCEDOTHER=25',
     '  QAPERCENTOTHERQUALITY=38',
     '  RANGEBEGINNINGDATE=2012-11-24',
     '  RANGEBEGINNINGTIME=00:00:00.000000',
     '  RANGEENDINGDATE=2012-12-10',
     '  RANGEENDINGTIME=23:59:59.999999',
     '  REPROCESSINGACTUAL=reprocessed',
     '  REPROCESSINGPLANNED=further update is anticipated',
     '  scale_factor=0.0001',
     '  scale_factor_err=0',
     '  SCIENCEQUALITYFLAG.1=Not Investigated',
     '  SCIENCEQUALITYFLAGEXPLANATION.1=See '
     'http://landweb.nascom/nasa.gov/cgi-bin/QA_WWW/qaFlagPage.cgi?sat=aqua the '
     'product Science Quality status.',
     '  SETUPFILEID=06121997',
     '  SHORTNAME=MCD43A4',
     '  SOUTHBOUNDINGCOORDINATE=39.99999999',
     '  SPSOPARAMETERS=2015',
     '  TileID=51012004',
     '  units=reflectance, no units',
     '  valid_range=0, 32767',
     '  VERSION=1.0',
     '  VERSIONID=6',
     '  VERTICALTILENUMBER=4',
     '  WESTBOUNDINGCOORDINATE=-93.34342959',
     '  _FillValue=32767',
     'Image Structure Metadata:',
     '  INTERLEAVE=BAND',
     'Corner Coordinates:',
     'Upper Left  (-6671703.118, 5559752.598) ( 93d20\'36.35"W, 50d 0\' 0.00"N)',
     'Lower Left  (-6671703.118, 4447802.079) ( 78d19\'27.97"W, 40d 0\' 0.00"N)',
     'Upper Right (-5559752.598, 5559752.598) ( 77d47\'10.29"W, 50d 0\' 0.00"N)',
     'Lower Right (-5559752.598, 4447802.079) ( 65d16\'13.31"W, 40d 0\' 0.00"N)',
     'Center      (-6115727.858, 5003777.339) ( 77d46\'54.29"W, 45d 0\' 0.00"N)',
     'Band 1 Block=2400x1 Type=Int16, ColorInterp=Gray',
     '  Description = ndsi',
     '  Minimum=-10000.000, Maximum=10000.000, Mean=-1041.783, StdDev=5406.760',
     '  NoData Value=-32768',
     '  Offset: 0,   Scale:0.0001',
     '  Metadata:',
     '    STATISTICS_MAXIMUM=10000',
     '    STATISTICS_MEAN=-1041.78304799',
     '    STATISTICS_MINIMUM=-10000',
     '    STATISTICS_STDDEV=5406.76014372',
     '    STATISTICS_VALID_PERCENT=31.72'])]),

 # t_process[modis-ndti] recording:
 ('ndti',
  [('modis/tiles/h12v04/2012337/h12v04_2012337_MCD_ndti.tif',
    'raster',
    'gdalinfo-stats',
    ['Driver: GTiff/GeoTIFF',
     'Size is 2400, 2400',
     'Coordinate System is:',
     'PROJCS["unnamed",',
     '    GEOGCS["Unknown datum based upon the custom spheroid",',
     '        DATUM["Not_specified_based_on_custom_spheroid",',
     '            SPHEROID["Custom spheroid",6371007.181,0]],',
     '        PRIMEM["Greenwich",0],',
     '        UNIT["degree",0.01745329]],',
     '    PROJECTION["Sinusoidal"],',
     '    PARAMETER["longitude_of_center",0],',
     '    PARAMETER["false_easting",0],',
     '    PARAMETER["false_northing",0],',
     '    UNIT["metre",1,',
     '        AUTHORITY["EPSG","9001"]]]',
     'Origin = (-6671703.11799999,5559752.59833300)',
     'Pixel Size = (463.31271652,-463.31271652)',
     'Metadata:',
     '  add_offset=0',
     '  add_offset_err=0',
     '  ALBEDOFILEID=06121997',
     '  AREA_OR_POINT=Area',
     '  ASSOCIATEDINSTRUMENTSHORTNAME.1=MODIS',
     '  ASSOCIATEDINSTRUMENTSHORTNAME.2=MODIS',
     '  ASSOCIATEDPLATFORMSHORTNAME.1=Terra',
     '  ASSOCIATEDPLATFORMSHORTNAME.2=Aqua',
     '  ASSOCIATEDSENSORSHORTNAME.1=MODIS',
     '  ASSOCIATEDSENSORSHORTNAME.2=MODIS',
     '  AUTOMATICQUALITYFLAG.1=Passed',
     '  AUTOMATICQUALITYFLAGEXPLANATION.1=Passed was set as a default value. '
     'More algorithm will be developed',
     '  AVERAGENUMBEROBS=1',
     '  BRDFCODEID=AMBRALS_V4.0R1',
     '  BRDFDATABASEVERSION=v1.0500m',
     '  calibrated_nt=5',
     '  CHARACTERISTICBINANGULARSIZE=15.0',
     '  CHARACTERISTICBINSIZE=463.31271652',
     '  COVERAGECALCULATIONMETHOD=volume',
     '  DATACOLUMNS=2400',
     '  DATAROWS=2400',
     '  DAYNIGHTFLAG=Day',
     '  DESCRREVISION=6.1',
     '  EASTBOUNDINGCOORDINATE=-65.25948606',
     '  EXCLUSIONGRINGFLAG.1=N',
     '  GEOANYABNORMAL=False',
     '  GEOESTMAXRMSERROR=75.0',
     '  GIPS_Modis_Version=1.0.0',
     '  GIPS_Source_Assets=MCD43A4.A2012337.h12v04.006.20161120.hdf',
     '  GIPS_Version=0.0.0-dev',
     '  GLOBALGRIDCOLUMNS=86400',
     '  GLOBALGRIDROWS=43200',
     '  GRINGPOINTLATITUDE.1=39.78578782, 49.99719181, 50.07541801, 39.84112776',
     '  GRINGPOINTLONGITUDE.1=-78.20833299, -93.38216574, -77.75056839, '
     '-65.07807811',
     '  GRINGPOINTSEQUENCENO.1=1, 2, 3, 4',
     '  HDFEOSVersion=HDFEOS_V2.17',
     '  HORIZONTALTILENUMBER=12',
     '  identifier_product_doi=10.5067/MODIS/MCD43A4.006',
     '  identifier_product_doi_authority=http://dx.doi.org',
     '  INPUTPOINTER=MYD09GA.A2012329.h12v04.006.20152510.hdf, '
     'MYD09GA.A2012330.h12v04.006.20152511.hdf, '
     'MYD09GA.A2012331.h12v04.006.20152511.hdf, '
     'MYD09GA.A2012332.h12v04.006.20152511.hdf, '
     'MYD09GA.A2012333.h12v04.006.20152521.hdf, '
     'MYD09GA.A2012334.h12v04.006.20152521.hdf, '
     'MYD09GA.A2012335.h12v04.006.20152521.hdf, '
     'MYD09GA.A2012336.h12v04.006.20152522.hdf, '
     'MYD09GA.A2012337.h12v04.006.20152521.hdf, '
     'MYD09GA.A2012338.h12v04.006.20152511.hdf, '
     'MYD09GA.A2012339.h12v04.006.20152521.hdf, '
     'MYD09GA.A2012340.h12v04.006.20152521.hdf, '
     'MYD09GA.A2012341.h12v04.006.20152521.hdf, '
     'MYD09GA.A2012342.h12v04.006.20152522.hdf, '
     'MYD09GA.A2012343.h12v04.006.20152522.hdf, '
     'MYD09GA.A2012344.h12v04.006.20152522.hdf, '
     'MOD09GA.A2012329.h12v04.006.20152511.hdf, '
     'MOD09GA.A2012330.h12v04.006.20152510.hdf, '
     'MOD09GA.A2012331.h12v04.006.20152511.hdf, '
     'MOD09GA.A2012332.h12v04.006.20152512.hdf, '
     'MOD09GA.A2012333.h12v04.006.20152521.hdf, '
     'MOD09GA.A2012334.h12v04.006.20152522.hdf, '
     'MOD09GA.A2012335.h12v04.006.20152522.hdf, '
     'MOD09GA.A2012336.h12v04.006.20152522.hdf, '
     'MOD09GA.A2012337.h12v04.006.20152522.hdf, '
     'MOD09GA.A2012338.h12v04.006.20152511.hdf, '
     'MOD09GA.A2012339.h12v04.006.20152512.hdf, '
     'MOD09GA.A2012340.h12v04.006.20152522.hdf, '
     'MOD09GA.A2012341.h12v04.006.20152522.hdf, '
     'MOD09GA.A2012342.h12v04.006.20152522.hdf, '
     'MOD09GA.A2012343.h12v04.006.20152530.hdf, '
     'MOD09GA.A2012344.h12v04.006.20152530.hdf, MCD43DB.A2012336.6.h12v04.hdf',
     '  LOCALGRANULEID=MCD43A4.A2012337.h12v04.006.20161120.hdf',
     '  LOCALVERSIONID=6.1.34',
     '  LONGNAME=MODIS/Terra+Aqua BRDF/Albedo Nadir BRDF-Adjusted Ref Daily L3 '
     'Global - 500m',
     '  long_name=Nadir_Reflectance_Band1',
     '  MAXIMUMOBSERVATIONS=0',
     '  NADIRDATARESOLUTION=500m',
     '  NORTHBOUNDINGCOORDINATE=49.99999999',
     '  NUMBEROFGRANULES=1',
     '  PARAMETERNAME.1=NOT SET',
     '  PERCENTLANDINTILE=35',
     '  PERCENTNEWBRDFS=0',
     '  PERCENTPROCESSEDINTILE=41',
     '  PERCENTSHAPEFIXEDBRDFS=99',
     '  PERCENTSUBSTITUTEBRDFS=0',
     '  PGEVERSION=6.0.34',
     '  PROCESSINGCENTER=MODAPS',
     '  PROCESSINGENVIRONMENT=Linux minion5709 2.6.18-408.el5 #1 SMP Tue Jan 19 '
     '09:14:52 EST 2016 x86_64 x86_64 x86_64 GNU/Linux',
     '  PRODUCTIONDATETIME=2016-04-21T01:37:46.000Z',
     '  QAPERCENTGOODQUALITY=0',
     '  QAPERCENTNOTPRODUCEDCLOUD=36',
     '  QAPERCENTNOTPRODUCEDOTHER=25',
     '  QAPERCENTOTHERQUALITY=38',
     '  RANGEBEGINNINGDATE=2012-11-24',
     '  RANGEBEGINNINGTIME=00:00:00.000000',
     '  RANGEENDINGDATE=2012-12-10',
     '  RANGEENDINGTIME=23:59:59.999999',
     '  REPROCESSINGACTUAL=reprocessed',
     '  REPROCESSINGPLANNED=further update is anticipated',
     '  scale_factor=0.0001',
     '  scale_factor_err=0',
     '  SCIENCEQUALITYFLAG.1=Not Investigated',
     '  SCIENCEQUALITYFLAGEXPLANATION.1=See '
     'http://landweb.nascom/nasa.gov/cgi-bin/QA_WWW/qaFlagPage.cgi?sat=aqua the '
     'product Science Quality status.',
     '  SETUPFILEID=06121997',
     '  SHORTNAME=MCD43A4',
     '  SOUTHBOUNDINGCOORDINATE=39.99999999',
     '  SPSOPARAMETERS=2015',
     '  TileID=51012004',
     '  units=reflectance, no units',
     '  valid_range=0, 32767',
     '  VERSION=1.0',
     '  VERSIONID=6',
     '  VERTICALTILENUMBER=4',
     '  WESTBOUNDINGCOORDINATE=-93.34342959',
     '  _FillValue=32767',
     'Image Structure Metadata:',
     '  INTERLEAVE=BAND',
     'Corner Coordinates:',
     'Upper Left  (-6671703.118, 5559752.598) ( 93d20\'36.35"W, 50d 0\' 0.00"N)',
     'Lower Left  (-6671703.118, 4447802.079) ( 78d19\'27.97"W, 40d 0\' 0.00"N)',
     'Upper Right (-5559752.598, 5559752.598) ( 77d47\'10.29"W, 50d 0\' 0.00"N)',
     'Lower Right (-5559752.598, 4447802.079) ( 65d16\'13.31"W, 40d 0\' 0.00"N)',
     'Center      (-6115727.858, 5003777.339) ( 77d46\'54.29"W, 45d 0\' 0.00"N)',
     'Band 1 Block=2400x1 Type=Int16, ColorInterp=Gray',
     '  Description = ndti',
     '  Minimum=-10000.000, Maximum=10000.000, Mean=3040.621, StdDev=1668.565',
     '  NoData Value=-32768',
     '  Offset: 0,   Scale:0.0001',
     '  Metadata:',
     '    STATISTICS_MAXIMUM=10000',
     '    STATISTICS_MEAN=3040.62093259',
     '    STATISTICS_MINIMUM=-10000',
     '    STATISTICS_STDDEV=1668.56466401',
     '    STATISTICS_VALID_PERCENT=31.36'])]),

 # t_process[modis-ndvi] recording:
 ('ndvi',
  [('modis/tiles/h12v04/2012337/h12v04_2012337_MCD_ndvi.tif',
    'raster',
    'gdalinfo-stats',
    ['Driver: GTiff/GeoTIFF',
     'Size is 2400, 2400',
     'Coordinate System is:',
     'PROJCS["unnamed",',
     '    GEOGCS["Unknown datum based upon the custom spheroid",',
     '        DATUM["Not_specified_based_on_custom_spheroid",',
     '            SPHEROID["Custom spheroid",6371007.181,0]],',
     '        PRIMEM["Greenwich",0],',
     '        UNIT["degree",0.01745329]],',
     '    PROJECTION["Sinusoidal"],',
     '    PARAMETER["longitude_of_center",0],',
     '    PARAMETER["false_easting",0],',
     '    PARAMETER["false_northing",0],',
     '    UNIT["metre",1,',
     '        AUTHORITY["EPSG","9001"]]]',
     'Origin = (-6671703.11799999,5559752.59833300)',
     'Pixel Size = (463.31271652,-463.31271652)',
     'Metadata:',
     '  add_offset=0',
     '  add_offset_err=0',
     '  ALBEDOFILEID=06121997',
     '  AREA_OR_POINT=Area',
     '  ASSOCIATEDINSTRUMENTSHORTNAME.1=MODIS',
     '  ASSOCIATEDINSTRUMENTSHORTNAME.2=MODIS',
     '  ASSOCIATEDPLATFORMSHORTNAME.1=Terra',
     '  ASSOCIATEDPLATFORMSHORTNAME.2=Aqua',
     '  ASSOCIATEDSENSORSHORTNAME.1=MODIS',
     '  ASSOCIATEDSENSORSHORTNAME.2=MODIS',
     '  AUTOMATICQUALITYFLAG.1=Passed',
     '  AUTOMATICQUALITYFLAGEXPLANATION.1=Passed was set as a default value. '
     'More algorithm will be developed',
     '  AVERAGENUMBEROBS=1',
     '  BRDFCODEID=AMBRALS_V4.0R1',
     '  BRDFDATABASEVERSION=v1.0500m',
     '  calibrated_nt=5',
     '  CHARACTERISTICBINANGULARSIZE=15.0',
     '  CHARACTERISTICBINSIZE=463.31271652',
     '  COVERAGECALCULATIONMETHOD=volume',
     '  DATACOLUMNS=2400',
     '  DATAROWS=2400',
     '  DAYNIGHTFLAG=Day',
     '  DESCRREVISION=6.1',
     '  EASTBOUNDINGCOORDINATE=-65.25948606',
     '  EXCLUSIONGRINGFLAG.1=N',
     '  GEOANYABNORMAL=False',
     '  GEOESTMAXRMSERROR=75.0',
     '  GIPS_Modis_Version=1.0.0',
     '  GIPS_Source_Assets=MCD43A4.A2012337.h12v04.006.20161120.hdf',
     '  GIPS_Version=0.0.0-dev',
     '  GLOBALGRIDCOLUMNS=86400',
     '  GLOBALGRIDROWS=43200',
     '  GRINGPOINTLATITUDE.1=39.78578782, 49.99719181, 50.07541801, 39.84112776',
     '  GRINGPOINTLONGITUDE.1=-78.20833299, -93.38216574, -77.75056839, '
     '-65.07807811',
     '  GRINGPOINTSEQUENCENO.1=1, 2, 3, 4',
     '  HDFEOSVersion=HDFEOS_V2.17',
     '  HORIZONTALTILENUMBER=12',
     '  identifier_product_doi=10.5067/MODIS/MCD43A4.006',
     '  identifier_product_doi_authority=http://dx.doi.org',
     '  INPUTPOINTER=MYD09GA.A2012329.h12v04.006.20152510.hdf, '
     'MYD09GA.A2012330.h12v04.006.20152511.hdf, '
     'MYD09GA.A2012331.h12v04.006.20152511.hdf, '
     'MYD09GA.A2012332.h12v04.006.20152511.hdf, '
     'MYD09GA.A2012333.h12v04.006.20152521.hdf, '
     'MYD09GA.A2012334.h12v04.006.20152521.hdf, '
     'MYD09GA.A2012335.h12v04.006.20152521.hdf, '
     'MYD09GA.A2012336.h12v04.006.20152522.hdf, '
     'MYD09GA.A2012337.h12v04.006.20152521.hdf, '
     'MYD09GA.A2012338.h12v04.006.20152511.hdf, '
     'MYD09GA.A2012339.h12v04.006.20152521.hdf, '
     'MYD09GA.A2012340.h12v04.006.20152521.hdf, '
     'MYD09GA.A2012341.h12v04.006.20152521.hdf, '
     'MYD09GA.A2012342.h12v04.006.20152522.hdf, '
     'MYD09GA.A2012343.h12v04.006.20152522.hdf, '
     'MYD09GA.A2012344.h12v04.006.20152522.hdf, '
     'MOD09GA.A2012329.h12v04.006.20152511.hdf, '
     'MOD09GA.A2012330.h12v04.006.20152510.hdf, '
     'MOD09GA.A2012331.h12v04.006.20152511.hdf, '
     'MOD09GA.A2012332.h12v04.006.20152512.hdf, '
     'MOD09GA.A2012333.h12v04.006.20152521.hdf, '
     'MOD09GA.A2012334.h12v04.006.20152522.hdf, '
     'MOD09GA.A2012335.h12v04.006.20152522.hdf, '
     'MOD09GA.A2012336.h12v04.006.20152522.hdf, '
     'MOD09GA.A2012337.h12v04.006.20152522.hdf, '
     'MOD09GA.A2012338.h12v04.006.20152511.hdf, '
     'MOD09GA.A2012339.h12v04.006.20152512.hdf, '
     'MOD09GA.A2012340.h12v04.006.20152522.hdf, '
     'MOD09GA.A2012341.h12v04.006.20152522.hdf, '
     'MOD09GA.A2012342.h12v04.006.20152522.hdf, '
     'MOD09GA.A2012343.h12v04.006.20152530.hdf, '
     'MOD09GA.A2012344.h12v04.006.20152530.hdf, MCD43DB.A2012336.6.h12v04.hdf',
     '  LOCALGRANULEID=MCD43A4.A2012337.h12v04.006.20161120.hdf',
     '  LOCALVERSIONID=6.1.34',
     '  LONGNAME=MODIS/Terra+Aqua BRDF/Albedo Nadir BRDF-Adjusted Ref Daily L3 '
     'Global - 500m',
     '  long_name=Nadir_Reflectance_Band1',
     '  MAXIMUMOBSERVATIONS=0',
     '  NADIRDATARESOLUTION=500m',
     '  NORTHBOUNDINGCOORDINATE=49.99999999',
     '  NUMBEROFGRANULES=1',
     '  PARAMETERNAME.1=NOT SET',
     '  PERCENTLANDINTILE=35',
     '  PERCENTNEWBRDFS=0',
     '  PERCENTPROCESSEDINTILE=41',
     '  PERCENTSHAPEFIXEDBRDFS=99',
     '  PERCENTSUBSTITUTEBRDFS=0',
     '  PGEVERSION=6.0.34',
     '  PROCESSINGCENTER=MODAPS',
     '  PROCESSINGENVIRONMENT=Linux minion5709 2.6.18-408.el5 #1 SMP Tue Jan 19 '
     '09:14:52 EST 2016 x86_64 x86_64 x86_64 GNU/Linux',
     '  PRODUCTIONDATETIME=2016-04-21T01:37:46.000Z',
     '  QAPERCENTGOODQUALITY=0',
     '  QAPERCENTNOTPRODUCEDCLOUD=36',
     '  QAPERCENTNOTPRODUCEDOTHER=25',
     '  QAPERCENTOTHERQUALITY=38',
     '  RANGEBEGINNINGDATE=2012-11-24',
     '  RANGEBEGINNINGTIME=00:00:00.000000',
     '  RANGEENDINGDATE=2012-12-10',
     '  RANGEENDINGTIME=23:59:59.999999',
     '  REPROCESSINGACTUAL=reprocessed',
     '  REPROCESSINGPLANNED=further update is anticipated',
     '  scale_factor=0.0001',
     '  scale_factor_err=0',
     '  SCIENCEQUALITYFLAG.1=Not Investigated',
     '  SCIENCEQUALITYFLAGEXPLANATION.1=See '
     'http://landweb.nascom/nasa.gov/cgi-bin/QA_WWW/qaFlagPage.cgi?sat=aqua the '
     'product Science Quality status.',
     '  SETUPFILEID=06121997',
     '  SHORTNAME=MCD43A4',
     '  SOUTHBOUNDINGCOORDINATE=39.99999999',
     '  SPSOPARAMETERS=2015',
     '  TileID=51012004',
     '  units=reflectance, no units',
     '  valid_range=0, 32767',
     '  VERSION=1.0',
     '  VERSIONID=6',
     '  VERTICALTILENUMBER=4',
     '  WESTBOUNDINGCOORDINATE=-93.34342959',
     '  _FillValue=32767',
     'Image Structure Metadata:',
     '  INTERLEAVE=BAND',
     'Corner Coordinates:',
     'Upper Left  (-6671703.118, 5559752.598) ( 93d20\'36.35"W, 50d 0\' 0.00"N)',
     'Lower Left  (-6671703.118, 4447802.079) ( 78d19\'27.97"W, 40d 0\' 0.00"N)',
     'Upper Right (-5559752.598, 5559752.598) ( 77d47\'10.29"W, 50d 0\' 0.00"N)',
     'Lower Right (-5559752.598, 4447802.079) ( 65d16\'13.31"W, 40d 0\' 0.00"N)',
     'Center      (-6115727.858, 5003777.339) ( 77d46\'54.29"W, 45d 0\' 0.00"N)',
     'Band 1 Block=2400x1 Type=Int16, ColorInterp=Gray',
     '  Description = ndvi',
     '  Minimum=-10000.000, Maximum=10000.000, Mean=3449.428, StdDev=3748.983',
     '  NoData Value=-32768',
     '  Offset: 0,   Scale:0.0001',
     '  Metadata:',
     '    STATISTICS_MAXIMUM=10000',
     '    STATISTICS_MEAN=3449.42843802',
     '    STATISTICS_MINIMUM=-10000',
     '    STATISTICS_STDDEV=3748.98268010',
     '    STATISTICS_VALID_PERCENT=39.58'])]),

 # t_process[modis-ndvi8] recording:
 ('ndvi8',
  [('modis/tiles/h12v04/2012337/h12v04_2012337_MOD_ndvi8.tif',
    'raster',
    'gdalinfo-stats',
    ['Driver: GTiff/GeoTIFF',
     'Size is 4800, 4800',
     'Coordinate System is:',
     'PROJCS["unnamed",',
     '    GEOGCS["Unknown datum based upon the custom spheroid",',
     '        DATUM["Not_specified_based_on_custom_spheroid",',
     '            SPHEROID["Custom spheroid",6371007.181,0]],',
     '        PRIMEM["Greenwich",0],',
     '        UNIT["degree",0.01745329]],',
     '    PROJECTION["Sinusoidal"],',
     '    PARAMETER["longitude_of_center",0],',
     '    PARAMETER["false_easting",0],',
     '    PARAMETER["false_northing",0],',
     '    UNIT["metre",1,',
     '        AUTHORITY["EPSG","9001"]]]',
     'Origin = (-6671703.11799999,5559752.59833300)',
     'Pixel Size = (231.65635826,-231.65635826)',
     'Metadata:',
     '  add_offset=0',
     '  add_offset_err=0',
     '  AREA_OR_POINT=Area',
     '  ASSOCIATEDINSTRUMENTSHORTNAME.1=MODIS',
     '  ASSOCIATEDPLATFORMSHORTNAME.1=Terra',
     '  ASSOCIATEDSENSORSHORTNAME.1=MODIS',
     '  AUTOMATICQUALITYFLAG.1=Passed',
     '  AUTOMATICQUALITYFLAGEXPLANATION.1=Always Passed',
     '  AVAILABLE_ASSETS=MOD09Q1',
     '  calibrated_nt=5',
     '  CHARACTERISTICBINANGULARSIZE250M=7.5',
     '  CHARACTERISTICBINANGULARSIZE500M=15.0',
     '  CHARACTERISTICBINSIZE250M=231.65635826',
     '  CHARACTERISTICBINSIZE500M=463.31271652',
     '  DATACOLUMNS250M=4800',
     '  DATACOLUMNS500M=2400',
     '  DATAROWS250M=4800',
     '  DATAROWS500M=2400',
     '  DAYNIGHTFLAG=Both',
     '  DESCRREVISION=6.0',
     '  EASTBOUNDINGCOORDINATE=-65.25948606',
     '  EQUATORCROSSINGDATE.1=2012-12-02',
     '  EQUATORCROSSINGDATE.10=2012-12-05',
     '  EQUATORCROSSINGDATE.11=2012-12-06',
     '  EQUATORCROSSINGDATE.12=2012-12-06',
     '  EQUATORCROSSINGDATE.13=2012-12-06',
     '  EQUATORCROSSINGDATE.14=2012-12-07',
     '  EQUATORCROSSINGDATE.15=2012-12-07',
     '  EQUATORCROSSINGDATE.16=2012-12-07',
     '  EQUATORCROSSINGDATE.17=2012-12-08',
     '  EQUATORCROSSINGDATE.18=2012-12-08',
     '  EQUATORCROSSINGDATE.19=2012-12-09',
     '  EQUATORCROSSINGDATE.2=2012-12-02',
     '  EQUATORCROSSINGDATE.20=2012-12-09',
     '  EQUATORCROSSINGDATE.21=2012-12-09',
     '  EQUATORCROSSINGDATE.3=2012-12-02',
     '  EQUATORCROSSINGDATE.4=2012-12-03',
     '  EQUATORCROSSINGDATE.5=2012-12-03',
     '  EQUATORCROSSINGDATE.6=2012-12-04',
     '  EQUATORCROSSINGDATE.7=2012-12-04',
     '  EQUATORCROSSINGDATE.8=2012-12-04',
     '  EQUATORCROSSINGDATE.9=2012-12-05',
     '  EQUATORCROSSINGLONGITUDE.1=-67.61842541',
     '  EQUATORCROSSINGLONGITUDE.10=-100.06470189',
     '  EQUATORCROSSINGLONGITUDE.11=-61.43623870',
     '  EQUATORCROSSINGLONGITUDE.12=-86.15767595',
     '  EQUATORCROSSINGLONGITUDE.13=-110.87974502',
     '  EQUATORCROSSINGLONGITUDE.14=-72.25084175',
     '  EQUATORCROSSINGLONGITUDE.15=-96.97273361',
     '  EQUATORCROSSINGLONGITUDE.16=-121.69454168',
     '  EQUATORCROSSINGLONGITUDE.17=-83.06546752',
     '  EQUATORCROSSINGLONGITUDE.18=-107.78754378',
     '  EQUATORCROSSINGLONGITUDE.19=-69.15842883',
     '  EQUATORCROSSINGLONGITUDE.2=-92.34022247',
     '  EQUATORCROSSINGLONGITUDE.20=-93.88019617',
     '  EQUATORCROSSINGLONGITUDE.21=-118.60208741',
     '  EQUATORCROSSINGLONGITUDE.3=-117.06220722',
     '  EQUATORCROSSINGLONGITUDE.4=-78.43381595',
     '  EQUATORCROSSINGLONGITUDE.5=-103.15591823',
     '  EQUATORCROSSINGLONGITUDE.6=-64.52758580',
     '  EQUATORCROSSINGLONGITUDE.7=-89.24920604',
     '  EQUATORCROSSINGLONGITUDE.8=-113.97126235',
     '  EQUATORCROSSINGLONGITUDE.9=-75.34269328',
     '  EQUATORCROSSINGTIME.1=15:00:18.332032',
     '  EQUATORCROSSINGTIME.10=17:10:05.982405',
     '  EQUATORCROSSINGTIME.11=14:35:35.474864',
     '  EQUATORCROSSINGTIME.12=16:14:28.610478',
     '  EQUATORCROSSINGTIME.13=17:53:21.799475',
     '  EQUATORCROSSINGTIME.14=15:18:51.245301',
     '  EQUATORCROSSINGTIME.15=16:57:44.424602',
     '  EQUATORCROSSINGTIME.16=18:36:37.572900',
     '  EQUATORCROSSINGTIME.17=16:02:07.023733',
     '  EQUATORCROSSINGTIME.18=17:41:00.212328',
     '  EQUATORCROSSINGTIME.19=15:06:29.602598',
     '  EQUATORCROSSINGTIME.2=16:39:11.504411',
     '  EQUATORCROSSINGTIME.20=16:45:22.768347',
     '  EQUATORCROSSINGTIME.21=18:24:15.930784',
     '  EQUATORCROSSINGTIME.3=18:18:04.685793',
     '  EQUATORCROSSINGTIME.4=15:43:34.242444',
     '  EQUATORCROSSINGTIME.5=17:22:27.439023',
     '  EQUATORCROSSINGTIME.6=14:47:56.952352',
     '  EQUATORCROSSINGTIME.7=16:26:50.106511',
     '  EQUATORCROSSINGTIME.8=18:05:43.293751',
     '  EQUATORCROSSINGTIME.9=15:31:12.793675',
     '  EXCLUSIONGRINGFLAG.1=N',
     '  GEOANYABNORMAL=False',
     '  GEOESTMAXRMSERROR=50.0',
     '  GIPS_Modis_Version=1.0.0',
     '  GIPS_Source_Assets=MOD09Q1.A2012337.h12v04.006.20152530.hdf',
     '  GIPS_Version=0.0.0-dev',
     '  GLOBALGRIDCOLUMNS250M=172800',
     '  GLOBALGRIDCOLUMNS500M=86400',
     '  GLOBALGRIDROWS250M=86400',
     '  GLOBALGRIDROWS500M=43200',
     '  GRANULEBEGINNINGDATETIME=2012-12-02T14:45:00.000000Z, '
     '2012-12-03T15:30:00.000000Z, 2012-12-04T14:35:00.000000Z, '
     '2012-12-05T15:15:00.000000Z, 2012-12-06T14:20:00.000000Z, '
     '2012-12-07T15:05:00.000000Z, 2012-12-08T15:45:00.000000Z, '
     '2012-12-09T14:50:00.000000Z',
     '  GRANULEDAYNIGHTFLAG=Day, Day, Day, Day, Day, Day, Day, Both',
     '  GRANULEDAYOFYEAR=337, 338, 339, 340, 341, 342, 343, 344',
     '  GRANULEENDINGDATETIME=2012-12-02T18:05:00.000000Z, '
     '2012-12-03T17:15:00.000000Z, 2012-12-04T17:55:00.000000Z, '
     '2012-12-05T17:00:00.000000Z, 2012-12-06T17:45:00.000000Z, '
     '2012-12-07T18:25:00.000000Z, 2012-12-08T17:30:00.000000Z, '
     '2012-12-09T18:15:00.000000Z',
     '  GRINGPOINTLATITUDE.1=39.78578782, 49.99719181, 50.07541801, 39.84112776',
     '  GRINGPOINTLONGITUDE.1=-78.20833299, -93.38216574, -77.75056839, '
     '-65.07807811',
     '  GRINGPOINTSEQUENCENO.1=1, 2, 3, 4',
     '  HDFEOSVersion=HDFEOS_V2.17',
     '  HORIZONTALTILENUMBER=12',
     '  identifier_product_doi=10.5067/MODIS/MOD09Q1.006',
     '  identifier_product_doi_authority=http://dx.doi.org',
     '  INPUTPOINTER=MOD09GQ.A2012337.h12v04.006.20152522.hdf, '
     'MOD09GQ.A2012338.h12v04.006.20152511.hdf, '
     'MOD09GQ.A2012339.h12v04.006.20152512.hdf, '
     'MOD09GQ.A2012340.h12v04.006.20152522.hdf, '
     'MOD09GQ.A2012341.h12v04.006.20152522.hdf, '
     'MOD09GQ.A2012342.h12v04.006.20152522.hdf, '
     'MOD09GQ.A2012343.h12v04.006.20152530.hdf, '
     'MOD09GQ.A2012344.h12v04.006.20152530.hdf, '
     'MOD09GA.A2012337.h12v04.006.20152522.hdf, '
     'MOD09GA.A2012338.h12v04.006.20152511.hdf, '
     'MOD09GA.A2012339.h12v04.006.20152512.hdf, '
     'MOD09GA.A2012340.h12v04.006.20152522.hdf, '
     'MOD09GA.A2012341.h12v04.006.20152522.hdf, '
     'MOD09GA.A2012342.h12v04.006.20152522.hdf, '
     'MOD09GA.A2012343.h12v04.006.20152530.hdf, '
     'MOD09GA.A2012344.h12v04.006.20152530.hdf',
     '  LOCALGRANULEID=MOD09Q1.A2012337.h12v04.006.20152530.hdf',
     '  LOCALVERSIONID=6.0.10',
     '  LONGNAME=MODIS/Terra Surface Reflectance 8-Day L3 Global 250m SIN Grid',
     '  long_name=Surface_reflectance_for_band_1',
     '  NADIRDATARESOLUTION250M=250m',
     '  NADIRDATARESOLUTION500M=500m',
     '  NORTHBOUNDINGCOORDINATE=49.99999999',
     '  NUMBEROFGRANULES=8',
     '  NUMBEROFORBITS=21',
     '  ORBITNUMBER.1=68928',
     '  ORBITNUMBER.10=68973',
     '  ORBITNUMBER.11=68986',
     '  ORBITNUMBER.12=68987',
     '  ORBITNUMBER.13=68988',
     '  ORBITNUMBER.14=69001',
     '  ORBITNUMBER.15=69002',
     '  ORBITNUMBER.16=69003',
     '  ORBITNUMBER.17=69016',
     '  ORBITNUMBER.18=69017',
     '  ORBITNUMBER.19=69030',
     '  ORBITNUMBER.2=68929',
     '  ORBITNUMBER.20=69031',
     '  ORBITNUMBER.21=69032',
     '  ORBITNUMBER.3=68930',
     '  ORBITNUMBER.4=68943',
     '  ORBITNUMBER.5=68944',
     '  ORBITNUMBER.6=68957',
     '  ORBITNUMBER.7=68958',
     '  ORBITNUMBER.8=68959',
     '  ORBITNUMBER.9=68972',
     '  PARAMETERNAME.1=MOD09A1',
     '  PERCENTCLOUDY=0',
     '  PERCENTDIFFERENTORBIT250M=0',
     '  PERCENTLAND=0',
     '  PERCENTLANDSEAMASKCLASS=0, 0, 0, 0, 0, 0, 0, 0',
     '  PERCENTLOWSUN=0',
     '  PERCENTPROCESSED=0',
     '  PERCENTSHADOW=0',
     '  PGEVERSION=6.0.10',
     '  PROCESSINGCENTER=MODAPS',
     '  PROCESSINGENVIRONMENT=Linux minion5684 2.6.18-406.el5 #1 SMP Tue Jun 2 '
     '17:25:57 EDT 2015 x86_64 x86_64 x86_64 GNU/Linux',
     '  PROCESSVERSION=6.0.10',
     '  PRODUCTIONDATETIME=2015-09-10T02:43:47.000Z',
     '  PRODUCTIONHISTORY=PGE21:6.0.10;ProductionHistory not read',
     '  QAPERCENTGOODQUALITY=0',
     '  QAPERCENTINTERPOLATEDDATA.1=0',
     '  QAPERCENTMISSINGDATA.1=0',
     '  QAPERCENTNOTPRODUCEDCLOUD=0',
     '  QAPERCENTNOTPRODUCEDOTHER=0',
     '  QAPERCENTOTHERQUALITY=0',
     '  QAPERCENTOUTOFBOUNDSDATA.1=0',
     '  QAPERCENTPOOROUTPUT250MBAND1=0',
     '  QAPERCENTPOOROUTPUT250MBAND2=0',
     '  QUALITYCLASSPERCENTAGE250MBAND1=0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, '
     '0, 0, 0',
     '  QUALITYCLASSPERCENTAGE250MBAND2=0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, '
     '0, 0, 0',
     '  RANGEBEGINNINGDATE=2012-12-02',
     '  RANGEBEGINNINGTIME=00:00:00.000000',
     '  RANGEENDINGDATE=2012-12-09',
     '  RANGEENDINGTIME=23:59:59.000000',
     '  REPROCESSINGACTUAL=reprocessed',
     '  REPROCESSINGPLANNED=further update is anticipated',
     '  RESOLUTIONBANDS1AND2=250',
     '  scale_factor=0.0001',
     '  scale_factor_err=0',
     '  SCIENCEQUALITYFLAG.1=Not Investigated',
     '  SCIENCEQUALITYFLAGEXPLANATION.1=See '
     'http://landweb.nascom.nasa.gov/cgi-bin/QA_WWW/qaFlagPage.cgi?sat=terra&ver=C5 '
     'for the product Science Quality status.',
     '  SHORTNAME=MOD09Q1',
     '  SOUTHBOUNDINGCOORDINATE=39.99999999',
     '  SPSOPARAMETERS=2015',
     '  SYSTEMFILENAME=MOD09GQ.A2012337.h12v04.006.20152522.hdf, '
     'MOD09GQ.A2012338.h12v04.006.20152511.hdf, '
     'MOD09GQ.A2012339.h12v04.006.20152512.hdf, '
     'MOD09GQ.A2012340.h12v04.006.20152522.hdf, '
     'MOD09GQ.A2012341.h12v04.006.20152522.hdf, '
     'MOD09GQ.A2012342.h12v04.006.20152522.hdf, '
     'MOD09GQ.A2012343.h12v04.006.20152530.hdf, '
     'MOD09GQ.A2012344.h12v04.006.20152530.hdf, '
     'MOD09GA.A2012337.h12v04.006.20152522.hdf, '
     'MOD09GA.A2012338.h12v04.006.20152511.hdf, '
     'MOD09GA.A2012339.h12v04.006.20152512.hdf, '
     'MOD09GA.A2012340.h12v04.006.20152522.hdf, '
     'MOD09GA.A2012341.h12v04.006.20152522.hdf, '
     'MOD09GA.A2012342.h12v04.006.20152522.hdf, '
     'MOD09GA.A2012343.h12v04.006.20152530.hdf, '
     'MOD09GA.A2012344.h12v04.006.20152530.hdf',
     '  TileID=51012004',
     '  units=reflectance',
     '  valid_range=-100, 16000',
     '  VERSION=1.0',
     '  VERSIONID=6',
     '  VERTICALTILENUMBER=4',
     '  WESTBOUNDINGCOORDINATE=-93.34342959',
     '  _FillValue=-28672',
     'Image Structure Metadata:',
     '  INTERLEAVE=BAND',
     'Corner Coordinates:',
     'Upper Left  (-6671703.118, 5559752.598) ( 93d20\'36.35"W, 50d 0\' 0.00"N)',
     'Lower Left  (-6671703.118, 4447802.079) ( 78d19\'27.97"W, 40d 0\' 0.00"N)',
     'Upper Right (-5559752.598, 5559752.598) ( 77d47\'10.29"W, 50d 0\' 0.00"N)',
     'Lower Right (-5559752.598, 4447802.079) ( 65d16\'13.31"W, 40d 0\' 0.00"N)',
     'Center      (-6115727.858, 5003777.339) ( 77d46\'54.29"W, 45d 0\' 0.00"N)',
     'Band 1 Block=4800x1 Type=Int16, ColorInterp=Gray',
     '  Description = ndvi',
     '  Minimum=-32759.000, Maximum=32767.000, Mean=2057.334, StdDev=5450.855',
     '  NoData Value=-32768',
     '  Offset: 0,   Scale:0.0001',
     '  Metadata:',
     '    STATISTICS_MAXIMUM=32767',
     '    STATISTICS_MEAN=2057.33388098',
     '    STATISTICS_MINIMUM=-32759',
     '    STATISTICS_STDDEV=5450.85464292',
     '    STATISTICS_VALID_PERCENT=99.34'])]),

 # t_process[modis-obstime] recording:
 ('obstime',
  [('modis/tiles/h12v04/2012337/h12v04_2012337_MOD-MYD_obstime.tif',
    'raster',
    'gdalinfo-stats',
    ['Driver: GTiff/GeoTIFF',
     'Size is 1200, 1200',
     'Coordinate System is:',
     'PROJCS["unnamed",',
     '    GEOGCS["Unknown datum based upon the custom spheroid",',
     '        DATUM["Not_specified_based_on_custom_spheroid",',
     '            SPHEROID["Custom spheroid",6371007.181,0]],',
     '        PRIMEM["Greenwich",0],',
     '        UNIT["degree",0.01745329]],',
     '    PROJECTION["Sinusoidal"],',
     '    PARAMETER["longitude_of_center",0],',
     '    PARAMETER["false_easting",0],',
     '    PARAMETER["false_northing",0],',
     '    UNIT["metre",1,',
     '        AUTHORITY["EPSG","9001"]]]',
     'Origin = (-6671703.11859900,5559752.59883300)',
     'Pixel Size = (926.62543313,-926.62543313)',
     'Metadata:',
     '  add_offset_err=0',
     '  ALGORITHMPACKAGEACCEPTANCEDATE=102004',
     '  ALGORITHMPACKAGEMATURITYCODE=Normal',
     '  ALGORITHMPACKAGENAME=MOD_PR11A',
     '  ALGORITHMPACKAGEVERSION=6',
     '  AREA_OR_POINT=Area',
     '  ASSOCIATEDINSTRUMENTSHORTNAME.1=MODIS',
     '  ASSOCIATEDPLATFORMSHORTNAME.1=Aqua',
     '  ASSOCIATEDSENSORSHORTNAME.1=MODIS',
     '  AUTOMATICQUALITYFLAG.1=Passed',
     '  AUTOMATICQUALITYFLAGEXPLANATION.1=No automatic quality assessment is '
     'performed in the PGE.',
     '  AVAILABLE_ASSETS=MOD11A1 MYD11A1',
     '  calibrated_nt=5',
     '  CLOUD_CONTAMINATED_LST_SCREENED=YES',
     '  DAYNIGHTFLAG=Both',
     '  DESCRREVISION=6.0',
     '  EASTBOUNDINGCOORDINATE=-65.28378163',
     '  EXCLUSIONGRINGFLAG.1=N',
     '  GIPS_Modis_Version=1.0.0',
     '  '
     'GIPS_Source_Assets=MOD11A1.A2012337.h12v04.006.20161311.hdf,MYD11A1.A2012337.h12v04.006.20161321.hdf',
     '  GIPS_Version=0.0.0-dev',
     '  GRINGPOINTLATITUDE.1=49.99583333, 49.99583333, 40.00416666, 40.00416666',
     '  GRINGPOINTLONGITUDE.1=-93.34989768, -77.79268535, -65.28378163, '
     '-78.33942601',
     '  GRINGPOINTSEQUENCENO.1=1, 2, 3, 4',
     '  HDFEOSVersion=HDFEOS_V2.17',
     '  HORIZONTALTILENUMBER=12',
     '  identifier_product_doi=10.5067/MODIS/MYD11A1.006',
     '  identifier_product_doi_authority=http://dx.doi.org',
     '  INPUTGRANULEPOINTER.1=MYD03.A2012337.0700.006.20123381.hdf',
     '  INPUTGRANULEPOINTER.10=MYD021KM.A2012337.1805.006.20123400.hdf',
     '  INPUTGRANULEPOINTER.11=MYD35_L2.A2012337.1805.006.20140950.hdf',
     '  INPUTGRANULEPOINTER.12=MYD10_L2.A2012337.1805.006.20161171.hdf',
     '  INPUTGRANULEPOINTER.13=MYD07_L2.A2012337.1805.006.20140950.hdf',
     '  INPUTGRANULEPOINTER.14=MYD03.A2012337.1810.006.20123382.hdf',
     '  INPUTGRANULEPOINTER.15=MYD021KM.A2012337.1810.006.20123390.hdf',
     '  INPUTGRANULEPOINTER.16=MYD35_L2.A2012337.1810.006.20140951.hdf',
     '  INPUTGRANULEPOINTER.17=MYD10_L2.A2012337.1810.006.20161171.hdf',
     '  INPUTGRANULEPOINTER.18=MYD07_L2.A2012337.1810.006.20140951.hdf',
     '  INPUTGRANULEPOINTER.19=MYD03.A2012337.1945.006.20123382.hdf',
     '  INPUTGRANULEPOINTER.2=MYD021KM.A2012337.0700.006.20123390.hdf',
     '  INPUTGRANULEPOINTER.20=MYD021KM.A2012337.1945.006.20123390.hdf',
     '  INPUTGRANULEPOINTER.21=MYD35_L2.A2012337.1945.006.20140950.hdf',
     '  INPUTGRANULEPOINTER.22=MYD10_L2.A2012337.1945.006.20161171.hdf',
     '  INPUTGRANULEPOINTER.23=MYD07_L2.A2012337.1945.006.20140950.hdf',
     '  INPUTGRANULEPOINTER.24=MOD35_L2.A2012337.1625.006.20150621.hdf',
     '  INPUTGRANULEPOINTER.25=MOD10_L2.A2012337.1625.006.20161171.hdf',
     '  INPUTGRANULEPOINTER.26=MOD07_L2.A2012337.1625.006.20150621.hdf',
     '  INPUTGRANULEPOINTER.27=MOD03.A2012337.1800.006.20123381.hdf',
     '  INPUTGRANULEPOINTER.28=MOD021KM.A2012337.1800.006.20142250.hdf',
     '  INPUTGRANULEPOINTER.29=MOD35_L2.A2012337.1800.006.20150621.hdf',
     '  INPUTGRANULEPOINTER.3=MYD35_L2.A2012337.0700.006.20140960.hdf',
     '  INPUTGRANULEPOINTER.30=MOD10_L2.A2012337.1800.006.20161171.hdf',
     '  INPUTGRANULEPOINTER.31=MOD07_L2.A2012337.1800.006.20150621.hdf',
     '  INPUTGRANULEPOINTER.4=MYD07_L2.A2012337.0700.006.20141940.hdf',
     '  INPUTGRANULEPOINTER.5=MYD03.A2012337.0835.006.20123381.hdf',
     '  INPUTGRANULEPOINTER.6=MYD021KM.A2012337.0835.006.20123382.hdf',
     '  INPUTGRANULEPOINTER.7=MYD35_L2.A2012337.0835.006.20140950.hdf',
     '  INPUTGRANULEPOINTER.8=MYD07_L2.A2012337.0835.006.20141940.hdf',
     '  INPUTGRANULEPOINTER.9=MYD03.A2012337.1805.006.20123382.hdf',
     '  INPUTPOINTER=MYD03.A2012337.0700.006.20123381.hdf, '
     'MYD021KM.A2012337.0700.006.20123390.hdf, '
     'MYD35_L2.A2012337.0700.006.20140960.hdf, '
     'MYD07_L2.A2012337.0700.006.20141940.hdf, '
     'MYD03.A2012337.0835.006.20123381.hdf, '
     'MYD021KM.A2012337.0835.006.20123382.hdf, '
     'MYD35_L2.A2012337.0835.006.20140950.hdf, '
     'MYD07_L2.A2012337.0835.006.20141940.hdf, '
     'MYD03.A2012337.1805.006.20123382.hdf, '
     'MYD021KM.A2012337.1805.006.20123400.hdf, '
     'MYD35_L2.A2012337.1805.006.20140950.hdf, '
     'MYD10_L2.A2012337.1805.006.20161171.hdf, '
     'MYD07_L2.A2012337.1805.006.20140950.hdf, '
     'MYD03.A2012337.1810.006.20123382.hdf, '
     'MYD021KM.A2012337.1810.006.20123390.hdf, '
     'MYD35_L2.A2012337.1810.006.20140951.hdf, '
     'MYD10_L2.A2012337.1810.006.20161171.hdf, '
     'MYD07_L2.A2012337.1810.006.20140951.hdf, '
     'MYD03.A2012337.1945.006.20123382.hdf, '
     'MYD021KM.A2012337.1945.006.20123390.hdf, '
     'MYD35_L2.A2012337.1945.006.20140950.hdf, '
     'MYD10_L2.A2012337.1945.006.20161171.hdf, '
     'MYD07_L2.A2012337.1945.006.20140950.hdf',
     '  INPUTTILEPOINTER.1=MCDLC1KM.A2010001.h12v04.051.20133400.hdf',
     '  INPUTTILEPOINTER.2=MCD43A1.A2012337.h12v04.006.20161120.hdf',
     '  INPUTTILEPOINTER.3=MYD11A1.6.A2012337.h12v04.hdf',
     '  INPUTTILEPOINTER.4=MYD11B1.6.A2012337.h12v04.hdf',
     '  INPUTTILEPOINTER.5=MYD11UPD.A2-1.6.update_for_lst.h12v04.hdf',
     '  INSTRUMENTNAME=Moderate-Resolution Imaging SpectroRadiometer',
     '  LOCALGRANULEID=MYD11A1.A2012337.h12v04.006.20161321.hdf',
     '  LOCALINPUTGRANULEID=0700,0835,1805,1810,1945',
     '  LOCALVERSIONID=6.4.4AS',
     '  LONGNAME=MODIS/Aqua Land Surface Temperature/Emissivity Daily L3 Global '
     '1km SIN Grid',
     '  long_name=Time of nighttime Land-surface Temperature observation',
     '  LOOKUPTABLEPOINTER.1=band_emis.h',
     '  LOOKUPTABLEPOINTER.2=lst_coef.h',
     '  LOOKUPTABLETYPE.1=Land-cover based band emissivity database',
     '  LOOKUPTABLETYPE.2=the generalized split-window LST coefficients',
     '  NORTHBOUNDINGCOORDINATE=49.99583333',
     '  Number Type=uint8',
     '  N_GRAN_POINTERS=23',
     '  PARAMETERNAME.1=MOD 1KM L3 LST',
     '  PGEVERSION=6.4.14',
     '  PROCESSINGCENTER=MODAPS',
     '  PROCESSINGDATETIME=2016-05-11T10:02:08.000Z',
     '  PROCESSINGENVIRONMENT=Linux minion5631 2.6.18-407.el5 #1 SMP Wed Nov 11 '
     '08:12:41 EST 2015 x86_64 x86_64 x86_64 GNU/Linux',
     '  PRODUCTIONDATETIME=2016-05-11T10:18:31.000Z',
     '  QAFRACTIONGOODQUALITY=0.0013476',
     '  QAFRACTIONNOTPRODUCEDCLOUD=0.8552590',
     '  QAFRACTIONNOTPRODUCEDOTHER=0.1269437',
     '  QAFRACTIONOTHERQUALITY=0.0164497',
     '  QAPERCENTCLOUDCOVER.1=86',
     '  QAPERCENTGOODQUALITY=0',
     '  QAPERCENTINTERPOLATEDDATA.1=0',
     '  QAPERCENTMISSINGDATA.1=0',
     '  QAPERCENTNOTPRODUCEDCLOUD=86',
     '  QAPERCENTNOTPRODUCEDOTHER=13',
     '  QAPERCENTOTHERQUALITY=2',
     '  QAPERCENTOUTOFBOUNDSDATA.1=0',
     '  RANGEBEGINNINGDATE=2012-12-02',
     '  RANGEBEGINNINGTIME=00:00:00',
     '  RANGEENDINGDATE=2012-12-02',
     '  RANGEENDINGTIME=23:59:59',
     '  REPROCESSINGACTUAL=reprocessed',
     '  REPROCESSINGPLANNED=further update is anticipated',
     '  scale_factor=0.1',
     '  scale_factor_err=0',
     '  SCIENCEQUALITYFLAG.1=Not Investigated',
     '  SCIENCEQUALITYFLAGEXPLANATION.1=See '
     'http://landweb.nascom.nasa.gov/cgi-bin/QA_WWW/qaFlagPage.cgi?sat=aqua for '
     'the product Science Quality status.',
     '  SHORTNAME=MYD11A1',
     '  SOUTHBOUNDINGCOORDINATE=40.00416666',
     '  SPSOPARAMETERS=2484 and 3323',
     '  TileID=51012004',
     '  units=hrs',
     '  valid_range=0, 240',
     '  VERSION=1',
     '  VERSIONID=6',
     '  VERTICALTILENUMBER=04',
     '  View_time=View_time data * scale_factor',
     '  WESTBOUNDINGCOORDINATE=-93.34989768',
     '  _FillValue=255',
     'Image Structure Metadata:',
     '  INTERLEAVE=PIXEL',
     'Corner Coordinates:',
     'Upper Left  (-6671703.119, 5559752.599) ( 93d20\'36.35"W, 50d 0\' 0.00"N)',
     'Lower Left  (-6671703.119, 4447802.079) ( 78d19\'27.97"W, 40d 0\' 0.00"N)',
     'Upper Right (-5559752.599, 5559752.599) ( 77d47\'10.29"W, 50d 0\' 0.00"N)',
     'Lower Right (-5559752.599, 4447802.079) ( 65d16\'13.31"W, 40d 0\' 0.00"N)',
     'Center      (-6115727.859, 5003777.339) ( 77d46\'54.29"W, 45d 0\' 0.00"N)',
     'Band 1 Block=1200x1 Type=Byte, ColorInterp=Red',
     '  Description = Observation Time Daytime Terra',
     '  Minimum=255.000, Maximum=255.000, Mean=255.000, StdDev=0.000',
     '  NoData Value=0',
     '  Offset: 0,   Scale:0.1',
     '  Metadata:',
     '    STATISTICS_MAXIMUM=255',
     '    STATISTICS_MEAN=255',
     '    STATISTICS_MINIMUM=255',
     '    STATISTICS_STDDEV=0',
     '    STATISTICS_VALID_PERCENT=1.171',
     'Band 2 Block=1200x1 Type=Byte, ColorInterp=Green',
     '  Description = Observation Time Nighttime Terra',
     '  Minimum=255.000, Maximum=255.000, Mean=255.000, StdDev=0.000',
     '  NoData Value=0',
     '  Offset: 0,   Scale:0.1',
     '  Metadata:',
     '    STATISTICS_MAXIMUM=255',
     '    STATISTICS_MEAN=255',
     '    STATISTICS_MINIMUM=255',
     '    STATISTICS_STDDEV=0',
     '    STATISTICS_VALID_PERCENT=3.791',
     'Band 3 Block=1200x1 Type=Byte, ColorInterp=Blue',
     '  Description = Observation Time Daytime Aqua',
     '  Minimum=255.000, Maximum=255.000, Mean=255.000, StdDev=0.000',
     '  NoData Value=0',
     '  Offset: 0,   Scale:0.1',
     '  Metadata:',
     '    STATISTICS_MAXIMUM=255',
     '    STATISTICS_MEAN=255',
     '    STATISTICS_MINIMUM=255',
     '    STATISTICS_STDDEV=0',
     '    STATISTICS_VALID_PERCENT=0.6742',
     'Band 4 Block=1200x1 Type=Byte, ColorInterp=Alpha',
     '  Description = Observation Time Nighttime Aqua',
     '  Minimum=10.000, Maximum=255.000, Mean=211.683, StdDev=58.782',
     '  NoData Value=0',
     '  Offset: 0,   Scale:0.1',
     '  Metadata:',
     '    STATISTICS_MAXIMUM=255',
     '    STATISTICS_MEAN=211.68345358',
     '    STATISTICS_MINIMUM=10',
     '    STATISTICS_STDDEV=58.78161431',
     '    STATISTICS_VALID_PERCENT=2.868'])]),

 # t_process[modis-quality] recording:
 ('quality',
  [('modis/tiles/h12v04/2012337/h12v04_2012337_MCD_quality.tif',
    'raster',
    'gdalinfo-stats',
    ['Driver: GTiff/GeoTIFF',
     'Size is 2400, 2400',
     'Coordinate System is:',
     'PROJCS["unnamed",',
     '    GEOGCS["Unknown datum based upon the custom spheroid",',
     '        DATUM["Not_specified_based_on_custom_spheroid",',
     '            SPHEROID["Custom spheroid",6371007.181,0]],',
     '        PRIMEM["Greenwich",0],',
     '        UNIT["degree",0.01745329]],',
     '    PROJECTION["Sinusoidal"],',
     '    PARAMETER["longitude_of_center",0],',
     '    PARAMETER["false_easting",0],',
     '    PARAMETER["false_northing",0],',
     '    UNIT["metre",1,',
     '        AUTHORITY["EPSG","9001"]]]',
     'Origin = (-6671703.11799999,5559752.59833300)',
     'Pixel Size = (463.31271652,-463.31271652)',
     'Metadata:',
     '  ALBEDOFILEID=06121997',
     '  AREA_OR_POINT=Area',
     '  ASSOCIATEDINSTRUMENTSHORTNAME.1=MODIS',
     '  ASSOCIATEDINSTRUMENTSHORTNAME.2=MODIS',
     '  ASSOCIATEDPLATFORMSHORTNAME.1=Terra',
     '  ASSOCIATEDPLATFORMSHORTNAME.2=Aqua',
     '  ASSOCIATEDSENSORSHORTNAME.1=MODIS',
     '  ASSOCIATEDSENSORSHORTNAME.2=MODIS',
     '  AUTOMATICQUALITYFLAG.1=Passed',
     '  AUTOMATICQUALITYFLAGEXPLANATION.1=Passed was set as a default value. '
     'More algorithm will be developed',
     '  AVAILABLE_ASSETS=MCD43A2',
     '  AVERAGENUMBEROBS=1',
     '  BRDFCODEID=AMBRALS_V4.0R1',
     '  BRDFDATABASEVERSION=v1.0500m',
     '  CHARACTERISTICBINANGULARSIZE=15.0',
     '  CHARACTERISTICBINSIZE=463.31271652',
     '  COVERAGECALCULATIONMETHOD=volume',
     '  DATACOLUMNS=2400',
     '  DATAROWS=2400',
     '  DAYNIGHTFLAG=Day',
     '  Description=Band Quality:',
     '  0 = best quality, full inversion (WoDs, RMSE majority good)',
     '  1 = good quality, full inversion',
     '  2 = Magnitude inversion (numobs >= 7)',
     '  3 = Magnitude inversion (numobs >= 2 & < 7)',
     '  4 = Fill value',
     '',
     '  DESCRREVISION=6.1',
     '  EASTBOUNDINGCOORDINATE=-65.25948606',
     '  EXCLUSIONGRINGFLAG.1=N',
     '  GEOANYABNORMAL=False',
     '  GEOESTMAXRMSERROR=75.0',
     '  GIPS_Modis_Version=1.0.0',
     '  GIPS_Source_Assets=MCD43A2.A2012337.h12v04.006.20161120.hdf',
     '  GIPS_Version=0.0.0-dev',
     '  GLOBALGRIDCOLUMNS=86400',
     '  GLOBALGRIDROWS=43200',
     '  GRINGPOINTLATITUDE.1=39.78578782, 49.99719181, 50.07541801, 39.84112776',
     '  GRINGPOINTLONGITUDE.1=-78.20833299, -93.38216574, -77.75056839, '
     '-65.07807811',
     '  GRINGPOINTSEQUENCENO.1=1, 2, 3, 4',
     '  HDFEOSVersion=HDFEOS_V2.17',
     '  HORIZONTALTILENUMBER=12',
     '  identifier_product_doi=10.5067/MODIS/MCD43A2.006',
     '  identifier_product_doi_authority=http://dx.doi.org',
     '  INPUTPOINTER=MYD09GA.A2012329.h12v04.006.20152510.hdf, '
     'MYD09GA.A2012330.h12v04.006.20152511.hdf, '
     'MYD09GA.A2012331.h12v04.006.20152511.hdf, '
     'MYD09GA.A2012332.h12v04.006.20152511.hdf, '
     'MYD09GA.A2012333.h12v04.006.20152521.hdf, '
     'MYD09GA.A2012334.h12v04.006.20152521.hdf, '
     'MYD09GA.A2012335.h12v04.006.20152521.hdf, '
     'MYD09GA.A2012336.h12v04.006.20152522.hdf, '
     'MYD09GA.A2012337.h12v04.006.20152521.hdf, '
     'MYD09GA.A2012338.h12v04.006.20152511.hdf, '
     'MYD09GA.A2012339.h12v04.006.20152521.hdf, '
     'MYD09GA.A2012340.h12v04.006.20152521.hdf, '
     'MYD09GA.A2012341.h12v04.006.20152521.hdf, '
     'MYD09GA.A2012342.h12v04.006.20152522.hdf, '
     'MYD09GA.A2012343.h12v04.006.20152522.hdf, '
     'MYD09GA.A2012344.h12v04.006.20152522.hdf, '
     'MOD09GA.A2012329.h12v04.006.20152511.hdf, '
     'MOD09GA.A2012330.h12v04.006.20152510.hdf, '
     'MOD09GA.A2012331.h12v04.006.20152511.hdf, '
     'MOD09GA.A2012332.h12v04.006.20152512.hdf, '
     'MOD09GA.A2012333.h12v04.006.20152521.hdf, '
     'MOD09GA.A2012334.h12v04.006.20152522.hdf, '
     'MOD09GA.A2012335.h12v04.006.20152522.hdf, '
     'MOD09GA.A2012336.h12v04.006.20152522.hdf, '
     'MOD09GA.A2012337.h12v04.006.20152522.hdf, '
     'MOD09GA.A2012338.h12v04.006.20152511.hdf, '
     'MOD09GA.A2012339.h12v04.006.20152512.hdf, '
     'MOD09GA.A2012340.h12v04.006.20152522.hdf, '
     'MOD09GA.A2012341.h12v04.006.20152522.hdf, '
     'MOD09GA.A2012342.h12v04.006.20152522.hdf, '
     'MOD09GA.A2012343.h12v04.006.20152530.hdf, '
     'MOD09GA.A2012344.h12v04.006.20152530.hdf, MCD43DB.A2012336.6.h12v04.hdf',
     '  LOCALGRANULEID=MCD43A2.A2012337.h12v04.006.20161120.hdf',
     '  LOCALVERSIONID=6.1.34',
     '  LONGNAME=MODIS/Terra+Aqua BRDF/Albedo Quality Daily L3 Global - 500m',
     '  long_name=BRDF_Albedo_Band_Quality_Band6',
     '  MAXIMUMOBSERVATIONS=0',
     '  NADIRDATARESOLUTION=500m',
     '  NORTHBOUNDINGCOORDINATE=49.99999999',
     '  NUMBEROFGRANULES=1',
     '  PARAMETERNAME.1=NOT SET',
     '  PERCENTLANDINTILE=35',
     '  PERCENTNEWBRDFS=0',
     '  PERCENTPROCESSEDINTILE=41',
     '  PERCENTSHAPEFIXEDBRDFS=99',
     '  PERCENTSUBSTITUTEBRDFS=0',
     '  PGEVERSION=6.0.34',
     '  PROCESSINGCENTER=MODAPS',
     '  PROCESSINGENVIRONMENT=Linux minion5709 2.6.18-408.el5 #1 SMP Tue Jan 19 '
     '09:14:52 EST 2016 x86_64 x86_64 x86_64 GNU/Linux',
     '  PRODUCTIONDATETIME=2016-04-21T01:37:42.000Z',
     '  QAPERCENTGOODQUALITY=0',
     '  QAPERCENTNOTPRODUCEDCLOUD=36',
     '  QAPERCENTNOTPRODUCEDOTHER=25',
     '  QAPERCENTOTHERQUALITY=38',
     '  RANGEBEGINNINGDATE=2012-11-24',
     '  RANGEBEGINNINGTIME=00:00:00.000000',
     '  RANGEENDINGDATE=2012-12-10',
     '  RANGEENDINGTIME=23:59:59.999999',
     '  REPROCESSINGACTUAL=reprocessed',
     '  REPROCESSINGPLANNED=further update is anticipated',
     '  SCIENCEQUALITYFLAG.1=Not Investigated',
     '  SCIENCEQUALITYFLAGEXPLANATION.1=See '
     'http://landweb.nascom/nasa.gov/cgi-bin/QA_WWW/qaFlagPage.cgi?sat=aqua the '
     'product Science Quality status.',
     '  SETUPFILEID=06121997',
     '  SHORTNAME=MCD43A2',
     '  SOUTHBOUNDINGCOORDINATE=39.99999999',
     '  SPSOPARAMETERS=2015',
     '  TileID=51012004',
     '  units=concatenated flags',
     '  valid_range=0, 254',
     '  VERSIONID=6',
     '  VERTICALTILENUMBER=4',
     '  WESTBOUNDINGCOORDINATE=-93.34342959',
     '  _FillValue=255',
     'Image Structure Metadata:',
     '  INTERLEAVE=PIXEL',
     'Corner Coordinates:',
     'Upper Left  (-6671703.118, 5559752.598) ( 93d20\'36.35"W, 50d 0\' 0.00"N)',
     'Lower Left  (-6671703.118, 4447802.079) ( 78d19\'27.97"W, 40d 0\' 0.00"N)',
     'Upper Right (-5559752.598, 5559752.598) ( 77d47\'10.29"W, 50d 0\' 0.00"N)',
     'Lower Right (-5559752.598, 4447802.079) ( 65d16\'13.31"W, 40d 0\' 0.00"N)',
     'Center      (-6115727.858, 5003777.339) ( 77d46\'54.29"W, 45d 0\' 0.00"N)',
     'Band 1 Block=2400x1 Type=Byte, ColorInterp=Gray',
     '  Description = QC BLUE',
     '  Minimum=0.000, Maximum=3.000, Mean=2.939, StdDev=0.314',
     '  NoData Value=255',
     '  Metadata:',
     '    STATISTICS_MAXIMUM=3',
     '    STATISTICS_MEAN=2.93941546',
     '    STATISTICS_MINIMUM=0',
     '    STATISTICS_STDDEV=0.31354263',
     '    STATISTICS_VALID_PERCENT=46.02',
     'Band 2 Block=2400x1 Type=Byte, ColorInterp=Undefined',
     '  Description = QC GREEN',
     '  Minimum=0.000, Maximum=3.000, Mean=2.925, StdDev=0.349',
     '  NoData Value=255',
     '  Metadata:',
     '    STATISTICS_MAXIMUM=3',
     '    STATISTICS_MEAN=2.92461509',
     '    STATISTICS_MINIMUM=0',
     '    STATISTICS_STDDEV=0.34871705',
     '    STATISTICS_VALID_PERCENT=46.33',
     'Band 3 Block=2400x1 Type=Byte, ColorInterp=Undefined',
     '  Description = QC RED',
     '  Minimum=0.000, Maximum=3.000, Mean=2.929, StdDev=0.342',
     '  NoData Value=255',
     '  Metadata:',
     '    STATISTICS_MAXIMUM=3',
     '    STATISTICS_MEAN=2.92894661',
     '    STATISTICS_MINIMUM=0',
     '    STATISTICS_STDDEV=0.34217250',
     '    STATISTICS_VALID_PERCENT=45.56',
     'Band 4 Block=2400x1 Type=Byte, ColorInterp=Undefined',
     '  Description = QC NIR',
     '  Minimum=0.000, Maximum=3.000, Mean=2.919, StdDev=0.364',
     '  NoData Value=255',
     '  Metadata:',
     '    STATISTICS_MAXIMUM=3',
     '    STATISTICS_MEAN=2.91912871',
     '    STATISTICS_MINIMUM=0',
     '    STATISTICS_STDDEV=0.36408043',
     '    STATISTICS_VALID_PERCENT=39.71',
     'Band 5 Block=2400x1 Type=Byte, ColorInterp=Undefined',
     '  Description = QC SWIR1',
     '  Minimum=0.000, Maximum=3.000, Mean=2.931, StdDev=0.338',
     '  NoData Value=255',
     '  Metadata:',
     '    STATISTICS_MAXIMUM=3',
     '    STATISTICS_MEAN=2.93058605',
     '    STATISTICS_MINIMUM=0',
     '    STATISTICS_STDDEV=0.33808624',
     '    STATISTICS_VALID_PERCENT=42.39',
     'Band 6 Block=2400x1 Type=Byte, ColorInterp=Undefined',
     '  Description = QC SWIR2',
     '  Minimum=0.000, Maximum=3.000, Mean=2.982, StdDev=0.166',
     '  NoData Value=255',
     '  Metadata:',
     '    STATISTICS_MAXIMUM=3',
     '    STATISTICS_MEAN=2.98205059',
     '    STATISTICS_MINIMUM=0',
     '    STATISTICS_STDDEV=0.16600311',
     '    STATISTICS_VALID_PERCENT=31.81'])]),

 # t_process[modis-satvi] recording:
 ('satvi',
  [('modis/tiles/h12v04/2012337/h12v04_2012337_MCD_satvi.tif',
    'raster',
    'gdalinfo-stats',
    ['Driver: GTiff/GeoTIFF',
     'Size is 2400, 2400',
     'Coordinate System is:',
     'PROJCS["unnamed",',
     '    GEOGCS["Unknown datum based upon the custom spheroid",',
     '        DATUM["Not_specified_based_on_custom_spheroid",',
     '            SPHEROID["Custom spheroid",6371007.181,0]],',
     '        PRIMEM["Greenwich",0],',
     '        UNIT["degree",0.01745329]],',
     '    PROJECTION["Sinusoidal"],',
     '    PARAMETER["longitude_of_center",0],',
     '    PARAMETER["false_easting",0],',
     '    PARAMETER["false_northing",0],',
     '    UNIT["metre",1,',
     '        AUTHORITY["EPSG","9001"]]]',
     'Origin = (-6671703.11799999,5559752.59833300)',
     'Pixel Size = (463.31271652,-463.31271652)',
     'Metadata:',
     '  add_offset=0',
     '  add_offset_err=0',
     '  ALBEDOFILEID=06121997',
     '  AREA_OR_POINT=Area',
     '  ASSOCIATEDINSTRUMENTSHORTNAME.1=MODIS',
     '  ASSOCIATEDINSTRUMENTSHORTNAME.2=MODIS',
     '  ASSOCIATEDPLATFORMSHORTNAME.1=Terra',
     '  ASSOCIATEDPLATFORMSHORTNAME.2=Aqua',
     '  ASSOCIATEDSENSORSHORTNAME.1=MODIS',
     '  ASSOCIATEDSENSORSHORTNAME.2=MODIS',
     '  AUTOMATICQUALITYFLAG.1=Passed',
     '  AUTOMATICQUALITYFLAGEXPLANATION.1=Passed was set as a default value. '
     'More algorithm will be developed',
     '  AVERAGENUMBEROBS=1',
     '  BRDFCODEID=AMBRALS_V4.0R1',
     '  BRDFDATABASEVERSION=v1.0500m',
     '  calibrated_nt=5',
     '  CHARACTERISTICBINANGULARSIZE=15.0',
     '  CHARACTERISTICBINSIZE=463.31271652',
     '  COVERAGECALCULATIONMETHOD=volume',
     '  DATACOLUMNS=2400',
     '  DATAROWS=2400',
     '  DAYNIGHTFLAG=Day',
     '  DESCRREVISION=6.1',
     '  EASTBOUNDINGCOORDINATE=-65.25948606',
     '  EXCLUSIONGRINGFLAG.1=N',
     '  GEOANYABNORMAL=False',
     '  GEOESTMAXRMSERROR=75.0',
     '  GIPS_Modis_Version=1.0.0',
     '  GIPS_Source_Assets=MCD43A4.A2012337.h12v04.006.20161120.hdf',
     '  GIPS_Version=0.0.0-dev',
     '  GLOBALGRIDCOLUMNS=86400',
     '  GLOBALGRIDROWS=43200',
     '  GRINGPOINTLATITUDE.1=39.78578782, 49.99719181, 50.07541801, 39.84112776',
     '  GRINGPOINTLONGITUDE.1=-78.20833299, -93.38216574, -77.75056839, '
     '-65.07807811',
     '  GRINGPOINTSEQUENCENO.1=1, 2, 3, 4',
     '  HDFEOSVersion=HDFEOS_V2.17',
     '  HORIZONTALTILENUMBER=12',
     '  identifier_product_doi=10.5067/MODIS/MCD43A4.006',
     '  identifier_product_doi_authority=http://dx.doi.org',
     '  INPUTPOINTER=MYD09GA.A2012329.h12v04.006.20152510.hdf, '
     'MYD09GA.A2012330.h12v04.006.20152511.hdf, '
     'MYD09GA.A2012331.h12v04.006.20152511.hdf, '
     'MYD09GA.A2012332.h12v04.006.20152511.hdf, '
     'MYD09GA.A2012333.h12v04.006.20152521.hdf, '
     'MYD09GA.A2012334.h12v04.006.20152521.hdf, '
     'MYD09GA.A2012335.h12v04.006.20152521.hdf, '
     'MYD09GA.A2012336.h12v04.006.20152522.hdf, '
     'MYD09GA.A2012337.h12v04.006.20152521.hdf, '
     'MYD09GA.A2012338.h12v04.006.20152511.hdf, '
     'MYD09GA.A2012339.h12v04.006.20152521.hdf, '
     'MYD09GA.A2012340.h12v04.006.20152521.hdf, '
     'MYD09GA.A2012341.h12v04.006.20152521.hdf, '
     'MYD09GA.A2012342.h12v04.006.20152522.hdf, '
     'MYD09GA.A2012343.h12v04.006.20152522.hdf, '
     'MYD09GA.A2012344.h12v04.006.20152522.hdf, '
     'MOD09GA.A2012329.h12v04.006.20152511.hdf, '
     'MOD09GA.A2012330.h12v04.006.20152510.hdf, '
     'MOD09GA.A2012331.h12v04.006.20152511.hdf, '
     'MOD09GA.A2012332.h12v04.006.20152512.hdf, '
     'MOD09GA.A2012333.h12v04.006.20152521.hdf, '
     'MOD09GA.A2012334.h12v04.006.20152522.hdf, '
     'MOD09GA.A2012335.h12v04.006.20152522.hdf, '
     'MOD09GA.A2012336.h12v04.006.20152522.hdf, '
     'MOD09GA.A2012337.h12v04.006.20152522.hdf, '
     'MOD09GA.A2012338.h12v04.006.20152511.hdf, '
     'MOD09GA.A2012339.h12v04.006.20152512.hdf, '
     'MOD09GA.A2012340.h12v04.006.20152522.hdf, '
     'MOD09GA.A2012341.h12v04.006.20152522.hdf, '
     'MOD09GA.A2012342.h12v04.006.20152522.hdf, '
     'MOD09GA.A2012343.h12v04.006.20152530.hdf, '
     'MOD09GA.A2012344.h12v04.006.20152530.hdf, MCD43DB.A2012336.6.h12v04.hdf',
     '  LOCALGRANULEID=MCD43A4.A2012337.h12v04.006.20161120.hdf',
     '  LOCALVERSIONID=6.1.34',
     '  LONGNAME=MODIS/Terra+Aqua BRDF/Albedo Nadir BRDF-Adjusted Ref Daily L3 '
     'Global - 500m',
     '  long_name=Nadir_Reflectance_Band1',
     '  MAXIMUMOBSERVATIONS=0',
     '  NADIRDATARESOLUTION=500m',
     '  NORTHBOUNDINGCOORDINATE=49.99999999',
     '  NUMBEROFGRANULES=1',
     '  PARAMETERNAME.1=NOT SET',
     '  PERCENTLANDINTILE=35',
     '  PERCENTNEWBRDFS=0',
     '  PERCENTPROCESSEDINTILE=41',
     '  PERCENTSHAPEFIXEDBRDFS=99',
     '  PERCENTSUBSTITUTEBRDFS=0',
     '  PGEVERSION=6.0.34',
     '  PROCESSINGCENTER=MODAPS',
     '  PROCESSINGENVIRONMENT=Linux minion5709 2.6.18-408.el5 #1 SMP Tue Jan 19 '
     '09:14:52 EST 2016 x86_64 x86_64 x86_64 GNU/Linux',
     '  PRODUCTIONDATETIME=2016-04-21T01:37:46.000Z',
     '  QAPERCENTGOODQUALITY=0',
     '  QAPERCENTNOTPRODUCEDCLOUD=36',
     '  QAPERCENTNOTPRODUCEDOTHER=25',
     '  QAPERCENTOTHERQUALITY=38',
     '  RANGEBEGINNINGDATE=2012-11-24',
     '  RANGEBEGINNINGTIME=00:00:00.000000',
     '  RANGEENDINGDATE=2012-12-10',
     '  RANGEENDINGTIME=23:59:59.999999',
     '  REPROCESSINGACTUAL=reprocessed',
     '  REPROCESSINGPLANNED=further update is anticipated',
     '  scale_factor=0.0001',
     '  scale_factor_err=0',
     '  SCIENCEQUALITYFLAG.1=Not Investigated',
     '  SCIENCEQUALITYFLAGEXPLANATION.1=See '
     'http://landweb.nascom/nasa.gov/cgi-bin/QA_WWW/qaFlagPage.cgi?sat=aqua the '
     'product Science Quality status.',
     '  SETUPFILEID=06121997',
     '  SHORTNAME=MCD43A4',
     '  SOUTHBOUNDINGCOORDINATE=39.99999999',
     '  SPSOPARAMETERS=2015',
     '  TileID=51012004',
     '  units=reflectance, no units',
     '  valid_range=0, 32767',
     '  VERSION=1.0',
     '  VERSIONID=6',
     '  VERTICALTILENUMBER=4',
     '  WESTBOUNDINGCOORDINATE=-93.34342959',
     '  _FillValue=32767',
     'Image Structure Metadata:',
     '  INTERLEAVE=BAND',
     'Corner Coordinates:',
     'Upper Left  (-6671703.118, 5559752.598) ( 93d20\'36.35"W, 50d 0\' 0.00"N)',
     'Lower Left  (-6671703.118, 4447802.079) ( 78d19\'27.97"W, 40d 0\' 0.00"N)',
     'Upper Right (-5559752.598, 5559752.598) ( 77d47\'10.29"W, 50d 0\' 0.00"N)',
     'Lower Right (-5559752.598, 4447802.079) ( 65d16\'13.31"W, 40d 0\' 0.00"N)',
     'Center      (-6115727.858, 5003777.339) ( 77d46\'54.29"W, 45d 0\' 0.00"N)',
     'Band 1 Block=2400x1 Type=Int16, ColorInterp=Gray',
     '  Description = satvi',
     '  Minimum=-8109.000, Maximum=6542.000, Mean=454.838, StdDev=1826.878',
     '  NoData Value=-32768',
     '  Offset: 0,   Scale:0.0001',
     '  Metadata:',
     '    STATISTICS_MAXIMUM=6542',
     '    STATISTICS_MEAN=454.83789743',
     '    STATISTICS_MINIMUM=-8109',
     '    STATISTICS_STDDEV=1826.87825982',
     '    STATISTICS_VALID_PERCENT=31.01'])]),

 # t_process[modis-sti] recording:
 ('sti',
  [('modis/tiles/h12v04/2012337/h12v04_2012337_MCD_sti.tif',
    'raster',
    'gdalinfo-stats',
    ['Driver: GTiff/GeoTIFF',
     'Size is 2400, 2400',
     'Coordinate System is:',
     'PROJCS["unnamed",',
     '    GEOGCS["Unknown datum based upon the custom spheroid",',
     '        DATUM["Not_specified_based_on_custom_spheroid",',
     '            SPHEROID["Custom spheroid",6371007.181,0]],',
     '        PRIMEM["Greenwich",0],',
     '        UNIT["degree",0.01745329]],',
     '    PROJECTION["Sinusoidal"],',
     '    PARAMETER["longitude_of_center",0],',
     '    PARAMETER["false_easting",0],',
     '    PARAMETER["false_northing",0],',
     '    UNIT["metre",1,',
     '        AUTHORITY["EPSG","9001"]]]',
     'Origin = (-6671703.11799999,5559752.59833300)',
     'Pixel Size = (463.31271652,-463.31271652)',
     'Metadata:',
     '  add_offset=0',
     '  add_offset_err=0',
     '  ALBEDOFILEID=06121997',
     '  AREA_OR_POINT=Area',
     '  ASSOCIATEDINSTRUMENTSHORTNAME.1=MODIS',
     '  ASSOCIATEDINSTRUMENTSHORTNAME.2=MODIS',
     '  ASSOCIATEDPLATFORMSHORTNAME.1=Terra',
     '  ASSOCIATEDPLATFORMSHORTNAME.2=Aqua',
     '  ASSOCIATEDSENSORSHORTNAME.1=MODIS',
     '  ASSOCIATEDSENSORSHORTNAME.2=MODIS',
     '  AUTOMATICQUALITYFLAG.1=Passed',
     '  AUTOMATICQUALITYFLAGEXPLANATION.1=Passed was set as a default value. '
     'More algorithm will be developed',
     '  AVERAGENUMBEROBS=1',
     '  BRDFCODEID=AMBRALS_V4.0R1',
     '  BRDFDATABASEVERSION=v1.0500m',
     '  calibrated_nt=5',
     '  CHARACTERISTICBINANGULARSIZE=15.0',
     '  CHARACTERISTICBINSIZE=463.31271652',
     '  COVERAGECALCULATIONMETHOD=volume',
     '  DATACOLUMNS=2400',
     '  DATAROWS=2400',
     '  DAYNIGHTFLAG=Day',
     '  DESCRREVISION=6.1',
     '  EASTBOUNDINGCOORDINATE=-65.25948606',
     '  EXCLUSIONGRINGFLAG.1=N',
     '  GEOANYABNORMAL=False',
     '  GEOESTMAXRMSERROR=75.0',
     '  GIPS_Modis_Version=1.0.0',
     '  GIPS_Source_Assets=MCD43A4.A2012337.h12v04.006.20161120.hdf',
     '  GIPS_Version=0.0.0-dev',
     '  GLOBALGRIDCOLUMNS=86400',
     '  GLOBALGRIDROWS=43200',
     '  GRINGPOINTLATITUDE.1=39.78578782, 49.99719181, 50.07541801, 39.84112776',
     '  GRINGPOINTLONGITUDE.1=-78.20833299, -93.38216574, -77.75056839, '
     '-65.07807811',
     '  GRINGPOINTSEQUENCENO.1=1, 2, 3, 4',
     '  HDFEOSVersion=HDFEOS_V2.17',
     '  HORIZONTALTILENUMBER=12',
     '  identifier_product_doi=10.5067/MODIS/MCD43A4.006',
     '  identifier_product_doi_authority=http://dx.doi.org',
     '  INPUTPOINTER=MYD09GA.A2012329.h12v04.006.20152510.hdf, '
     'MYD09GA.A2012330.h12v04.006.20152511.hdf, '
     'MYD09GA.A2012331.h12v04.006.20152511.hdf, '
     'MYD09GA.A2012332.h12v04.006.20152511.hdf, '
     'MYD09GA.A2012333.h12v04.006.20152521.hdf, '
     'MYD09GA.A2012334.h12v04.006.20152521.hdf, '
     'MYD09GA.A2012335.h12v04.006.20152521.hdf, '
     'MYD09GA.A2012336.h12v04.006.20152522.hdf, '
     'MYD09GA.A2012337.h12v04.006.20152521.hdf, '
     'MYD09GA.A2012338.h12v04.006.20152511.hdf, '
     'MYD09GA.A2012339.h12v04.006.20152521.hdf, '
     'MYD09GA.A2012340.h12v04.006.20152521.hdf, '
     'MYD09GA.A2012341.h12v04.006.20152521.hdf, '
     'MYD09GA.A2012342.h12v04.006.20152522.hdf, '
     'MYD09GA.A2012343.h12v04.006.20152522.hdf, '
     'MYD09GA.A2012344.h12v04.006.20152522.hdf, '
     'MOD09GA.A2012329.h12v04.006.20152511.hdf, '
     'MOD09GA.A2012330.h12v04.006.20152510.hdf, '
     'MOD09GA.A2012331.h12v04.006.20152511.hdf, '
     'MOD09GA.A2012332.h12v04.006.20152512.hdf, '
     'MOD09GA.A2012333.h12v04.006.20152521.hdf, '
     'MOD09GA.A2012334.h12v04.006.20152522.hdf, '
     'MOD09GA.A2012335.h12v04.006.20152522.hdf, '
     'MOD09GA.A2012336.h12v04.006.20152522.hdf, '
     'MOD09GA.A2012337.h12v04.006.20152522.hdf, '
     'MOD09GA.A2012338.h12v04.006.20152511.hdf, '
     'MOD09GA.A2012339.h12v04.006.20152512.hdf, '
     'MOD09GA.A2012340.h12v04.006.20152522.hdf, '
     'MOD09GA.A2012341.h12v04.006.20152522.hdf, '
     'MOD09GA.A2012342.h12v04.006.20152522.hdf, '
     'MOD09GA.A2012343.h12v04.006.20152530.hdf, '
     'MOD09GA.A2012344.h12v04.006.20152530.hdf, MCD43DB.A2012336.6.h12v04.hdf',
     '  LOCALGRANULEID=MCD43A4.A2012337.h12v04.006.20161120.hdf',
     '  LOCALVERSIONID=6.1.34',
     '  LONGNAME=MODIS/Terra+Aqua BRDF/Albedo Nadir BRDF-Adjusted Ref Daily L3 '
     'Global - 500m',
     '  long_name=Nadir_Reflectance_Band1',
     '  MAXIMUMOBSERVATIONS=0',
     '  NADIRDATARESOLUTION=500m',
     '  NORTHBOUNDINGCOORDINATE=49.99999999',
     '  NUMBEROFGRANULES=1',
     '  PARAMETERNAME.1=NOT SET',
     '  PERCENTLANDINTILE=35',
     '  PERCENTNEWBRDFS=0',
     '  PERCENTPROCESSEDINTILE=41',
     '  PERCENTSHAPEFIXEDBRDFS=99',
     '  PERCENTSUBSTITUTEBRDFS=0',
     '  PGEVERSION=6.0.34',
     '  PROCESSINGCENTER=MODAPS',
     '  PROCESSINGENVIRONMENT=Linux minion5709 2.6.18-408.el5 #1 SMP Tue Jan 19 '
     '09:14:52 EST 2016 x86_64 x86_64 x86_64 GNU/Linux',
     '  PRODUCTIONDATETIME=2016-04-21T01:37:46.000Z',
     '  QAPERCENTGOODQUALITY=0',
     '  QAPERCENTNOTPRODUCEDCLOUD=36',
     '  QAPERCENTNOTPRODUCEDOTHER=25',
     '  QAPERCENTOTHERQUALITY=38',
     '  RANGEBEGINNINGDATE=2012-11-24',
     '  RANGEBEGINNINGTIME=00:00:00.000000',
     '  RANGEENDINGDATE=2012-12-10',
     '  RANGEENDINGTIME=23:59:59.999999',
     '  REPROCESSINGACTUAL=reprocessed',
     '  REPROCESSINGPLANNED=further update is anticipated',
     '  scale_factor=0.0001',
     '  scale_factor_err=0',
     '  SCIENCEQUALITYFLAG.1=Not Investigated',
     '  SCIENCEQUALITYFLAGEXPLANATION.1=See '
     'http://landweb.nascom/nasa.gov/cgi-bin/QA_WWW/qaFlagPage.cgi?sat=aqua the '
     'product Science Quality status.',
     '  SETUPFILEID=06121997',
     '  SHORTNAME=MCD43A4',
     '  SOUTHBOUNDINGCOORDINATE=39.99999999',
     '  SPSOPARAMETERS=2015',
     '  TileID=51012004',
     '  units=reflectance, no units',
     '  valid_range=0, 32767',
     '  VERSION=1.0',
     '  VERSIONID=6',
     '  VERTICALTILENUMBER=4',
     '  WESTBOUNDINGCOORDINATE=-93.34342959',
     '  _FillValue=32767',
     'Image Structure Metadata:',
     '  INTERLEAVE=BAND',
     'Corner Coordinates:',
     'Upper Left  (-6671703.118, 5559752.598) ( 93d20\'36.35"W, 50d 0\' 0.00"N)',
     'Lower Left  (-6671703.118, 4447802.079) ( 78d19\'27.97"W, 40d 0\' 0.00"N)',
     'Upper Right (-5559752.598, 5559752.598) ( 77d47\'10.29"W, 50d 0\' 0.00"N)',
     'Lower Right (-5559752.598, 4447802.079) ( 65d16\'13.31"W, 40d 0\' 0.00"N)',
     'Center      (-6115727.858, 5003777.339) ( 77d46\'54.29"W, 45d 0\' 0.00"N)',
     'Band 1 Block=2400x1 Type=Int16, ColorInterp=Gray',
     '  Description = sti',
     '  Minimum=0.000, Maximum=32767.000, Mean=19423.443, StdDev=5499.371',
     '  NoData Value=-32768',
     '  Offset: 0,   Scale:0.0001',
     '  Metadata:',
     '    STATISTICS_MAXIMUM=32767',
     '    STATISTICS_MEAN=19423.44304077',
     '    STATISTICS_MINIMUM=0',
     '    STATISTICS_STDDEV=5499.37135843',
     '    STATISTICS_VALID_PERCENT=31.36'])]),

 # t_process[modis-temp] recording:
 ('temp',
  [('modis/tiles/h12v04/2012337/h12v04_2012337_MOD-MYD_temp.tif',
    'raster',
    'gdalinfo-stats',
    ['Driver: GTiff/GeoTIFF',
     'Size is 1200, 1200',
     'Coordinate System is:',
     'PROJCS["unnamed",',
     '    GEOGCS["Unknown datum based upon the custom spheroid",',
     '        DATUM["Not_specified_based_on_custom_spheroid",',
     '            SPHEROID["Custom spheroid",6371007.181,0]],',
     '        PRIMEM["Greenwich",0],',
     '        UNIT["degree",0.01745329]],',
     '    PROJECTION["Sinusoidal"],',
     '    PARAMETER["longitude_of_center",0],',
     '    PARAMETER["false_easting",0],',
     '    PARAMETER["false_northing",0],',
     '    UNIT["metre",1,',
     '        AUTHORITY["EPSG","9001"]]]',
     'Origin = (-6671703.11859900,5559752.59883300)',
     'Pixel Size = (926.62543313,-926.62543313)',
     'Metadata:',
     '  add_offset_err=0',
     '  ALGORITHMPACKAGEACCEPTANCEDATE=102004',
     '  ALGORITHMPACKAGEMATURITYCODE=Normal',
     '  ALGORITHMPACKAGENAME=MOD_PR11A',
     '  ALGORITHMPACKAGEVERSION=6',
     '  AREA_OR_POINT=Area',
     '  ASSOCIATEDINSTRUMENTSHORTNAME.1=MODIS',
     '  ASSOCIATEDPLATFORMSHORTNAME.1=Terra',
     '  ASSOCIATEDSENSORSHORTNAME.1=MODIS',
     '  AUTOMATICQUALITYFLAG.1=Passed',
     '  AUTOMATICQUALITYFLAGEXPLANATION.1=No automatic quality assessment is '
     'performed in the PGE.',
     '  AVAILABLE_ASSETS=MOD11A1 MYD11A1',
     '  calibrated_nt=5',
     '  CLOUD_CONTAMINATED_LST_SCREENED=YES',
     '  DAYNIGHTFLAG=Both',
     '  DESCRREVISION=6.0',
     '  EASTBOUNDINGCOORDINATE=-65.28378163',
     '  EXCLUSIONGRINGFLAG.1=N',
     '  GIPS_Modis_Version=1.0.0',
     '  '
     'GIPS_Source_Assets=MOD11A1.A2012337.h12v04.006.20161311.hdf,MYD11A1.A2012337.h12v04.006.20161321.hdf',
     '  GIPS_Version=0.0.0-dev',
     '  GRINGPOINTLATITUDE.1=49.99583333, 49.99583333, 40.00416666, 40.00416666',
     '  GRINGPOINTLONGITUDE.1=-93.34989768, -77.79268535, -65.28378163, '
     '-78.33942601',
     '  GRINGPOINTSEQUENCENO.1=1, 2, 3, 4',
     '  HDFEOSVersion=HDFEOS_V2.17',
     '  HORIZONTALTILENUMBER=12',
     '  identifier_product_doi=10.5067/MODIS/MOD11A1.006',
     '  identifier_product_doi_authority=http://dx.doi.org',
     '  INPUTGRANULEPOINTER.1=MOD03.A2012337.0245.006.20123381.hdf',
     '  INPUTGRANULEPOINTER.10=MOD021KM.A2012337.0425.006.20142250.hdf',
     '  INPUTGRANULEPOINTER.11=MOD35_L2.A2012337.0425.006.20150621.hdf',
     '  INPUTGRANULEPOINTER.12=MOD07_L2.A2012337.0425.006.20150621.hdf',
     '  INPUTGRANULEPOINTER.13=MOD03.A2012337.0430.006.20123381.hdf',
     '  INPUTGRANULEPOINTER.14=MOD021KM.A2012337.0430.006.20142250.hdf',
     '  INPUTGRANULEPOINTER.15=MOD35_L2.A2012337.0430.006.20150620.hdf',
     '  INPUTGRANULEPOINTER.16=MOD07_L2.A2012337.0430.006.20150620.hdf',
     '  INPUTGRANULEPOINTER.17=MOD03.A2012337.1445.006.20123381.hdf',
     '  INPUTGRANULEPOINTER.18=MOD021KM.A2012337.1445.006.20142250.hdf',
     '  INPUTGRANULEPOINTER.19=MOD35_L2.A2012337.1445.006.20150621.hdf',
     '  INPUTGRANULEPOINTER.2=MOD021KM.A2012337.0245.006.20142250.hdf',
     '  INPUTGRANULEPOINTER.20=MOD10_L2.A2012337.1445.006.20161171.hdf',
     '  INPUTGRANULEPOINTER.21=MOD07_L2.A2012337.1445.006.20150621.hdf',
     '  INPUTGRANULEPOINTER.22=MOD03.A2012337.1625.006.20123381.hdf',
     '  INPUTGRANULEPOINTER.23=MOD021KM.A2012337.1625.006.20142250.hdf',
     '  INPUTGRANULEPOINTER.24=MOD35_L2.A2012337.1625.006.20150621.hdf',
     '  INPUTGRANULEPOINTER.25=MOD10_L2.A2012337.1625.006.20161171.hdf',
     '  INPUTGRANULEPOINTER.26=MOD07_L2.A2012337.1625.006.20150621.hdf',
     '  INPUTGRANULEPOINTER.27=MOD03.A2012337.1800.006.20123381.hdf',
     '  INPUTGRANULEPOINTER.28=MOD021KM.A2012337.1800.006.20142250.hdf',
     '  INPUTGRANULEPOINTER.29=MOD35_L2.A2012337.1800.006.20150621.hdf',
     '  INPUTGRANULEPOINTER.3=MOD35_L2.A2012337.0245.006.20150620.hdf',
     '  INPUTGRANULEPOINTER.30=MOD10_L2.A2012337.1800.006.20161171.hdf',
     '  INPUTGRANULEPOINTER.31=MOD07_L2.A2012337.1800.006.20150621.hdf',
     '  INPUTGRANULEPOINTER.4=MOD07_L2.A2012337.0245.006.20150620.hdf',
     '  INPUTGRANULEPOINTER.5=MOD03.A2012337.0250.006.20123381.hdf',
     '  INPUTGRANULEPOINTER.6=MOD021KM.A2012337.0250.006.20142250.hdf',
     '  INPUTGRANULEPOINTER.7=MOD35_L2.A2012337.0250.006.20150620.hdf',
     '  INPUTGRANULEPOINTER.8=MOD07_L2.A2012337.0250.006.20150620.hdf',
     '  INPUTGRANULEPOINTER.9=MOD03.A2012337.0425.006.20123381.hdf',
     '  INPUTPOINTER=MOD03.A2012337.0245.006.20123381.hdf, '
     'MOD021KM.A2012337.0245.006.20142250.hdf, '
     'MOD35_L2.A2012337.0245.006.20150620.hdf, '
     'MOD07_L2.A2012337.0245.006.20150620.hdf, '
     'MOD03.A2012337.0250.006.20123381.hdf, '
     'MOD021KM.A2012337.0250.006.20142250.hdf, '
     'MOD35_L2.A2012337.0250.006.20150620.hdf, '
     'MOD07_L2.A2012337.0250.006.20150620.hdf, '
     'MOD03.A2012337.0425.006.20123381.hdf, '
     'MOD021KM.A2012337.0425.006.20142250.hdf, '
     'MOD35_L2.A2012337.0425.006.20150621.hdf, '
     'MOD07_L2.A2012337.0425.006.20150621.hdf, '
     'MOD03.A2012337.0430.006.20123381.hdf, '
     'MOD021KM.A2012337.0430.006.20142250.hdf, '
     'MOD35_L2.A2012337.0430.006.20150620.hdf, '
     'MOD07_L2.A2012337.0430.006.20150620.hdf, '
     'MOD03.A2012337.1445.006.20123381.hdf, '
     'MOD021KM.A2012337.1445.006.20142250.hdf, '
     'MOD35_L2.A2012337.1445.006.20150621.hdf, '
     'MOD10_L2.A2012337.1445.006.20161171.hdf, '
     'MOD07_L2.A2012337.1445.006.20150621.hdf, '
     'MOD03.A2012337.1625.006.20123381.hdf, '
     'MOD021KM.A2012337.1625.006.20142250.hdf, '
     'MOD35_L2.A2012337.1625.006.20150621.hdf, '
     'MOD10_L2.A2012337.1625.006.20161171.hdf, '
     'MOD07_L2.A2012337.1625.006.20150621.hdf, '
     'MOD03.A2012337.1800.006.20123381.hdf, '
     'MOD021KM.A2012337.1800.006.20142250.hdf, '
     'MOD35_L2.A2012337.1800.006.20150621.hdf, '
     'MOD10_L2.A2012337.1800.006.20161171.hdf, '
     'MOD07_L2.A2012337.1800.006.20150621.hdf',
     '  INPUTTILEPOINTER.1=MCDLC1KM.A2010001.h12v04.051.20133400.hdf',
     '  INPUTTILEPOINTER.2=MCD43A1.A2012337.h12v04.006.20161120.hdf',
     '  INPUTTILEPOINTER.3=MOD11A1.6.A2012337.h12v04.hdf',
     '  INPUTTILEPOINTER.4=MOD11B1.6.A2012337.h12v04.hdf',
     '  INPUTTILEPOINTER.5=MOD11UPD.A2-1.6.update_for_lst.h12v04.hdf',
     '  INSTRUMENTNAME=Moderate-Resolution Imaging SpectroRadiometer',
     '  LOCALGRANULEID=MOD11A1.A2012337.h12v04.006.20161311.hdf',
     '  LOCALINPUTGRANULEID=0245,0250,0425,0430,1445,1625,1800',
     '  LOCALVERSIONID=6.4.4AS',
     '  LONGNAME=MODIS/Terra Land Surface Temperature/Emissivity Daily L3 '
     'Global 1km SIN Grid',
     '  long_name=Daily daytime 1km grid Land-surface Temperature',
     '  LOOKUPTABLEPOINTER.1=band_emis.h',
     '  LOOKUPTABLEPOINTER.2=lst_coef.h',
     '  LOOKUPTABLETYPE.1=Land-cover based band emissivity database',
     '  LOOKUPTABLETYPE.2=the generalized split-window LST coefficients',
     '  LST=LST data * scale_factor',
     '  MEANOVERPASSTIME_DAY_AQUA=2.33734235',
     '  MEANOVERPASSTIME_DAY_TERRA=21.84355846',
     '  NORTHBOUNDINGCOORDINATE=49.99583333',
     '  NUMBAD_DAY_AQUA=1398452',
     '  NUMBAD_DAY_TERRA=1385409',
     '  Number Type=uint16',
     '  NUMBEST_DAY_AQUA=3352',
     '  NUMBEST_DAY_TERRA=1756',
     '  NUMGOOD_DAY_AQUA=41548',
     '  NUMGOOD_DAY_TERRA=54591',
     '  N_GRAN_POINTERS=31',
     '  PARAMETERNAME.1=MOD 1KM L3 LST',
     '  PGEVERSION=6.4.14',
     '  PROCESSINGCENTER=MODAPS',
     '  PROCESSINGDATETIME=2016-05-10T16:45:34.000Z',
     '  PROCESSINGENVIRONMENT=Linux minion5631 2.6.18-407.el5 #1 SMP Wed Nov 11 '
     '08:12:41 EST 2015 x86_64 x86_64 x86_64 GNU/Linux',
     '  PRODUCTIONDATETIME=2016-05-10T18:58:51.000Z',
     '  QAFRACTIONGOODQUALITY=0.0009281',
     '  QAFRACTIONNOTPRODUCEDCLOUD=0.8482469',
     '  QAFRACTIONNOTPRODUCEDOTHER=0.1269437',
     '  QAFRACTIONOTHERQUALITY=0.0238812',
     '  QAPERCENTCLOUDCOVER.1=85',
     '  QAPERCENTGOODQUALITY=0',
     '  QAPERCENTINTERPOLATEDDATA.1=0',
     '  QAPERCENTMISSINGDATA.1=0',
     '  QAPERCENTNOTPRODUCEDCLOUD=85',
     '  QAPERCENTNOTPRODUCEDOTHER=13',
     '  QAPERCENTOTHERQUALITY=2',
     '  QAPERCENTOUTOFBOUNDSDATA.1=0',
     '  RANGEBEGINNINGDATE=2012-12-02',
     '  RANGEBEGINNINGTIME=00:00:00',
     '  RANGEENDINGDATE=2012-12-02',
     '  RANGEENDINGTIME=23:59:59',
     '  REPROCESSINGACTUAL=reprocessed',
     '  REPROCESSINGPLANNED=further update is anticipated',
     '  scale_factor=0.02',
     '  scale_factor_err=0',
     '  SCIENCEQUALITYFLAG.1=Not Investigated',
     '  SCIENCEQUALITYFLAGEXPLANATION.1=See '
     'http://landweb.nascom.nasa.gov/cgi-bin/QA_WWW/qaFlagPage.cgi?sat=terra '
     'for the product Science Quality status.',
     '  SHORTNAME=MOD11A1',
     '  SOUTHBOUNDINGCOORDINATE=40.00416666',
     '  SPSOPARAMETERS=2484 and 3323',
     '  TileID=51012004',
     '  units=K',
     '  valid_range=7500, 65535',
     '  VERSION=1.1',
     '  VERSIONID=6',
     '  VERTICALTILENUMBER=04',
     '  WESTBOUNDINGCOORDINATE=-93.34989768',
     '  _FillValue=0',
     'Image Structure Metadata:',
     '  INTERLEAVE=PIXEL',
     'Corner Coordinates:',
     'Upper Left  (-6671703.119, 5559752.599) ( 93d20\'36.35"W, 50d 0\' 0.00"N)',
     'Lower Left  (-6671703.119, 4447802.079) ( 78d19\'27.97"W, 40d 0\' 0.00"N)',
     'Upper Right (-5559752.599, 5559752.599) ( 77d47\'10.29"W, 50d 0\' 0.00"N)',
     'Lower Right (-5559752.599, 4447802.079) ( 65d16\'13.31"W, 40d 0\' 0.00"N)',
     'Center      (-6115727.859, 5003777.339) ( 77d46\'54.29"W, 45d 0\' 0.00"N)',
     'Band 1 Block=1200x1 Type=UInt16, ColorInterp=Gray',
     '  Description = Temperature Daytime Terra',
     '  NoData Value=65535',
     '  Offset: 0,   Scale:0.02',
     '  Metadata:',
     '    STATISTICS_VALID_PERCENT=0',
     'Band 2 Block=1200x1 Type=UInt16, ColorInterp=Undefined',
     '  Description = Temperature Nighttime Terra',
     '  NoData Value=65535',
     '  Offset: 0,   Scale:0.02',
     '  Metadata:',
     '    STATISTICS_VALID_PERCENT=0',
     'Band 3 Block=1200x1 Type=UInt16, ColorInterp=Undefined',
     '  Description = Temperature Daytime Aqua',
     '  NoData Value=65535',
     '  Offset: 0,   Scale:0.02',
     '  Metadata:',
     '    STATISTICS_VALID_PERCENT=0',
     'Band 4 Block=1200x1 Type=UInt16, ColorInterp=Undefined',
     '  Description = Temperature Nighttime Aqua',
     '  NoData Value=65535',
     '  Offset: 0,   Scale:0.02',
     '  Metadata:',
     '    STATISTICS_VALID_PERCENT=0',
     'Band 5 Block=1200x1 Type=UInt16, ColorInterp=Undefined',
     '  Description = Temperature Best Quality',
     '  Minimum=0.000, Maximum=10.000, Mean=0.023, StdDev=0.402',
     '  NoData Value=65535',
     '  Metadata:',
     '    STATISTICS_MAXIMUM=10',
     '    STATISTICS_MEAN=0.02316736',
     '    STATISTICS_MINIMUM=0',
     '    STATISTICS_STDDEV=0.40188800',
     '    STATISTICS_VALID_PERCENT=100'])]),

 # t_process[modis-temp8td] recording:
 ('temp8td',
  [('modis/tiles/h12v04/2012337/h12v04_2012337_MOD_temp8td.tif',
    'symlink',
    'HDF4_EOS:EOS_GRID:"',
    '/modis/tiles/h12v04/2012337/MOD11A2.A2012337.h12v04.006.2016137164847.hdf":MODIS_Grid_8Day_1km_LST:LST_Day_1km')]),

 # t_process[modis-temp8tn] recording:
 ('temp8tn',
  [('modis/tiles/h12v04/2012337/h12v04_2012337_MOD_temp8tn.tif',
    'symlink',
    'HDF4_EOS:EOS_GRID:"',
    '/modis/tiles/h12v04/2012337/MOD11A2.A2012337.h12v04.006.2016137164847.hdf":MODIS_Grid_8Day_1km_LST:LST_Night_1km')]),

 # t_process[modis-vari] recording:
 ('vari',
  [('modis/tiles/h12v04/2012337/h12v04_2012337_MCD_vari.tif',
    'raster',
    'gdalinfo-stats',
    ['Driver: GTiff/GeoTIFF',
     'Size is 2400, 2400',
     'Coordinate System is:',
     'PROJCS["unnamed",',
     '    GEOGCS["Unknown datum based upon the custom spheroid",',
     '        DATUM["Not_specified_based_on_custom_spheroid",',
     '            SPHEROID["Custom spheroid",6371007.181,0]],',
     '        PRIMEM["Greenwich",0],',
     '        UNIT["degree",0.01745329]],',
     '    PROJECTION["Sinusoidal"],',
     '    PARAMETER["longitude_of_center",0],',
     '    PARAMETER["false_easting",0],',
     '    PARAMETER["false_northing",0],',
     '    UNIT["metre",1,',
     '        AUTHORITY["EPSG","9001"]]]',
     'Origin = (-6671703.11799999,5559752.59833300)',
     'Pixel Size = (463.31271652,-463.31271652)',
     'Metadata:',
     '  add_offset=0',
     '  add_offset_err=0',
     '  ALBEDOFILEID=06121997',
     '  AREA_OR_POINT=Area',
     '  ASSOCIATEDINSTRUMENTSHORTNAME.1=MODIS',
     '  ASSOCIATEDINSTRUMENTSHORTNAME.2=MODIS',
     '  ASSOCIATEDPLATFORMSHORTNAME.1=Terra',
     '  ASSOCIATEDPLATFORMSHORTNAME.2=Aqua',
     '  ASSOCIATEDSENSORSHORTNAME.1=MODIS',
     '  ASSOCIATEDSENSORSHORTNAME.2=MODIS',
     '  AUTOMATICQUALITYFLAG.1=Passed',
     '  AUTOMATICQUALITYFLAGEXPLANATION.1=Passed was set as a default value. '
     'More algorithm will be developed',
     '  AVERAGENUMBEROBS=1',
     '  BRDFCODEID=AMBRALS_V4.0R1',
     '  BRDFDATABASEVERSION=v1.0500m',
     '  calibrated_nt=5',
     '  CHARACTERISTICBINANGULARSIZE=15.0',
     '  CHARACTERISTICBINSIZE=463.31271652',
     '  COVERAGECALCULATIONMETHOD=volume',
     '  DATACOLUMNS=2400',
     '  DATAROWS=2400',
     '  DAYNIGHTFLAG=Day',
     '  DESCRREVISION=6.1',
     '  EASTBOUNDINGCOORDINATE=-65.25948606',
     '  EXCLUSIONGRINGFLAG.1=N',
     '  GEOANYABNORMAL=False',
     '  GEOESTMAXRMSERROR=75.0',
     '  GIPS_Modis_Version=1.0.0',
     '  GIPS_Source_Assets=MCD43A4.A2012337.h12v04.006.20161120.hdf',
     '  GIPS_Version=0.0.0-dev',
     '  GLOBALGRIDCOLUMNS=86400',
     '  GLOBALGRIDROWS=43200',
     '  GRINGPOINTLATITUDE.1=39.78578782, 49.99719181, 50.07541801, 39.84112776',
     '  GRINGPOINTLONGITUDE.1=-78.20833299, -93.38216574, -77.75056839, '
     '-65.07807811',
     '  GRINGPOINTSEQUENCENO.1=1, 2, 3, 4',
     '  HDFEOSVersion=HDFEOS_V2.17',
     '  HORIZONTALTILENUMBER=12',
     '  identifier_product_doi=10.5067/MODIS/MCD43A4.006',
     '  identifier_product_doi_authority=http://dx.doi.org',
     '  INPUTPOINTER=MYD09GA.A2012329.h12v04.006.20152510.hdf, '
     'MYD09GA.A2012330.h12v04.006.20152511.hdf, '
     'MYD09GA.A2012331.h12v04.006.20152511.hdf, '
     'MYD09GA.A2012332.h12v04.006.20152511.hdf, '
     'MYD09GA.A2012333.h12v04.006.20152521.hdf, '
     'MYD09GA.A2012334.h12v04.006.20152521.hdf, '
     'MYD09GA.A2012335.h12v04.006.20152521.hdf, '
     'MYD09GA.A2012336.h12v04.006.20152522.hdf, '
     'MYD09GA.A2012337.h12v04.006.20152521.hdf, '
     'MYD09GA.A2012338.h12v04.006.20152511.hdf, '
     'MYD09GA.A2012339.h12v04.006.20152521.hdf, '
     'MYD09GA.A2012340.h12v04.006.20152521.hdf, '
     'MYD09GA.A2012341.h12v04.006.20152521.hdf, '
     'MYD09GA.A2012342.h12v04.006.20152522.hdf, '
     'MYD09GA.A2012343.h12v04.006.20152522.hdf, '
     'MYD09GA.A2012344.h12v04.006.20152522.hdf, '
     'MOD09GA.A2012329.h12v04.006.20152511.hdf, '
     'MOD09GA.A2012330.h12v04.006.20152510.hdf, '
     'MOD09GA.A2012331.h12v04.006.20152511.hdf, '
     'MOD09GA.A2012332.h12v04.006.20152512.hdf, '
     'MOD09GA.A2012333.h12v04.006.20152521.hdf, '
     'MOD09GA.A2012334.h12v04.006.20152522.hdf, '
     'MOD09GA.A2012335.h12v04.006.20152522.hdf, '
     'MOD09GA.A2012336.h12v04.006.20152522.hdf, '
     'MOD09GA.A2012337.h12v04.006.20152522.hdf, '
     'MOD09GA.A2012338.h12v04.006.20152511.hdf, '
     'MOD09GA.A2012339.h12v04.006.20152512.hdf, '
     'MOD09GA.A2012340.h12v04.006.20152522.hdf, '
     'MOD09GA.A2012341.h12v04.006.20152522.hdf, '
     'MOD09GA.A2012342.h12v04.006.20152522.hdf, '
     'MOD09GA.A2012343.h12v04.006.20152530.hdf, '
     'MOD09GA.A2012344.h12v04.006.20152530.hdf, MCD43DB.A2012336.6.h12v04.hdf',
     '  LOCALGRANULEID=MCD43A4.A2012337.h12v04.006.20161120.hdf',
     '  LOCALVERSIONID=6.1.34',
     '  LONGNAME=MODIS/Terra+Aqua BRDF/Albedo Nadir BRDF-Adjusted Ref Daily L3 '
     'Global - 500m',
     '  long_name=Nadir_Reflectance_Band1',
     '  MAXIMUMOBSERVATIONS=0',
     '  NADIRDATARESOLUTION=500m',
     '  NORTHBOUNDINGCOORDINATE=49.99999999',
     '  NUMBEROFGRANULES=1',
     '  PARAMETERNAME.1=NOT SET',
     '  PERCENTLANDINTILE=35',
     '  PERCENTNEWBRDFS=0',
     '  PERCENTPROCESSEDINTILE=41',
     '  PERCENTSHAPEFIXEDBRDFS=99',
     '  PERCENTSUBSTITUTEBRDFS=0',
     '  PGEVERSION=6.0.34',
     '  PROCESSINGCENTER=MODAPS',
     '  PROCESSINGENVIRONMENT=Linux minion5709 2.6.18-408.el5 #1 SMP Tue Jan 19 '
     '09:14:52 EST 2016 x86_64 x86_64 x86_64 GNU/Linux',
     '  PRODUCTIONDATETIME=2016-04-21T01:37:46.000Z',
     '  QAPERCENTGOODQUALITY=0',
     '  QAPERCENTNOTPRODUCEDCLOUD=36',
     '  QAPERCENTNOTPRODUCEDOTHER=25',
     '  QAPERCENTOTHERQUALITY=38',
     '  RANGEBEGINNINGDATE=2012-11-24',
     '  RANGEBEGINNINGTIME=00:00:00.000000',
     '  RANGEENDINGDATE=2012-12-10',
     '  RANGEENDINGTIME=23:59:59.999999',
     '  REPROCESSINGACTUAL=reprocessed',
     '  REPROCESSINGPLANNED=further update is anticipated',
     '  scale_factor=0.0001',
     '  scale_factor_err=0',
     '  SCIENCEQUALITYFLAG.1=Not Investigated',
     '  SCIENCEQUALITYFLAGEXPLANATION.1=See '
     'http://landweb.nascom/nasa.gov/cgi-bin/QA_WWW/qaFlagPage.cgi?sat=aqua the '
     'product Science Quality status.',
     '  SETUPFILEID=06121997',
     '  SHORTNAME=MCD43A4',
     '  SOUTHBOUNDINGCOORDINATE=39.99999999',
     '  SPSOPARAMETERS=2015',
     '  TileID=51012004',
     '  units=reflectance, no units',
     '  valid_range=0, 32767',
     '  VERSION=1.0',
     '  VERSIONID=6',
     '  VERTICALTILENUMBER=4',
     '  WESTBOUNDINGCOORDINATE=-93.34342959',
     '  _FillValue=32767',
     'Image Structure Metadata:',
     '  INTERLEAVE=BAND',
     'Corner Coordinates:',
     'Upper Left  (-6671703.118, 5559752.598) ( 93d20\'36.35"W, 50d 0\' 0.00"N)',
     'Lower Left  (-6671703.118, 4447802.079) ( 78d19\'27.97"W, 40d 0\' 0.00"N)',
     'Upper Right (-5559752.598, 5559752.598) ( 77d47\'10.29"W, 50d 0\' 0.00"N)',
     'Lower Right (-5559752.598, 4447802.079) ( 65d16\'13.31"W, 40d 0\' 0.00"N)',
     'Center      (-6115727.858, 5003777.339) ( 77d46\'54.29"W, 45d 0\' 0.00"N)',
     'Band 1 Block=2400x1 Type=Int16, ColorInterp=Gray',
     '  Description = vari',
     '  Minimum=-32766.000, Maximum=32767.000, Mean=838.624, StdDev=9278.502',
     '  NoData Value=-32768',
     '  Offset: 0,   Scale:0.0001',
     '  Metadata:',
     '    STATISTICS_MAXIMUM=32767',
     '    STATISTICS_MEAN=838.62446558',
     '    STATISTICS_MINIMUM=-32766',
     '    STATISTICS_STDDEV=9278.50189910',
     '    STATISTICS_VALID_PERCENT=43.45'])]),
])
