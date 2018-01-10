
import collections

from .. import util

from . import modis_process
from . import merra_process

expectations = {}
mark_spec = {}

expectations['modis'] = modis_process.expectations
expectations['merra'] = merra_process.expectations

expectations['prism'] = {
    # t_process[tmin] recording:
    'tmin':
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
          '/prism/tiles/CONUS/19821203/PRISM_tmin_stable_4kmD1_19821203_bil.zip/PRISM_tmin_stable_4kmD1_19821203_bil.bil')],

    # t_process[tmax] recording:
    'tmax':
        [('prism/tiles/CONUS/19821203/CONUS_19821203_prism_tmax.tif',
          'symlink',
          '/vsizip/',
          '/prism/tiles/CONUS/19821203/PRISM_tmax_stable_4kmD1_19821203_bil.zip/PRISM_tmax_stable_4kmD1_19821203_bil.bil'),
         ('prism/tiles/CONUS/19821201/CONUS_19821201_prism_tmax.tif',
          'symlink',
          '/vsizip/',
          '/prism/tiles/CONUS/19821201/PRISM_tmax_stable_4kmD1_19821201_bil.zip/PRISM_tmax_stable_4kmD1_19821201_bil.bil'),
         ('prism/tiles/CONUS/19821202/CONUS_19821202_prism_tmax.tif',
          'symlink',
          '/vsizip/',
          '/prism/tiles/CONUS/19821202/PRISM_tmax_stable_4kmD1_19821202_bil.zip/PRISM_tmax_stable_4kmD1_19821202_bil.bil')],

    # IMPORTANT NOTE pptsum seems to generate ppt products as part of
    # its function; as a result ppt products may exist already if pptsum
    # goes first.
    # t_process[ppt] recording:
    'ppt':
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
          '/prism/tiles/CONUS/19821202/PRISM_ppt_stable_4kmD2_19821202_bil.zip/PRISM_ppt_stable_4kmD2_19821202_bil.bil')],

    # t_process[pptsum] recording:
    'pptsum':
        [('prism/tiles/CONUS/19821203/CONUS_19821203_prism_pptsum-3.tif',
          'hash',
          'sha256',
          'd9772d10372ad86550dacae3d5645837cd9a10228db70f4e2bc7149b836495d9')],
}

mark_spec['sentinel2'] = util.slow

expectations['sentinel2'] = collections.OrderedDict([
    # TODO acolite products; should use --acolite flag
    # acoflags    0 = water 1 = no data 2 = land
    # fai         Floating Algae Index
    # oc2chl      Blue-Green Ratio Chlorophyll Algorithm using bands 483 & 561
    # oc3chl      Blue-Green Ratio Chlorophyll Algorithm using bands 443, 483, & 561
    # rhow        Water-Leaving Radiance-Reflectance
    # spm655      Suspended Sediment Concentration 655nm
    # turbidity   Blended Turbidity
    ('ref-toa',
     [('sentinel2/tiles/19TCH/2017010/19TCH_2017010_S2A_ref-toa.tif',
       'hash',
       'sha256',
       '59521f38170ff8d5d001292dc9424fe23ce0c7226f6dcc79801d7b78eb8faacd')],
    ),
    ('rad-toa',
     [('sentinel2/tiles/19TCH/2017010/19TCH_2017010_S2A_rad-toa.tif',
       'hash',
       'sha256',
       'fa8a2cb6917d68d77931fb52c4a1dadd93501a7431f966e2641179ed570f7d3e')],
    ),
    ('rad',
     [('sentinel2/tiles/19TCH/2017010/19TCH_2017010_S2A_rad.tif',
      'hash',
      'sha256',
      '7017fdee077e01f592c80465a82a7f6b9904ed60d6fdfc941f26c2d94299438c')],
    ),
    ('ref',
     [('sentinel2/tiles/19TCH/2017010/19TCH_2017010_S2A_ref.tif',
       'hash',
       'sha256',
       '34e1f63f0680e05172dd763f78d55254c0f44c9b730f00c01646acc7b4ad452b')],
    ),
    ('cfmask',
     [('sentinel2/tiles/19TCH/2017010/19TCH_2017010_S2A_cfmask.tif',
       'hash',
       'sha256',
       'd4438cc066e2e4cc26891635cbcaf46c00c46e240a29d5e7397344538bba7346')],
    ),

    # all the index products are made by the same gippy call so given
    # how slow sentinel2 is, just do a few for now; it probably
    # exercises the code well enough.  How to know if you're exercising
    # the bands:
    # https://github.com/gipit/gippy/blob/6d201870e55a7855814b3bdd3d30b05a889c24ed/GIP/GeoAlgorithms.cpp#L458
    # other indices if desired:
    # 'lswi', 'bi', 'brgt', 'crc', 'isti', 'msavi2',
    # 'ndti', 'satvi', 'sti', 'vari',
    ('evi-toa', # nir, red, blue, TOA version
     [('sentinel2/tiles/19TCH/2017010/19TCH_2017010_S2A_evi-toa.tif',
       'hash',
       'sha256',
       '0d68b587a7a84c4287c5aa8621c82aa0d8be237a1b1e80f7ac4855dfdd4fe9ec')],
    ),
    # t_process[crcm] recording:
    ('crcm', # swir1, swir2, green, surface version
     [('sentinel2/tiles/19TCH/2017010/19TCH_2017010_S2A_crcm.tif',
       'hash',
       'sha256',
       '5cc5d30a22fc2e24f636f1c6dc722160cb0c5eb502ed803e4ff94290ecee1109')],
    ),
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
