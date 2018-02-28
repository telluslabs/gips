
import collections

from .. import util

from . import modis_process
from . import merra_process
from . import sentinel2_process

expectations = {}
mark_spec = {}

expectations['modis'] = modis_process.expectations
expectations['merra'] = merra_process.expectations

expectations['sentinel2'] = sentinel2_process.expectations

mark_spec['sentinel2'] = util.slow

expectations['prism'] = collections.OrderedDict([
    # t_process[tmin] recording:
    ('tmin',
        [('prism/tiles/CONUS/19821201/CONUS_19821201_prism_tmin.tif',
          'symlink',
          '/vsizip/',
          '/prism/tiles/CONUS/19821201/PRISM_tmin_stable_4kmD1_19821201_bil.zip/PRISM_tmin_stable_4kmD1_19821201_bil.bil'),
         ('prism/tiles/CONUS/19821202/CONUS_19821202_prism_tmin.tif',
          'symlink',
          '/vsizip/',
          '/prism/tiles/CONUS/19821202/PRISM_tmin_stable_4kmD1_19821202_bil.zip/PRISM_tmin_stable_4kmD1_19821202_bil.bil'),
         ('prism/tiles/CONUS/19821203/CONUS_19821203_prism_tmin.tif',
          'symlink',
          '/vsizip/',
          '/prism/tiles/CONUS/19821203/PRISM_tmin_stable_4kmD1_19821203_bil.zip/PRISM_tmin_stable_4kmD1_19821203_bil.bil')]),

    # t_process[tmax] recording:
    ('tmax',
        [('prism/tiles/CONUS/19821202/CONUS_19821202_prism_tmax.tif',
          'symlink',
          '/vsizip/',
          '/prism/tiles/CONUS/19821202/PRISM_tmax_stable_4kmD1_19821202_bil.zip/PRISM_tmax_stable_4kmD1_19821202_bil.bil'),
         ('prism/tiles/CONUS/19821203/CONUS_19821203_prism_tmax.tif',
          'symlink',
          '/vsizip/',
          '/prism/tiles/CONUS/19821203/PRISM_tmax_stable_4kmD1_19821203_bil.zip/PRISM_tmax_stable_4kmD1_19821203_bil.bil'),
         ('prism/tiles/CONUS/19821201/CONUS_19821201_prism_tmax.tif',
          'symlink',
          '/vsizip/',
          '/prism/tiles/CONUS/19821201/PRISM_tmax_stable_4kmD1_19821201_bil.zip/PRISM_tmax_stable_4kmD1_19821201_bil.bil')]),

    # IMPORTANT NOTE pptsum seems to generate ppt products as part of
    # its function; as a result ppt products may exist already if pptsum
    # goes first.
    # t_process[ppt] recording:
    ('ppt',
        [('prism/tiles/CONUS/19821203/CONUS_19821203_prism_ppt.tif',
          'symlink',
          '/vsizip/',
          '/prism/tiles/CONUS/19821203/PRISM_ppt_stable_4kmD2_19821203_bil.zip/PRISM_ppt_stable_4kmD2_19821203_bil.bil'),
         ('prism/tiles/CONUS/19821201/CONUS_19821201_prism_ppt.tif',
          'symlink',
          '/vsizip/',
          '/prism/tiles/CONUS/19821201/PRISM_ppt_stable_4kmD2_19821201_bil.zip/PRISM_ppt_stable_4kmD2_19821201_bil.bil'),
         ('prism/tiles/CONUS/19821202/CONUS_19821202_prism_ppt.tif',
          'symlink',
          '/vsizip/',
          '/prism/tiles/CONUS/19821202/PRISM_ppt_stable_4kmD2_19821202_bil.zip/PRISM_ppt_stable_4kmD2_19821202_bil.bil')]),

    # t_process[pptsum] recording:
    ('pptsum',
        [('prism/tiles/CONUS/19821203/CONUS_19821203_prism_pptsum-3.tif',
          'raster',
          'gdalinfo-stats',
          ['Driver: GTiff/GeoTIFF',
           'Size is 1405, 621',
           'Coordinate System is:',
           'GEOGCS["NAD83",',
           '    DATUM["North_American_Datum_1983",',
           '        SPHEROID["GRS 1980",6378137,298.2572221010042,',
           '            AUTHORITY["EPSG","7019"]],',
           '        AUTHORITY["EPSG","6269"]],',
           '    PRIMEM["Greenwich",0],',
           '    UNIT["degree",0.0174532925199433],',
           '    AUTHORITY["EPSG","4269"]]',
           'Origin = (-125.020833333333329,49.937500000002032)',
           'Pixel Size = (0.041666666666670,-0.041666666666670)',
           'Metadata:',
           '  AREA_OR_POINT=Area',
           'Image Structure Metadata:',
           '  INTERLEAVE=BAND',
           'Corner Coordinates:',
           'Upper Left  (-125.0208333,  49.9375000) (125d 1\'15.00"W, 49d56\'15.00"N)',
           'Lower Left  (-125.0208333,  24.0625000) (125d 1\'15.00"W, 24d 3\'45.00"N)',
           'Upper Right ( -66.4791667,  49.9375000) ( 66d28\'45.00"W, 49d56\'15.00"N)',
           'Lower Right ( -66.4791667,  24.0625000) ( 66d28\'45.00"W, 24d 3\'45.00"N)',
           'Center      ( -95.7500000,  37.0000000) ( 95d45\' 0.00"W, 37d 0\' 0.00"N)',
           'Band 1 Block=1405x1 Type=Float32, ColorInterp=Gray',
           '  Description = Cumulative Precipitate(3 day window)',
           '  Minimum=-29997.000, Maximum=332.600, Mean=-13428.782, StdDev=14925.792',
           '  NoData Value=-9999',
           '  Metadata:',
           '    STATISTICS_MAXIMUM=332.60000610352',
           '    STATISTICS_MEAN=-13428.782340994',
           '    STATISTICS_MINIMUM=-29997',
           '    STATISTICS_STDDEV=14925.791999964'])]),
])

