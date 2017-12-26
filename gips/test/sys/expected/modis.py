"""Known-good outcomes for tests, mostly stdout and created files."""

t_inventory = { 'stdout': u"""\x1b[1mGIPS Data Inventory (v0.8.2)\x1b[0m
Retrieving inventory for site NHseacoast-0

\x1b[1mAsset Coverage for site NHseacoast-0\x1b[0m
\x1b[1m
Tile Coverage
\x1b[4m  Tile      % Coverage   % Tile Used\x1b[0m
  h12v04      100.0%        0.2%

\x1b[1m\x1b[4m    DATE     MCD12Q1   MCD43A2   MCD43A4   MOD09Q1   MOD10A1   MOD10A2   MOD11A1   MOD11A2   MYD10A1   MYD10A2   MYD11A1   MYD11A2   Product  \x1b[0m
\x1b[1m2012        
\x1b[0m    336                 100.0%     100.0%               100.0%               100.0%               100.0%               100.0%             
    337                 100.0%     100.0%     100.0%     100.0%               100.0%     100.0%     100.0%               100.0%             
    338                 100.0%     100.0%               100.0%               100.0%               100.0%               100.0%             


3 files on 3 dates
\x1b[1m
SENSORS\x1b[0m
\x1b[35mMCD: Aqua/Terra Combined\x1b[0m
\x1b[31mMOD: Terra\x1b[0m
\x1b[32mMOD-MYD: Aqua/Terra together\x1b[0m
\x1b[34mMYD: Aqua\x1b[0m
"""
}

# trailing whitespace and other junk characters are in current output
t_info = { 'stdout':  u"""\x1b[1mGIPS Data Repositories (v0.8.2)\x1b[0m
\x1b[1m
Modis Products v1.0.0\x1b[0m
\x1b[1m
Terra 8-day Products
\x1b[0m   ndvi8       Normalized Difference Vegetation Index: 250m
   temp8td     Surface temperature: 1km                
   temp8tn     Surface temperature: 1km                
\x1b[1m
Nadir BRDF-Adjusted 16-day Products
\x1b[0m   indices     Land indices                            
   quality     MCD Product Quality                     
\x1b[1m
Terra/Aqua Daily Products
\x1b[0m   fsnow       Fractional snow cover data              
   obstime     MODIS Terra/Aqua overpass time          
   snow        Snow and ice cover data                 
   temp        Surface temperature data                
\x1b[1m
Standard Products
\x1b[0m   clouds      Cloud Mask                              
   landcover   MCD Annual Land Cover                   
"""}

