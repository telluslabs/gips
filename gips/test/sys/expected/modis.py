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


t_process = {
    # 'landcover' [], # is annual, not available for the scene under test
    # weird symlink products:
    # t_process[quality] recording:
    'quality':
        [('data-root/modis/tiles/h12v04/2012336/h12v04_2012336_MCD_quality.tif',
          'symlink',
          'HDF4_EOS:EOS_GRID:"',
          '/data-root/modis/tiles/h12v04/2012336/MCD43A2.A2012336.h12v04.006.2016112010833.hdf":MOD_Grid_BRDF:Snow_BRDF_Albedo'),
         ('data-root/modis/tiles/h12v04/2012337/h12v04_2012337_MCD_quality.tif',
          'symlink',
          'HDF4_EOS:EOS_GRID:"',
          '/data-root/modis/tiles/h12v04/2012337/MCD43A2.A2012337.h12v04.006.2016112013509.hdf":MOD_Grid_BRDF:Snow_BRDF_Albedo'),
         ('data-root/modis/tiles/h12v04/2012338/h12v04_2012338_MCD_quality.tif',
          'symlink',
          'HDF4_EOS:EOS_GRID:"',
          '/data-root/modis/tiles/h12v04/2012338/MCD43A2.A2012338.h12v04.006.2016112020013.hdf":MOD_Grid_BRDF:Snow_BRDF_Albedo')],

    # t_process[temp8tn] recording:
    'temp8tn':
        [('data-root/modis/tiles/h12v04/2012337/h12v04_2012337_MOD_temp8tn.tif',
          'symlink',
          'HDF4_EOS:EOS_GRID:"',
          '/data-root/modis/tiles/h12v04/2012337/MOD11A2.A2012337.h12v04.006.2016137164847.hdf":MODIS_Grid_8Day_1km_LST:LST_Night_1km')],

    # t_process[temp8td] recording:
    'temp8td':
        [('data-root/modis/tiles/h12v04/2012337/h12v04_2012337_MOD_temp8td.tif',
          'symlink',
          'HDF4_EOS:EOS_GRID:"',
          '/data-root/modis/tiles/h12v04/2012337/MOD11A2.A2012337.h12v04.006.2016137164847.hdf":MODIS_Grid_8Day_1km_LST:LST_Day_1km')],

    # normal products
    # t_process[satvi] recording:
    'satvi':
        [('data-root/modis/tiles/h12v04/2012337/h12v04_2012337_MCD_satvi.tif',
          'hash',
          'sha256',
          '94bee7cecf0f0a227fd8532223f86de10e01c3e39d1dd70b7675d91b3ca338a4'),
         ('data-root/modis/tiles/h12v04/2012336/h12v04_2012336_MCD_satvi.tif',
          'hash',
          'sha256',
          '6397669a6cd62bb39813b9000d93ba50f4cabe73aebf1e6444f4e3be9f630e19'),
         ('data-root/modis/tiles/h12v04/2012338/h12v04_2012338_MCD_satvi.tif',
          'hash',
          'sha256',
          '6124ee615a4f522fdf966a5479d03d87934908e5090a192192f9700020f24760')],

    # t_process[ndti] recording:
    'ndti':
        [('data-root/modis/tiles/h12v04/2012338/h12v04_2012338_MCD_ndti.tif',
          'hash',
          'sha256',
          '025ea7a9204ae8ad0952a92b386bf735dbbce8337e336843476d3f227cf1f1ab'),
         ('data-root/modis/tiles/h12v04/2012337/h12v04_2012337_MCD_ndti.tif',
          'hash',
          'sha256',
          'b6baa8c7a3996f680c4177e4157c9275dd895c8e6350afa6ef564e673bb6a5f0'),
         ('data-root/modis/tiles/h12v04/2012336/h12v04_2012336_MCD_ndti.tif',
          'hash',
          'sha256',
          'a1c4f1161e8a584257352e76160319c39aa4605dd565d388d0116e193773771f')],

    # t_process[ndvi] recording:
    'ndvi':
        [('data-root/modis/tiles/h12v04/2012338/h12v04_2012338_MCD_ndvi.tif',
          'hash',
          'sha256',
          'efbeae3a1c5e59ccd54b6108e275f9a8f0059162ac2797f4d69b00acb80147b3'),
         ('data-root/modis/tiles/h12v04/2012336/h12v04_2012336_MCD_ndvi.tif',
          'hash',
          'sha256',
          'b56d5c96229a1ad4cdcbd09db10b19a216b4cde8a0ffd184ee5cf01a35ab2b46'),
         ('data-root/modis/tiles/h12v04/2012337/h12v04_2012337_MCD_ndvi.tif',
          'hash',
          'sha256',
          'd9ff5d2f85ac9a267a8f6b1aca34f62b8196721e212b1e092f82ce9f1e208c61')],

    # t_process[isti] recording:
    'isti':
        [('data-root/modis/tiles/h12v04/2012338/h12v04_2012338_MCD_isti.tif',
          'hash',
          'sha256',
          'c0a38d1cd00de52eacd8abcda714bfdaa575787e27b40dc0472ffca5ab1696c0'),
         ('data-root/modis/tiles/h12v04/2012337/h12v04_2012337_MCD_isti.tif',
          'hash',
          'sha256',
          'b1759c1008e5914b955c4a9f55572baa8f7c0310677264a1057329e236d826cb'),
         ('data-root/modis/tiles/h12v04/2012336/h12v04_2012336_MCD_isti.tif',
          'hash',
          'sha256',
          '677182d186dac992b52b93239af0f419536075c7cd467864fa544bcde4b89e69')],

    # t_process[ndvi8] recording:
    'ndvi8':
        [('data-root/modis/tiles/h12v04/2012337/h12v04_2012337_MOD_ndvi8.tif',
          'hash',
          'sha256',
          '93db24c18886fbac0b87d1404a0c80606a599cc55b02d745a09ffb051b8131ac')],

    # t_process[snow] recording:
    'snow':
        [('data-root/modis/tiles/h12v04/2012336/h12v04_2012336_MCD_snow.tif',
          'hash',
          'sha256',
          'bea7315b736a75bcf37df86089679845ac597f3fba5d5cd6e79f5516b9657faa'),
         ('data-root/modis/tiles/h12v04/2012337/h12v04_2012337_MCD_snow.tif',
          'hash',
          'sha256',
          'de979c1a0c616d7889dd5fd45816849f9c08df54167d7f3b40301d6ac4495778'),
         ('data-root/modis/tiles/h12v04/2012338/h12v04_2012338_MCD_snow.tif',
          'hash',
          'sha256',
          '5d9bbfff1522e74165cdd677f1580e9eb2236c2c5922a796a6c9ee0db24ae05a')],

    # t_process[fsnow] recording:
    'fsnow':
        [('data-root/modis/tiles/h12v04/2012336/h12v04_2012336_MCD_fsnow.tif',
          'hash',
          'sha256',
          '853a5ca95f21c4a745e41e4acc46a71a74c74e0cdd1cae9ed3dd31b2fef1ddbd'),
         ('data-root/modis/tiles/h12v04/2012337/h12v04_2012337_MCD_fsnow.tif',
          'hash',
          'sha256',
          '3a5f7c95fe60e5789919cf55d7f8e652e4d668c6eb63eaa53a82249c0ea19c5a'),
         ('data-root/modis/tiles/h12v04/2012338/h12v04_2012338_MCD_fsnow.tif',
          'hash',
          'sha256',
          'd09b8a12ad17a7e715ae2e988fbf683e5fe2df46e97e9ac3ebb4444c8b1c169d')],

    # t_process[crcm] recording:
    'crcm':
        [('data-root/modis/tiles/h12v04/2012338/h12v04_2012338_MCD_crcm.tif',
          'hash',
          'sha256',
          'a45c2fb16d871a919e0c803f80e1f3b4ec831472d0466c33741fcf8e8150f6ba'),
         ('data-root/modis/tiles/h12v04/2012337/h12v04_2012337_MCD_crcm.tif',
          'hash',
          'sha256',
          '9aa80c0e1fa1b62b0a41aed42eeaf84632845d74f29594dfee55c22673b0a6f5'),
         ('data-root/modis/tiles/h12v04/2012336/h12v04_2012336_MCD_crcm.tif',
          'hash',
          'sha256',
          'a28c7d280fb8dfe0fe1cc003e1001457abdf14acc5545b2a69b782cfbcce7b50')],

    # t_process[ndsi] recording:
    'ndsi':
        [('data-root/modis/tiles/h12v04/2012337/h12v04_2012337_MCD_ndsi.tif',
          'hash',
          'sha256',
          '1f91f738bbb28b3ebeba36affd8d0689e105e90e1547cca58497eb7c7fdf7346'),
         ('data-root/modis/tiles/h12v04/2012338/h12v04_2012338_MCD_ndsi.tif',
          'hash',
          'sha256',
          'a626d375fbe5094a5199fdfc2206cf94777ff574379b45811cf7a49055a9f6ec'),
         ('data-root/modis/tiles/h12v04/2012336/h12v04_2012336_MCD_ndsi.tif',
          'hash',
          'sha256',
          'cb2ca7461c65f66ddb13e804ae7fe8f54daaf620ade600efee24810d40d4eb34')],

    # t_process[brgt] recording:
    'brgt':
        [('data-root/modis/tiles/h12v04/2012338/h12v04_2012338_MCD_brgt.tif',
          'hash',
          'sha256',
          'bf6bad538c7c6e703bc2f39503c2f128fa8e988a533e302c0124e085735dfaf9'),
         ('data-root/modis/tiles/h12v04/2012337/h12v04_2012337_MCD_brgt.tif',
          'hash',
          'sha256',
          '5c72e8f37640ec6b4a5a33e18980d71c70482fc8f708ba25da73e074cf64729f'),
         ('data-root/modis/tiles/h12v04/2012336/h12v04_2012336_MCD_brgt.tif',
          'hash',
          'sha256',
          '3460d0d35e35540b55e9eda35f253af8d85eabb84c0c44cb5f9c02d43da7e20a')],

    # t_process[msavi2] recording:
    'msavi2':
        [('data-root/modis/tiles/h12v04/2012336/h12v04_2012336_MCD_msavi2.tif',
          'hash',
          'sha256',
          'd2c93798df10939ff8afb6cd23e18ac3281cfd844e45da47a29d0342c2b980e9'),
         ('data-root/modis/tiles/h12v04/2012337/h12v04_2012337_MCD_msavi2.tif',
          'hash',
          'sha256',
          '92fe4f40d051ef3f479bde76a67bfff978bc513893af5ed62e4a48e457daabad'),
         ('data-root/modis/tiles/h12v04/2012338/h12v04_2012338_MCD_msavi2.tif',
          'hash',
          'sha256',
          'f25bd2d58d3edae72b11e73c08341479dee13af80352a4749861b6a54a81b351')],

    # t_process[bi] recording:
    'bi':
        [('data-root/modis/tiles/h12v04/2012336/h12v04_2012336_MCD_bi.tif',
          'hash',
          'sha256',
          '28c181b8d210b71759589da53295cc894c9d12c74ff1f7b0a49b88f73664282e'),
         ('data-root/modis/tiles/h12v04/2012337/h12v04_2012337_MCD_bi.tif',
          'hash',
          'sha256',
          '45acfc9249e063b6b97f269338590d51e2334e9bc5df118613ad908c6f0a3f8e'),
         ('data-root/modis/tiles/h12v04/2012338/h12v04_2012338_MCD_bi.tif',
          'hash',
          'sha256',
          '8526cb96d59fc9549dc8535fc8128123b9d39a63a3b7cd97ee3e611b7eeadf6f')],

    # t_process[obstime] recording:
    'obstime':
        [('data-root/modis/tiles/h12v04/2012338/h12v04_2012338_MOD-MYD_obstime.tif',
          'hash',
          'sha256',
          '66e01c94910c4fdd4f6fb2ab99b0c2d0cb73618032783e3cbdf1867191981fdc'),
         ('data-root/modis/tiles/h12v04/2012337/h12v04_2012337_MOD-MYD_obstime.tif',
          'hash',
          'sha256',
          '117cea0497b3158b465dd7dd197c886ebb1acf5059ed83dfdd6b5d7e94bb5243'),
         ('data-root/modis/tiles/h12v04/2012336/h12v04_2012336_MOD-MYD_obstime.tif',
          'hash',
          'sha256',
          'b04d8b07ef83e479db5650a30c84513bde7d5b05dd68187782c057ea0fd3e537')],

    # t_process[lswi] recording:
    'lswi':
        [('data-root/modis/tiles/h12v04/2012336/h12v04_2012336_MCD_lswi.tif',
          'hash',
          'sha256',
          '8de7378cdba830171c8da94424bf7807fa6c8b12523e8b34175a4b17ec770a5d'),
         ('data-root/modis/tiles/h12v04/2012337/h12v04_2012337_MCD_lswi.tif',
          'hash',
          'sha256',
          '62de4bdafcc276e9c1c343f4e63f5dd06167e87f7712796f991e3a957f2b71de'),
         ('data-root/modis/tiles/h12v04/2012338/h12v04_2012338_MCD_lswi.tif',
          'hash',
          'sha256',
          'add051ef35d7ffff5eb68c48f8b8071f9cb493b5d3426867605d4c61746e3a26')],

    # t_process[vari] recording:
    'vari':
        [('data-root/modis/tiles/h12v04/2012336/h12v04_2012336_MCD_vari.tif',
          'hash',
          'sha256',
          '732d6d3d9fbe0e1b4616a3f8a91bf12d532598a0a02e8aab16c9a01c3ac56913'),
         ('data-root/modis/tiles/h12v04/2012337/h12v04_2012337_MCD_vari.tif',
          'hash',
          'sha256',
          '9875717cc5e1926f11378bbf16345dbade5a2badf9f3dd06844a77f94d80ef72'),
         ('data-root/modis/tiles/h12v04/2012338/h12v04_2012338_MCD_vari.tif',
          'hash',
          'sha256',
          '70fd19862ef4145c24f26a8a74cb748279b88fd973de935726ebef2294e17edd')],

    # t_process[evi] recording:
    'evi':
        [('data-root/modis/tiles/h12v04/2012338/h12v04_2012338_MCD_evi.tif',
          'hash',
          'sha256',
          '13548ae74456f08e6add657a637ca364626eafd2cc767724f57aac8ff93005bb'),
         ('data-root/modis/tiles/h12v04/2012337/h12v04_2012337_MCD_evi.tif',
          'hash',
          'sha256',
          '7b926f7004cd92f2ec604fc4e2cc1489f60a335e39f4954030332a012fd33f87'),
         ('data-root/modis/tiles/h12v04/2012336/h12v04_2012336_MCD_evi.tif',
          'hash',
          'sha256',
          '51db813a857f795817f529edd56d7134004566be46edab8a8dadc81286fb895f')],

    # t_process[clouds] recording:
    'clouds':
        [('data-root/modis/tiles/h12v04/2012338/h12v04_2012338_MOD_clouds.tif',
          'hash',
          'sha256',
          '26b3e7e695f08ec2e9fb26985f9d5e392f9e8cedc331ab6721ea8e48821d93f0'),
         ('data-root/modis/tiles/h12v04/2012336/h12v04_2012336_MOD_clouds.tif',
          'hash',
          'sha256',
          'c43eec8178d0521d20e2a5b6e9b61525007d80702c6dd705a3e52ed3a76a7b73'),
         ('data-root/modis/tiles/h12v04/2012337/h12v04_2012337_MOD_clouds.tif',
          'hash',
          'sha256',
          '24a6a7050c866eed989530bec45b72004097f1e36fcc0e686652b87723a86de4')],

    # t_process[temp] recording:
    'temp':
        [('data-root/modis/tiles/h12v04/2012336/h12v04_2012336_MOD-MYD_temp.tif',
          'hash',
          'sha256',
          'ead2622531929bba3192b8a6b609d5d920e79394ec577c5245d74d69593d827c'),
         ('data-root/modis/tiles/h12v04/2012337/h12v04_2012337_MOD-MYD_temp.tif',
          'hash',
          'sha256',
          '5d498bad2779f84289dfb75b14345d64d16b5bc7994b4aca6cd694f70b86064d'),
         ('data-root/modis/tiles/h12v04/2012338/h12v04_2012338_MOD-MYD_temp.tif',
          'hash',
          'sha256',
          '097f341fa917a0ec316c37d7907ff15b754dcd0925469be586016137ca47575f')],

    # t_process[sti] recording:
    'sti':
        [('data-root/modis/tiles/h12v04/2012336/h12v04_2012336_MCD_sti.tif',
          'hash',
          'sha256',
          '24e50766ec18826f30bbad07bc8f5a34e72f1966b325cc23f064aa5fd35dc24a'),
         ('data-root/modis/tiles/h12v04/2012338/h12v04_2012338_MCD_sti.tif',
          'hash',
          'sha256',
          'c223de9d00e9cfedc0cfc13a45163535f3c59e5587642fa2c725b00b17b7437c'),
         ('data-root/modis/tiles/h12v04/2012337/h12v04_2012337_MCD_sti.tif',
          'hash',
          'sha256',
          '73c247fd2c7623e79145b6337846c97d14d1752d660b2f32245a4ccaac033350')],

    # t_process[crc] recording:
    'crc':
        [('data-root/modis/tiles/h12v04/2012338/h12v04_2012338_MCD_crc.tif',
          'hash',
          'sha256',
          '07debf171aedfeba7d6c1e3220ff8e4a2a7b1033e68c72bbc121b500b6ed3c9c'),
         ('data-root/modis/tiles/h12v04/2012337/h12v04_2012337_MCD_crc.tif',
          'hash',
          'sha256',
          'a7b61aabc950be7a3040b6f9572bf755522b12ad27644583e603def05ac1980b'),
         ('data-root/modis/tiles/h12v04/2012336/h12v04_2012336_MCD_crc.tif',
          'hash',
          'sha256',
          '942efeeee2b020123be6d7334bbb3ef5995c93d2fd0247cb79948836865c8067')],
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

t_stats = { 'created': {
    'clouds_stats.txt': -142855826,
    'fsnow_stats.txt': 1649245444,
    'indices_stats.txt': -896610352,
    'ndvi8_stats.txt': -493982920,
    'obstime_stats.txt': -1865008021,
    'quality_stats.txt': -914294800,
    'snow_stats.txt': 239300424,
    'temp8td_stats.txt': 1298400117,
    'temp8tn_stats.txt': -312645073,
    'temp_stats.txt': 2580004,
}}


t_gridded_export = { 'created': {
    '0': None,
    '0/2005001_MCD_indices.tif': 1618619735,
}}


t_cubic_gridded_export = { 'created': {
    '0': None,
    '0/2005001_MCD_indices.tif': 1939857358,
}}