mark_spec['landsat'] = util.slow

expectations['landsat'] = {
    # t_process[bqashadow] recording:
    'bqashadow':
        [('landsat/tiles/012030/2017213/012030_2017213_LC8_bqashadow.tif',
          'hash',
          'sha256',
          '1c8c8e252afe94deb0684c56c71149d3585b997abae72a1671217aa4b74faacb')],

    # t_process[ndvi-toa] recording:
    'ndvi-toa':
        [('landsat/tiles/012030/2017213/012030_2017213_LC8_ndvi-toa.tif',
          'hash',
          'sha256',
          '5d2273f5eafa9fcfff1a068fba21c686b574345d1c090397a05942bb5017a715')],

    # t_process[acca] recording:
    'acca':
        [('landsat/tiles/012030/2017213/012030_2017213_LC8_acca.tif',
          'hash',
          'sha256',
          'd4412cd13adad9cde0c7668fb44f728fc7a2e5bda6ddaa062fc65d5de9546765')],

    # t_process[rad-toa] recording:
    'rad-toa':
        [('landsat/tiles/012030/2017213/012030_2017213_LC8_rad-toa.tif',
          'hash',
          'sha256',
          '2e4923033454e9021b31def954b0e8b3c4247ed0856414995e148f672207ca46')],

    # t_process[ref-toa] recording:
    'ref-toa':
        [('landsat/tiles/012030/2017213/012030_2017213_LC8_ref-toa.tif',
          'hash',
          'sha256',
          'a10ba27cd930bb6bd32c4649cd2ce7d7274e82fef043cf4a2a79c212cc4754ea')],
}