t_project = {
    # t_project[satvi] recording:
    'satvi':
        [('output/0/2012336_MCD_satvi.tif',
          'hash',
          'sha256',
          '893d968ff6359d0d34f8a587246690d1c724832505d66fbee8be8c1a43a6e3df'),
         ('output/0/2012337_MCD_satvi.tif',
          'hash',
          'sha256',
          '6092d7cfb609f000124b8ef107f278decaa27c3cdb69696bd094940ead97d96e'),
         ('output/0/2012338_MCD_satvi.tif',
          'hash',
          'sha256',
          '37dd32e0f5e761846f44615ec6e82e2cce8d6c98197f0bd721dcfb266d963b6b')],

    # t_project[ndti] recording:
    'ndti':
        [('output/0/2012337_MCD_ndti.tif',
          'hash',
          'sha256',
          'db85948227815660b94d570adf0f1119d9f1001284c3de6c8b219c6455bd3c4e'),
         ('output/0/2012338_MCD_ndti.tif',
          'hash',
          'sha256',
          '5028c194e41d8c07076cee09631b276ef7b86c3c45b0a4f705f5e4c6b72c2812'),
         ('output/0/2012336_MCD_ndti.tif',
          'hash',
          'sha256',
          '157134ea0e9cbb0b2fcdb4203e17e82ae906a5779eb1f735e8c55d1f60c231e1')],

    # t_project[ndvi] recording:
    'ndvi':
        [('output/0/2012337_MCD_ndvi.tif',
          'hash',
          'sha256',
          '28a288720a0846348fbd6315e5d9e3801ad76eb2c873dc028e7a52d1fdcdad10'),
         ('output/0/2012336_MCD_ndvi.tif',
          'hash',
          'sha256',
          '78e090b1cc92304c666a8e480d11fa99985ee3d2113c4fe3be29fb85910b86b9'),
         ('output/0/2012338_MCD_ndvi.tif',
          'hash',
          'sha256',
          'bbcee4ac1b49466c90264e305c20ce19a021fd177ffc35da5ed92a86555c480e')],

    # t_project[quality] recording:
    'quality':
        [('output/0/2012338_MCD_quality.tif',
          'hash',
          'sha256',
          '895abfc825d9da56c56202c670f94a16b28f2aaab5590db55ac6e903b6638e91'),
         ('output/0/2012336_MCD_quality.tif',
          'hash',
          'sha256',
          '4f40fdeb7ded507a68f404ec34a17fb6283c9b90d81ecccc7782746eaba85323'),
         ('output/0/2012337_MCD_quality.tif',
          'hash',
          'sha256',
          '5cdd315b2a423fbb82c19cfe859325c889a5d05cf0c3cdf71359b257524175a3')],

    # t_project[isti] recording:
    'isti':
        [('output/0/2012337_MCD_isti.tif',
          'hash',
          'sha256',
          '391367ee5bdd0a96435c09df85db312919121c5d9a28b5bda59a68db7b609871'),
         ('output/0/2012338_MCD_isti.tif',
          'hash',
          'sha256',
          'cc082d45a2a4dd4a7e53d0970029decf24ce5033b9715930cd250b524ad87757'),
         ('output/0/2012336_MCD_isti.tif',
          'hash',
          'sha256',
          '16be9705c06a44f3a35e684cded2d2ceb26213510eaf0ccfbafb62ebc39bb153')],

    # t_project[ndvi8] recording:
    'ndvi8':
        [('output/0/2012337_MOD_ndvi8.tif',
          'hash',
          'sha256',
          '23a72df39da253ac07de5a9e98c88f40e3335f3b1b779ccf91153d1d5573a780')],

    # t_project[snow] recording:
    'snow':
        [('output/0/2012336_MCD_snow.tif',
          'hash',
          'sha256',
          'b3eeca8fc933d2f43c2d96e869956447d9556737181635167744d0d420dfd813'),
         ('output/0/2012338_MCD_snow.tif',
          'hash',
          'sha256',
          '98a38e1a75fcea269bd75a952cde9d84af86b14ddb928e4777ff812dba8befbe'),
         ('output/0/2012337_MCD_snow.tif',
          'hash',
          'sha256',
          'da26696be559bb79c399ad18942ac629a9604d857dd7fc461fd76c4577a06303')],

    # t_project[fsnow] recording:
    'fsnow':
        [('output/0/2012338_MCD_fsnow.tif',
          'hash',
          'sha256',
          'f2efdf504e004caf05563f3402fdde7e771351d7d93de5970af0a54d0b5bd2c2'),
         ('output/0/2012336_MCD_fsnow.tif',
          'hash',
          'sha256',
          'a9d2ea29a6d77325246e0baaf298d16cb84d6003a19faed8ba162b475703f563'),
         ('output/0/2012337_MCD_fsnow.tif',
          'hash',
          'sha256',
          'e8465aa3764c60b21a943f3e078d93c0484272292f075455693ea2084971ace4')],

    # t_project[crcm] recording:
    'crcm':
        [('output/0/2012337_MCD_crcm.tif',
          'hash',
          'sha256',
          'c00e7b7c6970ae23904ee52afd614a8871f3d771d26830a2aef412163d9d9228'),
         ('output/0/2012338_MCD_crcm.tif',
          'hash',
          'sha256',
          'ed336a3ba4cf482936ca781ea1a5e0f04ca5ad68919c3dbe6e117edac55ec242'),
         ('output/0/2012336_MCD_crcm.tif',
          'hash',
          'sha256',
          'f217a9278b195e945e2337663cf7dfe2b09faa0dc68062fbc3614a6954866eaf')],

    # t_project[ndsi] recording:
    'ndsi':
        [('output/0/2012338_MCD_ndsi.tif',
          'hash',
          'sha256',
          '8e26a8f6d78b9612c8cd3924936c5944f56c67ae1c63f6541d045b41a27baafe'),
         ('output/0/2012337_MCD_ndsi.tif',
          'hash',
          'sha256',
          '2aaea763ab1d5b54d7079e7ee2381bd987a3c72c5cbbd6f18f97aa320c186e2a'),
         ('output/0/2012336_MCD_ndsi.tif',
          'hash',
          'sha256',
          '83b6bbf241d080cf6860798da299038be5e6d3e20a8b544e5af51e2eefd3a5c9')],

    # t_project[brgt] recording:
    'brgt':
        [('output/0/2012337_MCD_brgt.tif',
          'hash',
          'sha256',
          'fc385e6e42538a09655762d1b2557abe35af38aecef1571705cec8b971efbe4d'),
         ('output/0/2012338_MCD_brgt.tif',
          'hash',
          'sha256',
          'a8f8ef66bc87c2370bd61d5eed64905ba4f832d05579687478ff5f38c65e8038'),
         ('output/0/2012336_MCD_brgt.tif',
          'hash',
          'sha256',
          '24f8130de39daac6e181cb2f98b48d9a14412700632d3cbd2ffbe2704283b740')],

    # t_project[msavi2] recording:
    'msavi2':
        [('output/0/2012336_MCD_msavi2.tif',
          'hash',
          'sha256',
          '997b562420fe223677881d577cdb2100ee653ee932b9989b95f3089c0fe38352'),
         ('output/0/2012338_MCD_msavi2.tif',
          'hash',
          'sha256',
          '26a7ab45723856361d108064fe0c810535de75f272a733d86f66eeb8146dee35'),
         ('output/0/2012337_MCD_msavi2.tif',
          'hash',
          'sha256',
          'ee7b2006b79f65bdf11d77f678d66765abfcc024b7856ab296f855570efb9940')],

    # t_project[bi] recording:
    'bi':
        [('output/0/2012336_MCD_bi.tif',
          'hash',
          'sha256',
          'e5f891a6290301508107714657274fc808fcf96cb138c652a9c22552675796a5'),
         ('output/0/2012337_MCD_bi.tif',
          'hash',
          'sha256',
          '58b9e3809630ba24879bb85e81bc6dc0eed548348373588d70d49de65d246582'),
         ('output/0/2012338_MCD_bi.tif',
          'hash',
          'sha256',
          '914ca6d15c25a22d3e0a43d0d266f72bd65d102b4d6b015a9f12b8ee3a116c13')],

    # t_project[obstime] recording:
    'obstime':
        [('output/0/2012337_MOD-MYD_obstime.tif',
          'hash',
          'sha256',
          'a9345d21f3d754d083d3b4d13b059f2ffe07eb42ea9a0d6f3e40ef326e4ea75f'),
         ('output/0/2012336_MOD-MYD_obstime.tif',
          'hash',
          'sha256',
          'fac305543c4afbf76611900579cd5f37d63e7a45814c997dce40fc46a74f13e5'),
         ('output/0/2012338_MOD-MYD_obstime.tif',
          'hash',
          'sha256',
          'e18456caaf9a2dd005cc6568f7aa77ac534bfa24ec364d3af28affb4ae652de9')],

    # t_project[lswi] recording:
    'lswi':
        [('output/0/2012337_MCD_lswi.tif',
          'hash',
          'sha256',
          '586dd3782070b983b9d383161bed82bee21c54ad312d1c993b0329965144deab'),
         ('output/0/2012336_MCD_lswi.tif',
          'hash',
          'sha256',
          '296c849e70d31127bcefef54ffed72832529f7ae60d50b7c639c5c6d253d30f4'),
         ('output/0/2012338_MCD_lswi.tif',
          'hash',
          'sha256',
          '992fa3d7b4bdc8cf95fba759a0096f9a913e84762717e93c477baae0d7d3c0ed')],

    # t_project[vari] recording:
    'vari':
        [('output/0/2012336_MCD_vari.tif',
          'hash',
          'sha256',
          'be5d2273b9f0b9aca79df89b66ca0e7e1a2b8d386e6d34a6eca6eb37810b488d'),
         ('output/0/2012338_MCD_vari.tif',
          'hash',
          'sha256',
          '016ec5b1ee512d9306251a4c2b3630c90ea18723159a6a254c8e77c4e730abc8'),
         ('output/0/2012337_MCD_vari.tif',
          'hash',
          'sha256',
          'a6c10e80436b92908637b22b40e7993a0a648e82b96993760a7b26ba43df0667')],

    # t_project[evi] recording:
    'evi':
        [('output/0/2012338_MCD_evi.tif',
          'hash',
          'sha256',
          '8a1beba0730ac7d113a7edb8b55035a742892bbe678cd0eaaa540e59906a6990'),
         ('output/0/2012337_MCD_evi.tif',
          'hash',
          'sha256',
          '824a5247b0e8e0730dec6e82b390533649aa796ef04ef4be27ac38cae9a24d04'),
         ('output/0/2012336_MCD_evi.tif',
          'hash',
          'sha256',
          '361798060d02c97153a9828c1f8ac6b7df396070ec243932e9ed18fd472e9669')],

    # t_project[temp8tn] recording:
    'temp8tn':
        [('output/0/2012337_MOD_temp8tn.tif',
          'hash',
          'sha256',
          '1600d412e2590b4f4006ac0d98ebf9c6bf83fe16967c2fd721e412d2a14040c6')],

    # t_project[clouds] recording:
    'clouds':
        [('output/0/2012337_MOD_clouds.tif',
          'hash',
          'sha256',
          '8b13afeec6d1a5612a3eeb51896507e2d4eeb851261881f3854d2b804e97835f'),
         ('output/0/2012336_MOD_clouds.tif',
          'hash',
          'sha256',
          'cb4fab2519652bebe4830479c95425050f63d519397beb5b0c40349cc6f49372'),
         ('output/0/2012338_MOD_clouds.tif',
          'hash',
          'sha256',
          '54505d6d4063caa27fda74f5fdbb916c20d281f6e15deea28596c379ffa661e2')],

    # t_project[temp] recording:
    'temp':
        [('output/0/2012336_MOD-MYD_temp.tif',
          'hash',
          'sha256',
          '614023db948d0b0249057ca9c458356c2222e45224a726f87a7cf512cd87745c'),
         ('output/0/2012338_MOD-MYD_temp.tif',
          'hash',
          'sha256',
          '51864699b8347a30d9669ec41298665cd893a27516089cc21b4c3f03b3e65b2b'),
         ('output/0/2012337_MOD-MYD_temp.tif',
          'hash',
          'sha256',
          '29373079984e8aaf55add6a1fdd7bd766eb89a1c74ebc85674da54aeb643e3ef')],

    # t_project[temp8td] recording:
    'temp8td':
        [('output/0/2012337_MOD_temp8td.tif',
          'hash',
          'sha256',
          'eaa0ff94bb34cbad8d9c187b16c7cd2bd5948d1d94cf1caf30b0396ac7e8a735')],

    # t_project[sti] recording:
    'sti':
        [('output/0/2012337_MCD_sti.tif',
          'hash',
          'sha256',
          '9850777cae46b42fa3c8361849529e6f230dd1ce86fb6c6676aa8eb2768e71d5'),
         ('output/0/2012336_MCD_sti.tif',
          'hash',
          'sha256',
          'b7fde6a04ac091946553b25b1a26de806fa7f9c23e915b415034ef811aca1d16'),
         ('output/0/2012338_MCD_sti.tif',
          'hash',
          'sha256',
          'b2714cadf4e779c433415f194f366ac87877c60b383f46971843b4ab3a610fa9')],

    # t_project[crc] recording:
    'crc':
        [('output/0/2012338_MCD_crc.tif',
          'hash',
          'sha256',
          'dc9a4885e694fe7117cf10df11b5589745b4eb119d5f58f9d1c14e27d0eda333'),
         ('output/0/2012337_MCD_crc.tif',
          'hash',
          'sha256',
          '5688d80a613c28c657237186291a88ae786037a77dad0247c0bd734da214c927'),
         ('output/0/2012336_MCD_crc.tif',
          'hash',
          'sha256',
          '3df0003b6153970e73c46d5e999697ce5af268744274ccd3a4a2c14e3ae932cb')],
}

t_project_two_runs = t_project

t_project_no_warp = { 'created': {
    '0': None, # directory
    '0/2012336_MCD_fsnow.tif': -232655043,
    '0/2012336_MCD_indices.tif': 1748308005,
    '0/2012336_MCD_quality.tif': 1342857096,
    '0/2012336_MCD_snow.tif': 1704870455,
    '0/2012336_MOD-MYD_obstime.tif': -921877250,
    '0/2012336_MOD-MYD_temp.tif': -142389004,
    '0/2012336_MOD_clouds.tif': 792250507,
    '0/2012337_MCD_fsnow.tif': -118176399,
    '0/2012337_MCD_indices.tif': -558289948,
    '0/2012337_MCD_quality.tif': 1342857096,
    '0/2012337_MCD_snow.tif': -1562861219,
    '0/2012337_MOD-MYD_obstime.tif': -266130329,
    '0/2012337_MOD-MYD_temp.tif': 125915217,
    '0/2012337_MOD_clouds.tif': 1172608606,
    '0/2012337_MOD_ndvi8.tif': -996255186,
    '0/2012337_MOD_temp8td.tif': 1918564798,
    '0/2012337_MOD_temp8tn.tif': 1646469409,
    '0/2012338_MCD_fsnow.tif': -50404254,
    '0/2012338_MCD_indices.tif': 1361372393,
    '0/2012338_MCD_quality.tif': -429347844,
    '0/2012338_MCD_snow.tif': 415741551,
    '0/2012338_MOD-MYD_obstime.tif': -721900363,
    '0/2012338_MOD-MYD_temp.tif': -299932762,
    '0/2012338_MOD_clouds.tif': -1110899594,
}}