expectations['sar'] = {
    # t_process[date] recording:
    'date':
        [('sar/tiles/N07E099/2015101/N07E099_2015101_AWBD_date.tif',
          'hash',
          'sha256',
          'c29663846c6ec54f570e925e0e27bbf6fcf92824ff68c11531f266ffc073331a'),
         ('sar/tiles/N19E100/2010182/N19E100_2010182_AFBD_date.tif',
          'hash',
          'sha256',
          '8b6a0d270e53ca91c6cbaeaa5c9a5290ad11970e36a5b49e9b75f5e5dd272adc'),
         ('sar/tiles/N00E099/2009041/N00E099_2009041_AWB1_date.tif',
          'hash',
          'sha256',
          '13bdb0c9bb93a31491c8843d0c7b24ad75dfb8a33bc2d37460d09592d01a04ce')],

    # t_process[linci] recording:
    'linci':
        [('sar/tiles/N07E099/2015101/N07E099_2015101_AWBD_linci.tif',
          'hash',
          'sha256',
          'ac5082457c7b7ff7c5361534a2f691469b18cf636b8c5c136694310ac6693c33'),
         ('sar/tiles/N19E100/2010182/N19E100_2010182_AFBD_linci.tif',
          'hash',
          'sha256',
          'd18394c725a5f8c62b18ff8ab7fc7357a3bfb1a263e3c3dbc2eb0aed09a0f0c8'),
         ('sar/tiles/N00E099/2009041/N00E099_2009041_AWB1_linci.tif',
          'hash',
          'sha256',
          'b76a9e585762f060b653d012bfeff760c5250076c174348446dc8f31d0fb4fe2')],

    # t_process[mask] recording:
    'mask':
        [('sar/tiles/N00E099/2009041/N00E099_2009041_AWB1_mask.tif',
          'hash',
          'sha256',
          '72311122b6b88f80dd85e76380e092bd70c33c4f26461316b4829962c1ecc1fc'),
         ('sar/tiles/N07E099/2015101/N07E099_2015101_AWBD_mask.tif',
          'hash',
          'sha256',
          '5e463c8174e0acb64db0d7067a6414791a795d237221af30944adaa155fec622'),
         ('sar/tiles/N19E100/2010182/N19E100_2010182_AFBD_mask.tif',
          'hash',
          'sha256',
          'e3896c79e5b5ed6380bf821a2cddd65014cc35278933cb1c2c15620e27615afc')],

    # t_process[sign] recording:
    'sign':
        [('sar/tiles/N07E099/2015101/N07E099_2015101_AWBD_sign.tif',
          'hash',
          'sha256',
          'a47201adaca8f0cbd9ffa64f6953d3b75a502860f48196169449db69b766aef3'),
         ('sar/tiles/N00E099/2009041/N00E099_2009041_AWB1_sign.tif',
          'hash',
          'sha256',
          'f871ea0bfe899438ed7d233ed4e7f72db1d989d1af9d6c55362fac87dce74b31'),
         ('sar/tiles/N19E100/2010182/N19E100_2010182_AFBD_sign.tif',
          'hash',
          'sha256',
          '49e9ded5ee3a169eddaa5e50aa34b6a0c91dc1f37b345be6f2cf2aea25dfd6ce')],
}