# TODO there should be something here but nothing is saved here during manual runs.
# See https://github.com/Applied-GeoSolutions/gips/issues/54
t_tiles = { 'created': {'h12v04': None}}

t_tiles_copy = { 'created': {
    'h12v04': None, # directory
    'h12v04/h12v04_2012336_MCD_fsnow.tif': 1284302156,
    'h12v04/h12v04_2012336_MCD_indices.tif': -2042919995,
    'h12v04/h12v04_2012336_MCD_quality.tif': 1121349116,
    'h12v04/h12v04_2012336_MCD_snow.tif': -2069225181,
    'h12v04/h12v04_2012336_MOD-MYD_obstime.tif': 808053323,
    'h12v04/h12v04_2012336_MOD-MYD_temp.tif': -1801734793,
    'h12v04/h12v04_2012336_MOD_clouds.tif': -221229092,
    'h12v04/h12v04_2012337_MCD_fsnow.tif': 1361214837,
    'h12v04/h12v04_2012337_MCD_indices.tif': -2147420472,
    'h12v04/h12v04_2012337_MCD_quality.tif': -1108654,
    'h12v04/h12v04_2012337_MCD_snow.tif': 1201721272,
    'h12v04/h12v04_2012337_MOD-MYD_obstime.tif': 673261584,
    'h12v04/h12v04_2012337_MOD-MYD_temp.tif': -1130082355,
    'h12v04/h12v04_2012337_MOD_clouds.tif': 1101505794,
    'h12v04/h12v04_2012337_MOD_ndvi8.tif': -181882164,
    'h12v04/h12v04_2012337_MOD_temp8td.tif': 868273975,
    'h12v04/h12v04_2012337_MOD_temp8tn.tif': 1173355207,
    'h12v04/h12v04_2012338_MCD_fsnow.tif': -647359984,
    'h12v04/h12v04_2012338_MCD_indices.tif': 1738864618,
    'h12v04/h12v04_2012338_MCD_quality.tif': 1379793143,
    'h12v04/h12v04_2012338_MCD_snow.tif': -1222056036,
    'h12v04/h12v04_2012338_MOD-MYD_obstime.tif': 411701973,
    'h12v04/h12v04_2012338_MOD-MYD_temp.tif': 1212632414,
    'h12v04/h12v04_2012338_MOD_clouds.tif': -2052728372,
}}

t_stats = {
    # t_stats[satvi] recording:
    'satvi':
        [('output/satvi_stats.txt',
          'text-full',
          ['date min max mean sd skew count\n',
           '2012-336 -0.1199 0.2757 0.188845 0.0394886 -2.85581 221002.0 \n',
           '2012-337 -0.1179 0.2955 0.189273 0.0399094 -2.7273 221002.0 \n',
           '2012-338 -0.1125 0.2985 0.187186 0.0408718 -2.44579 218582.0 \n'])],

    # t_stats[ndti] recording:
    'ndti':
        [('output/ndti_stats.txt',
          'text-full',
          ['date min max mean sd skew count\n',
           '2012-336 -1.0048 0.8895 0.31602 0.0595381 -2.46398 221002.0 \n',
           '2012-337 -0.643 0.9544 0.31893 0.0596861 -0.906354 221002.0 \n',
           '2012-338 -0.5051 0.9999 0.320866 0.064446 -0.195554 218582.0 \n'])],

    # t_stats[ndvi] recording:
    'ndvi':
        [('output/ndvi_stats.txt',
          'text-full',
          ['date min max mean sd skew count\n',
           '2012-336 -0.8893 0.8144 0.598198 0.130008 -4.50499 221002.0 \n',
           '2012-337 -0.9126 0.8198 0.598463 0.132692 -4.61097 221002.0 \n',
           '2012-338 -1.0001 0.8117 0.595837 0.134746 -4.68736 220979.0 \n'])],

    # t_stats[quality] recording:
    'quality':
        [('output/quality_stats.txt',
          'text-full',
          ['date min max mean sd skew count\n',
           '2012-336 0.0 0.0 0.0 0.0 nan 221002.0 \n',
           '2012-337 0.0 0.0 0.0 0.0 nan 221002.0 \n',
           '2012-338 0.0 0.0 0.0 0.0 nan 220979.0 \n'])],

    # t_stats[isti] recording:
    'isti':
        [('output/isti_stats.txt',
          'text-full',
          ['date min max mean sd skew count\n',
           '2012-336 0.0583 3.2766 0.522676 0.0837755 13.2684 220980.0 \n',
           '2012-337 0.0232 3.2766 0.519636 0.0845782 12.4045 221002.0 \n',
           '2012-338 -0.0001 3.0399 0.517872 0.0852503 7.69029 218582.0 \n'])],

    # t_stats[ndvi8] recording:
    'ndvi8':
        [('output/ndvi8_stats.txt',
          'text-full',
          ['date min max mean sd skew count\n',
           '2012-337 -1.9475 3.2766 0.612297 0.162128 -3.72226 220758.0 \n'])],

    # t_stats[snow] recording:
    'snow':
        [('output/snow_stats.txt',
          'text-full',
          ['date Snow Cover-min Snow Cover-max Snow Cover-mean Snow Cover-sd Snow Cover-skew Snow Cover-count Fractional Snow Cover-min Fractional Snow Cover-max Fractional Snow Cover-mean Fractional Snow Cover-sd Fractional Snow Cover-skew Fractional Snow Cover-count \n',
           '2012-336 0.0 100.0 66.0782 43.1646 -0.66934 2379.0  0.0 70.0 44.8928 24.6763 -0.938924 2379.0 \n',
           '2012-337 0.0 0.0 0.0 0.0 nan 677.0  0.0 0.0 0.0 0.0 nan 677.0 \n',
           '2012-338 0.0 100.0 7.3169 20.9113 2.95797 221002.0  0.0 38.0 0.358599 2.04345 8.82778 221002.0 \n'])],

    # t_stats[fsnow] recording:
    'fsnow':
        [('output/fsnow_stats.txt',
          'text-full',
          ['date min max mean sd skew count\n',
           '2012-336 0.0 70.0 36.4813 30.8325 -0.322887 2379.0 \n',
           '2012-337 0.0 0.0 0.0 0.0 nan 677.0 \n',
           '2012-338 0.0 35.0 0.0644655 1.11486 23.1911 221002.0 \n'])],

    # t_stats[crcm] recording:
    'crcm':
        [('output/crcm_stats.txt',
          'text-full',
          ['date min max mean sd skew count\n',
           '2012-336 -0.8857 1.6238 0.960025 0.21929 -3.32392 221002.0 \n',
           '2012-337 -0.8639 1.5786 0.966857 0.222374 -3.25955 221002.0 \n',
           '2012-338 -0.8744 1.8977 0.963618 0.23254 -2.82714 218582.0 \n'])],

    # t_stats[ndsi] recording:
    'ndsi':
        [('output/ndsi_stats.txt',
          'text-full',
          ['date min max mean sd skew count\n',
           '2012-336 -0.7313 1.0045 -0.58418 0.123674 6.27293 221002.0 \n',
           '2012-337 -0.731 0.9434 -0.58564 0.12352 6.14429 221002.0 \n',
           '2012-338 -0.7775 0.9329 -0.581803 0.125509 5.997 218582.0 \n'])],

    # t_stats[brgt] recording:
    'brgt':
        [('output/brgt_stats.txt',
          'text-full',
          ['date min max mean sd skew count\n',
           '2012-336 0.0062 0.1361 0.0467873 0.0103586 0.699293 221002.0 \n',
           '2012-337 0.0062 0.1379 0.0465373 0.0103964 0.708942 221002.0 \n',
           '2012-338 0.0064 0.1351 0.0464351 0.0105081 0.660629 220979.0 \n'])],

    # t_stats[msavi2] recording:
    'msavi2':
        [('output/msavi2_stats.txt',
          'text-full',
          ['date min max mean sd skew count\n',
           '2012-336 0.014 0.6976 0.503178 0.0608721 -2.7989 219182.0 \n',
           '2012-337 -0.0001 0.6996 0.502591 0.0601847 -2.75199 219026.0 \n',
           '2012-338 0.014 0.693 0.499838 0.0606011 -2.67091 219027.0 \n'])],

    # t_stats[bi] recording:
    'bi':
        [('output/bi_stats.txt',
          'text-full',
          ['date min max mean sd skew count\n',
           '2012-336 0.0033 0.1717 0.0948656 0.0173088 -1.23546 221002.0 \n',
           '2012-337 0.0033 0.1714 0.0944838 0.0173897 -1.24311 221002.0 \n',
           '2012-338 0.0038 0.1705 0.0938487 0.0174975 -1.19669 220979.0 \n'])],

    # t_stats[obstime] recording:
    'obstime':
        [('output/obstime_stats.txt',
          'text-full',
          ['date Observation Time Daytime Terra-min Observation Time Daytime Terra-max Observation Time Daytime Terra-mean Observation Time Daytime Terra-sd Observation Time Daytime Terra-skew Observation Time Daytime Terra-count Observation Time Nighttime Terra-min Observation Time Nighttime Terra-max Observation Time Nighttime Terra-mean Observation Time Nighttime Terra-sd Observation Time Nighttime Terra-skew Observation Time Nighttime Terra-count Observation Time Daytime Aqua-min Observation Time Daytime Aqua-max Observation Time Daytime Aqua-mean Observation Time Daytime Aqua-sd Observation Time Daytime Aqua-skew Observation Time Daytime Aqua-count Observation Time Nighttime Aqua-min Observation Time Nighttime Aqua-max Observation Time Nighttime Aqua-mean Observation Time Nighttime Aqua-sd Observation Time Nighttime Aqua-skew Observation Time Nighttime Aqua-count \n',
           '2012-336 10.8 10.8 10.8 1.90735e-07 -0.999996 716.0  255.0 0.0 nan nan nan 0.0  255.0 0.0 nan nan nan 0.0  1.4 1.4 1.4 2.38419e-08 inf 6685.0 \n',
           '2012-337 255.0 0.0 nan nan nan 0.0  255.0 0.0 nan nan nan 0.0  255.0 0.0 nan nan nan 0.0  255.0 0.0 nan nan nan 0.0 \n',
           '2012-338 10.6 10.6 10.6 3.8147e-07 -1.0 184032.0  255.0 0.0 nan nan nan 0.0  12.3 12.3 12.3 1.90735e-07 -0.999996 216873.0  1.2 2.8 1.61335 0.700361 1.10413 181365.0 \n'])],

    # t_stats[lswi] recording:
    'lswi':
        [('output/lswi_stats.txt',
          'text-full',
          ['date min max mean sd skew count\n',
           '2012-336 -0.9413 1.004 0.0704005 0.0795676 -0.897423 221002.0 \n',
           '2012-337 -0.9644 0.879 0.068998 0.0814312 -1.75006 221002.0 \n',
           '2012-338 -1.0001 0.8591 0.0695461 0.0851064 -1.65515 218582.0 \n'])],

    # t_stats[vari] recording:
    'vari':
        [('output/vari_stats.txt',
          'text-full',
          ['date min max mean sd skew count\n',
           '2012-336 -0.2931 3.2766 -0.0579385 0.0896767 11.2112 221002.0 \n',
           '2012-337 -0.3266 3.2766 -0.0573387 0.109661 15.3818 221002.0 \n',
           '2012-338 -0.3817 3.2766 -0.0567795 0.115018 15.8625 220979.0 \n'])],

    # t_stats[evi] recording:
    'evi':
        [('output/evi_stats.txt',
          'text-full',
          ['date min max mean sd skew count\n',
           '2012-336 -0.0689 0.4391 0.251258 0.0534915 -2.19097 221002.0 \n',
           '2012-337 -0.0704 0.4432 0.250715 0.0535784 -2.20674 221002.0 \n',
           '2012-338 -0.0727 0.4339 0.248372 0.0536924 -2.14955 220979.0 \n'])],

    # t_stats[temp8tn] recording:
    'temp8tn':
        [('output/temp8tn_stats.txt',
          'text-full',
          ['date min max mean sd skew count\n',
           '2012-337 267.02 280.38 273.055 1.35905 0.334532 212758.0 \n'])],

    # t_stats[clouds] recording:
    'clouds':
        [('output/clouds_stats.txt',
          'text-full',
          ['date min max mean sd skew count\n',
           '2012-336 0.0 1.0 0.990964 0.094628 -10.3767 221002.0 \n',
           '2012-337 0.0 1.0 0.998367 0.0403832 -24.6819 221002.0 \n',
           '2012-338 0.0 1.0 0.0838499 0.277163 3.00293 221002.0 \n'])],

    # t_stats[temp] recording:
    'temp':
        [('output/temp_stats.txt',
          'text-full',
          ['date Temperature Daytime Terra-min Temperature Daytime Terra-max Temperature Daytime Terra-mean Temperature Daytime Terra-sd Temperature Daytime Terra-skew Temperature Daytime Terra-count Temperature Nighttime Terra-min Temperature Nighttime Terra-max Temperature Nighttime Terra-mean Temperature Nighttime Terra-sd Temperature Nighttime Terra-skew Temperature Nighttime Terra-count Temperature Daytime Aqua-min Temperature Daytime Aqua-max Temperature Daytime Aqua-mean Temperature Daytime Aqua-sd Temperature Daytime Aqua-skew Temperature Daytime Aqua-count Temperature Nighttime Aqua-min Temperature Nighttime Aqua-max Temperature Nighttime Aqua-mean Temperature Nighttime Aqua-sd Temperature Nighttime Aqua-skew Temperature Nighttime Aqua-count Temperature Best Quality-min Temperature Best Quality-max Temperature Best Quality-mean Temperature Best Quality-sd Temperature Best Quality-skew Temperature Best Quality-count \n',
           '2012-336 267.44 267.9 267.67 0.140381 -0.244244 716.0  65535.0 0.0 nan nan nan 0.0  65535.0 0.0 nan nan nan 0.0  258.94 263.7 261.912 1.39539 -0.717615 6685.0  0.0 0.0 0.0 0.0 nan 221255.0 \n',
           '2012-337 65535.0 0.0 nan nan nan 0.0  65535.0 0.0 nan nan nan 0.0  65535.0 0.0 nan nan nan 0.0  65535.0 0.0 nan nan nan 0.0  0.0 0.0 0.0 0.0 nan 221255.0 \n',
           '2012-338 275.34 286.28 282.987 2.17515 -1.16826 184032.0  65535.0 0.0 nan nan nan 0.0  277.56 283.86 281.873 0.980026 -0.679654 216873.0  270.04 280.26 277.74 1.43805 -1.36599 181365.0  0.0 13.0 4.60988 3.26751 1.22493 221255.0 \n'])],

    # t_stats[temp8td] recording:
    'temp8td':
        [('output/temp8td_stats.txt',
          'text-full',
          ['date min max mean sd skew count\n',
           '2012-337 273.32 283.76 279.933 1.98691 -1.00057 218113.0 \n'])],

    # t_stats[sti] recording:
    'sti':
        [('output/sti_stats.txt',
          'text-full',
          ['date min max mean sd skew count\n',
           '2012-336 -0.0024 3.2766 1.94182 0.235117 0.707709 221002.0 \n',
           '2012-337 0.2173 3.2766 1.95394 0.239902 0.761782 221002.0 \n',
           '2012-338 0.3288 3.2766 1.96524 0.263691 0.833778 218582.0 \n'])],

    # t_stats[crc] recording:
    'crc':
        [('output/crc_stats.txt',
          'text-full',
          ['date min max mean sd skew count\n',
           '2012-336 -0.8526 2.1525 1.29852 0.263609 -2.37667 221002.0 \n',
           '2012-337 -0.868 2.2016 1.30555 0.268596 -2.32839 221002.0 \n',
           '2012-338 -0.8795 2.8088 1.30562 0.283586 -1.87226 218582.0 \n'])],
}


t_gridded_export = { 'created': {
    '0': None,
    '0/2005001_MCD_indices.tif': 1618619735,
}}


t_cubic_gridded_export = { 'created': {
    '0': None,
    '0/2005001_MCD_indices.tif': 1939857358,
}}