expectations['aster'] = {
    'ndvi':
        [('aster/tiles/AST_L1T_00309072010154405_20150602204317_52300/2010250/AST_L1T_00309072010154405_20150602204317_52300_2010250_L1T_ndvi.tif',
          'raster',
          'gdalinfo-stats',
          ['Driver: GTiff/GeoTIFF',
           'Size is 5779, 5191',
           "Coordinate System is `'",
           'Metadata:',
           '  AVAILABLE_ASSETS=L1T',
           '  GIPS Version=0.9.3-dev',
           '  VERSION=1.0',
           'Image Structure Metadata:',
           '  INTERLEAVE=BAND',
           'Corner Coordinates:',
           'Upper Left  (    0.0,    0.0)',
           'Lower Left  (    0.0, 5191.0)',
           'Upper Right ( 5779.0,    0.0)',
           'Lower Right ( 5779.0, 5191.0)',
           'Center      ( 2889.5, 2595.5)',
           'Band 1 Block=5779x1 Type=Int16, ColorInterp=Gray',
           '  Description = NDVI',
           '  Minimum=-10000.000, Maximum=10000.000, Mean=-1247.030, StdDev=2887.928',
           '  NoData Value=32767',
           '  Offset: 0,   Scale:0.0001',
           '  Metadata:',
           '    STATISTICS_MAXIMUM=10000',
           '    STATISTICS_MEAN=-1247.0296384634',
           '    STATISTICS_MINIMUM=-10000',
           '    STATISTICS_STDDEV=2887.9276352503']),
         ('aster/tiles/AST_L1T_00309072010154347_20150602204320_81635/2010250/AST_L1T_00309072010154347_20150602204320_81635_2010250_L1T_ndvi.tif',
          'raster',
          'gdalinfo-stats',
          ['Driver: GTiff/GeoTIFF',
           'Size is 5779, 5191',
           "Coordinate System is `'",
           'Metadata:',
           '  AVAILABLE_ASSETS=L1T',
           '  GIPS Version=0.9.3-dev',
           '  VERSION=1.0',
           'Image Structure Metadata:',
           '  INTERLEAVE=BAND',
           'Corner Coordinates:',
           'Upper Left  (    0.0,    0.0)',
           'Lower Left  (    0.0, 5191.0)',
           'Upper Right ( 5779.0,    0.0)',
           'Lower Right ( 5779.0, 5191.0)',
           'Center      ( 2889.5, 2595.5)',
           'Band 1 Block=5779x1 Type=Int16, ColorInterp=Gray',
           '  Description = NDVI',
           '  Minimum=-10000.000, Maximum=10000.000, Mean=-1533.238, StdDev=825.590',
           '  NoData Value=32767',
           '  Offset: 0,   Scale:0.0001',
           '  Metadata:',
           '    STATISTICS_MAXIMUM=10000',
           '    STATISTICS_MEAN=-1533.2377396827',
           '    STATISTICS_MINIMUM=-10000',
           '    STATISTICS_STDDEV=825.5896949366']),
         ('aster/tiles/AST_L1T_00309072010154356_20150602204320_81633/2010250/AST_L1T_00309072010154356_20150602204320_81633_2010250_L1T_ndvi.tif',
          'raster',
          'gdalinfo-stats',
          ['Driver: GTiff/GeoTIFF',
           'Size is 5779, 5191',
           "Coordinate System is `'",
           'Metadata:',
           '  AVAILABLE_ASSETS=L1T',
           '  GIPS Version=0.9.3-dev',
           '  VERSION=1.0',
           'Image Structure Metadata:',
           '  INTERLEAVE=BAND',
           'Corner Coordinates:',
           'Upper Left  (    0.0,    0.0)',
           'Lower Left  (    0.0, 5191.0)',
           'Upper Right ( 5779.0,    0.0)',
           'Lower Right ( 5779.0, 5191.0)',
           'Center      ( 2889.5, 2595.5)',
           'Band 1 Block=5779x1 Type=Int16, ColorInterp=Gray',
           '  Description = NDVI',
           '  Minimum=-10000.000, Maximum=10000.000, Mean=-1560.682, StdDev=1553.922',
           '  NoData Value=32767',
           '  Offset: 0,   Scale:0.0001',
           '  Metadata:',
           '    STATISTICS_MAXIMUM=10000',
           '    STATISTICS_MEAN=-1560.682477304',
           '    STATISTICS_MINIMUM=-10000',
           '    STATISTICS_STDDEV=1553.9216186018'])],
}
