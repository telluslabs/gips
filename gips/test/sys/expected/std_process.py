
import collections

from .. import util

expectations = {}
mark_spec = {}

expectations['modis'] = {
    # 'landcover' [], # is annual, not available for the scene under test
    # 'indices', deprecated; not testing as a result
    # weird symlink products:
    # t_process[quality] recording:
    'quality':
        [('modis/tiles/h12v04/2012336/h12v04_2012336_MCD_quality.tif',
          'symlink',
          'HDF4_EOS:EOS_GRID:"',
          '/modis/tiles/h12v04/2012336/MCD43A2.A2012336.h12v04.006.2016112010833.hdf":MOD_Grid_BRDF:Snow_BRDF_Albedo'),
         ('modis/tiles/h12v04/2012337/h12v04_2012337_MCD_quality.tif',
          'symlink',
          'HDF4_EOS:EOS_GRID:"',
          '/modis/tiles/h12v04/2012337/MCD43A2.A2012337.h12v04.006.2016112013509.hdf":MOD_Grid_BRDF:Snow_BRDF_Albedo'),
         ('modis/tiles/h12v04/2012338/h12v04_2012338_MCD_quality.tif',
          'symlink',
          'HDF4_EOS:EOS_GRID:"',
          '/modis/tiles/h12v04/2012338/MCD43A2.A2012338.h12v04.006.2016112020013.hdf":MOD_Grid_BRDF:Snow_BRDF_Albedo')],

    # t_process[temp8tn] recording:
    'temp8tn':
        [('modis/tiles/h12v04/2012337/h12v04_2012337_MOD_temp8tn.tif',
          'symlink',
          'HDF4_EOS:EOS_GRID:"',
          '/modis/tiles/h12v04/2012337/MOD11A2.A2012337.h12v04.006.2016137164847.hdf":MODIS_Grid_8Day_1km_LST:LST_Night_1km')],

    # t_process[temp8td] recording:
    'temp8td':
        [('modis/tiles/h12v04/2012337/h12v04_2012337_MOD_temp8td.tif',
          'symlink',
          'HDF4_EOS:EOS_GRID:"',
          '/modis/tiles/h12v04/2012337/MOD11A2.A2012337.h12v04.006.2016137164847.hdf":MODIS_Grid_8Day_1km_LST:LST_Day_1km')],

    # normal products
    # t_process[satvi] recording:
    'satvi':
        [('modis/tiles/h12v04/2012337/h12v04_2012337_MCD_satvi.tif',
          'hash',
          'sha256',
          '94bee7cecf0f0a227fd8532223f86de10e01c3e39d1dd70b7675d91b3ca338a4'),
         ('modis/tiles/h12v04/2012336/h12v04_2012336_MCD_satvi.tif',
          'hash',
          'sha256',
          '6397669a6cd62bb39813b9000d93ba50f4cabe73aebf1e6444f4e3be9f630e19'),
         ('modis/tiles/h12v04/2012338/h12v04_2012338_MCD_satvi.tif',
          'hash',
          'sha256',
          '6124ee615a4f522fdf966a5479d03d87934908e5090a192192f9700020f24760')],

    # t_process[ndti] recording:
    'ndti':
        [('modis/tiles/h12v04/2012338/h12v04_2012338_MCD_ndti.tif',
          'hash',
          'sha256',
          '025ea7a9204ae8ad0952a92b386bf735dbbce8337e336843476d3f227cf1f1ab'),
         ('modis/tiles/h12v04/2012337/h12v04_2012337_MCD_ndti.tif',
          'hash',
          'sha256',
          'b6baa8c7a3996f680c4177e4157c9275dd895c8e6350afa6ef564e673bb6a5f0'),
         ('modis/tiles/h12v04/2012336/h12v04_2012336_MCD_ndti.tif',
          'hash',
          'sha256',
          'a1c4f1161e8a584257352e76160319c39aa4605dd565d388d0116e193773771f')],

    # t_process[ndvi] recording:
    'ndvi':
        [('modis/tiles/h12v04/2012338/h12v04_2012338_MCD_ndvi.tif',
          'hash',
          'sha256',
          'efbeae3a1c5e59ccd54b6108e275f9a8f0059162ac2797f4d69b00acb80147b3'),
         ('modis/tiles/h12v04/2012336/h12v04_2012336_MCD_ndvi.tif',
          'hash',
          'sha256',
          'b56d5c96229a1ad4cdcbd09db10b19a216b4cde8a0ffd184ee5cf01a35ab2b46'),
         ('modis/tiles/h12v04/2012337/h12v04_2012337_MCD_ndvi.tif',
          'hash',
          'sha256',
          'd9ff5d2f85ac9a267a8f6b1aca34f62b8196721e212b1e092f82ce9f1e208c61')],

    # t_process[isti] recording:
    'isti':
        [('modis/tiles/h12v04/2012338/h12v04_2012338_MCD_isti.tif',
          'hash',
          'sha256',
          'c0a38d1cd00de52eacd8abcda714bfdaa575787e27b40dc0472ffca5ab1696c0'),
         ('modis/tiles/h12v04/2012337/h12v04_2012337_MCD_isti.tif',
          'hash',
          'sha256',
          'b1759c1008e5914b955c4a9f55572baa8f7c0310677264a1057329e236d826cb'),
         ('modis/tiles/h12v04/2012336/h12v04_2012336_MCD_isti.tif',
          'hash',
          'sha256',
          '677182d186dac992b52b93239af0f419536075c7cd467864fa544bcde4b89e69')],

    # t_process[ndvi8] recording:
    'ndvi8':
        [('modis/tiles/h12v04/2012337/h12v04_2012337_MOD_ndvi8.tif',
          'hash',
          'sha256',
          '93db24c18886fbac0b87d1404a0c80606a599cc55b02d745a09ffb051b8131ac')],

    # t_process[snow] recording:
    'snow':
        [('modis/tiles/h12v04/2012336/h12v04_2012336_MCD_snow.tif',
          'hash',
          'sha256',
          'bea7315b736a75bcf37df86089679845ac597f3fba5d5cd6e79f5516b9657faa'),
         ('modis/tiles/h12v04/2012337/h12v04_2012337_MCD_snow.tif',
          'hash',
          'sha256',
          'de979c1a0c616d7889dd5fd45816849f9c08df54167d7f3b40301d6ac4495778'),
         ('modis/tiles/h12v04/2012338/h12v04_2012338_MCD_snow.tif',
          'hash',
          'sha256',
          '5d9bbfff1522e74165cdd677f1580e9eb2236c2c5922a796a6c9ee0db24ae05a')],

    # t_process[fsnow] recording:
    'fsnow':
        [('modis/tiles/h12v04/2012336/h12v04_2012336_MCD_fsnow.tif',
          'hash',
          'sha256',
          '853a5ca95f21c4a745e41e4acc46a71a74c74e0cdd1cae9ed3dd31b2fef1ddbd'),
         ('modis/tiles/h12v04/2012337/h12v04_2012337_MCD_fsnow.tif',
          'hash',
          'sha256',
          '3a5f7c95fe60e5789919cf55d7f8e652e4d668c6eb63eaa53a82249c0ea19c5a'),
         ('modis/tiles/h12v04/2012338/h12v04_2012338_MCD_fsnow.tif',
          'hash',
          'sha256',
          'd09b8a12ad17a7e715ae2e988fbf683e5fe2df46e97e9ac3ebb4444c8b1c169d')],

    # t_process[crcm] recording:
    'crcm':
        [('modis/tiles/h12v04/2012338/h12v04_2012338_MCD_crcm.tif',
          'hash',
          'sha256',
          'a45c2fb16d871a919e0c803f80e1f3b4ec831472d0466c33741fcf8e8150f6ba'),
         ('modis/tiles/h12v04/2012337/h12v04_2012337_MCD_crcm.tif',
          'hash',
          'sha256',
          '9aa80c0e1fa1b62b0a41aed42eeaf84632845d74f29594dfee55c22673b0a6f5'),
         ('modis/tiles/h12v04/2012336/h12v04_2012336_MCD_crcm.tif',
          'hash',
          'sha256',
          'a28c7d280fb8dfe0fe1cc003e1001457abdf14acc5545b2a69b782cfbcce7b50')],

    # t_process[ndsi] recording:
    'ndsi':
        [('modis/tiles/h12v04/2012337/h12v04_2012337_MCD_ndsi.tif',
          'hash',
          'sha256',
          '1f91f738bbb28b3ebeba36affd8d0689e105e90e1547cca58497eb7c7fdf7346'),
         ('modis/tiles/h12v04/2012338/h12v04_2012338_MCD_ndsi.tif',
          'hash',
          'sha256',
          'a626d375fbe5094a5199fdfc2206cf94777ff574379b45811cf7a49055a9f6ec'),
         ('modis/tiles/h12v04/2012336/h12v04_2012336_MCD_ndsi.tif',
          'hash',
          'sha256',
          'cb2ca7461c65f66ddb13e804ae7fe8f54daaf620ade600efee24810d40d4eb34')],

    # t_process[brgt] recording:
    'brgt':
        [('modis/tiles/h12v04/2012338/h12v04_2012338_MCD_brgt.tif',
          'hash',
          'sha256',
          'bf6bad538c7c6e703bc2f39503c2f128fa8e988a533e302c0124e085735dfaf9'),
         ('modis/tiles/h12v04/2012337/h12v04_2012337_MCD_brgt.tif',
          'hash',
          'sha256',
          '5c72e8f37640ec6b4a5a33e18980d71c70482fc8f708ba25da73e074cf64729f'),
         ('modis/tiles/h12v04/2012336/h12v04_2012336_MCD_brgt.tif',
          'hash',
          'sha256',
          '3460d0d35e35540b55e9eda35f253af8d85eabb84c0c44cb5f9c02d43da7e20a')],

    # t_process[msavi2] recording:
    'msavi2':
        [('modis/tiles/h12v04/2012336/h12v04_2012336_MCD_msavi2.tif',
          'hash',
          'sha256',
          'd2c93798df10939ff8afb6cd23e18ac3281cfd844e45da47a29d0342c2b980e9'),
         ('modis/tiles/h12v04/2012337/h12v04_2012337_MCD_msavi2.tif',
          'hash',
          'sha256',
          '92fe4f40d051ef3f479bde76a67bfff978bc513893af5ed62e4a48e457daabad'),
         ('modis/tiles/h12v04/2012338/h12v04_2012338_MCD_msavi2.tif',
          'hash',
          'sha256',
          'f25bd2d58d3edae72b11e73c08341479dee13af80352a4749861b6a54a81b351')],

    # t_process[bi] recording:
    'bi':
        [('modis/tiles/h12v04/2012336/h12v04_2012336_MCD_bi.tif',
          'hash',
          'sha256',
          '28c181b8d210b71759589da53295cc894c9d12c74ff1f7b0a49b88f73664282e'),
         ('modis/tiles/h12v04/2012337/h12v04_2012337_MCD_bi.tif',
          'hash',
          'sha256',
          '45acfc9249e063b6b97f269338590d51e2334e9bc5df118613ad908c6f0a3f8e'),
         ('modis/tiles/h12v04/2012338/h12v04_2012338_MCD_bi.tif',
          'hash',
          'sha256',
          '8526cb96d59fc9549dc8535fc8128123b9d39a63a3b7cd97ee3e611b7eeadf6f')],

    # t_process[obstime] recording:
    'obstime':
        [('modis/tiles/h12v04/2012338/h12v04_2012338_MOD-MYD_obstime.tif',
          'hash',
          'sha256',
          '66e01c94910c4fdd4f6fb2ab99b0c2d0cb73618032783e3cbdf1867191981fdc'),
         ('modis/tiles/h12v04/2012337/h12v04_2012337_MOD-MYD_obstime.tif',
          'hash',
          'sha256',
          '117cea0497b3158b465dd7dd197c886ebb1acf5059ed83dfdd6b5d7e94bb5243'),
         ('modis/tiles/h12v04/2012336/h12v04_2012336_MOD-MYD_obstime.tif',
          'hash',
          'sha256',
          'b04d8b07ef83e479db5650a30c84513bde7d5b05dd68187782c057ea0fd3e537')],

    # t_process[lswi] recording:
    'lswi':
        [('modis/tiles/h12v04/2012336/h12v04_2012336_MCD_lswi.tif',
          'hash',
          'sha256',
          '8de7378cdba830171c8da94424bf7807fa6c8b12523e8b34175a4b17ec770a5d'),
         ('modis/tiles/h12v04/2012337/h12v04_2012337_MCD_lswi.tif',
          'hash',
          'sha256',
          '62de4bdafcc276e9c1c343f4e63f5dd06167e87f7712796f991e3a957f2b71de'),
         ('modis/tiles/h12v04/2012338/h12v04_2012338_MCD_lswi.tif',
          'hash',
          'sha256',
          'add051ef35d7ffff5eb68c48f8b8071f9cb493b5d3426867605d4c61746e3a26')],

    # t_process[vari] recording:
    'vari':
        [('modis/tiles/h12v04/2012336/h12v04_2012336_MCD_vari.tif',
          'hash',
          'sha256',
          '732d6d3d9fbe0e1b4616a3f8a91bf12d532598a0a02e8aab16c9a01c3ac56913'),
         ('modis/tiles/h12v04/2012337/h12v04_2012337_MCD_vari.tif',
          'hash',
          'sha256',
          '9875717cc5e1926f11378bbf16345dbade5a2badf9f3dd06844a77f94d80ef72'),
         ('modis/tiles/h12v04/2012338/h12v04_2012338_MCD_vari.tif',
          'hash',
          'sha256',
          '70fd19862ef4145c24f26a8a74cb748279b88fd973de935726ebef2294e17edd')],

    # t_process[evi] recording:
    'evi':
        [('modis/tiles/h12v04/2012338/h12v04_2012338_MCD_evi.tif',
          'hash',
          'sha256',
          '13548ae74456f08e6add657a637ca364626eafd2cc767724f57aac8ff93005bb'),
         ('modis/tiles/h12v04/2012337/h12v04_2012337_MCD_evi.tif',
          'hash',
          'sha256',
          '7b926f7004cd92f2ec604fc4e2cc1489f60a335e39f4954030332a012fd33f87'),
         ('modis/tiles/h12v04/2012336/h12v04_2012336_MCD_evi.tif',
          'hash',
          'sha256',
          '51db813a857f795817f529edd56d7134004566be46edab8a8dadc81286fb895f')],

    # t_process[clouds] recording:
    'clouds':
        [('modis/tiles/h12v04/2012338/h12v04_2012338_MOD_clouds.tif',
          'hash',
          'sha256',
          '26b3e7e695f08ec2e9fb26985f9d5e392f9e8cedc331ab6721ea8e48821d93f0'),
         ('modis/tiles/h12v04/2012336/h12v04_2012336_MOD_clouds.tif',
          'hash',
          'sha256',
          'c43eec8178d0521d20e2a5b6e9b61525007d80702c6dd705a3e52ed3a76a7b73'),
         ('modis/tiles/h12v04/2012337/h12v04_2012337_MOD_clouds.tif',
          'hash',
          'sha256',
          '24a6a7050c866eed989530bec45b72004097f1e36fcc0e686652b87723a86de4')],

    # t_process[temp] recording:
    'temp':
        [('modis/tiles/h12v04/2012336/h12v04_2012336_MOD-MYD_temp.tif',
          'hash',
          'sha256',
          'ead2622531929bba3192b8a6b609d5d920e79394ec577c5245d74d69593d827c'),
         ('modis/tiles/h12v04/2012337/h12v04_2012337_MOD-MYD_temp.tif',
          'hash',
          'sha256',
          '5d498bad2779f84289dfb75b14345d64d16b5bc7994b4aca6cd694f70b86064d'),
         ('modis/tiles/h12v04/2012338/h12v04_2012338_MOD-MYD_temp.tif',
          'hash',
          'sha256',
          '097f341fa917a0ec316c37d7907ff15b754dcd0925469be586016137ca47575f')],

    # t_process[sti] recording:
    'sti':
        [('modis/tiles/h12v04/2012336/h12v04_2012336_MCD_sti.tif',
          'hash',
          'sha256',
          '24e50766ec18826f30bbad07bc8f5a34e72f1966b325cc23f064aa5fd35dc24a'),
         ('modis/tiles/h12v04/2012338/h12v04_2012338_MCD_sti.tif',
          'hash',
          'sha256',
          'c223de9d00e9cfedc0cfc13a45163535f3c59e5587642fa2c725b00b17b7437c'),
         ('modis/tiles/h12v04/2012337/h12v04_2012337_MCD_sti.tif',
          'hash',
          'sha256',
          '73c247fd2c7623e79145b6337846c97d14d1752d660b2f32245a4ccaac033350')],

    # t_process[crc] recording:
    'crc':
        [('modis/tiles/h12v04/2012338/h12v04_2012338_MCD_crc.tif',
          'hash',
          'sha256',
          '07debf171aedfeba7d6c1e3220ff8e4a2a7b1033e68c72bbc121b500b6ed3c9c'),
         ('modis/tiles/h12v04/2012337/h12v04_2012337_MCD_crc.tif',
          'hash',
          'sha256',
          'a7b61aabc950be7a3040b6f9572bf755522b12ad27644583e603def05ac1980b'),
         ('modis/tiles/h12v04/2012336/h12v04_2012336_MCD_crc.tif',
          'hash',
          'sha256',
          '942efeeee2b020123be6d7334bbb3ef5995c93d2fd0247cb79948836865c8067')],
}

expectations['merra'] = {
    # test this too?  'frland': [],
    # t_process[srad] recording:
    'srad':
        [('merra/tiles/h01v01/2015135/h01v01_2015135_merra_srad.tif',
          'hash',
          'sha256',
          '882a44af70e337bf905c8695936f101792a518507a4304b23781a2f30aaabab4')],
    # t_process[tave] recording:
    'tave':
        [('merra/tiles/h01v01/2015135/h01v01_2015135_merra_tave.tif',
          'hash',
          'sha256',
          '5185aebd7cda54157cad2ddbde9f6fec4871c1b85fe78d0738634ba0211f2c9b')],
    # t_process[shum] recording:
    'shum':
        [('merra/tiles/h01v01/2015135/h01v01_2015135_merra_shum.tif',
          'hash',
          'sha256',
          '558f567c1e931891553d396f81b2b90929ad48a0ae88fa95d3894eae23ab3eba')],
    # t_process[rhum] recording:
    'rhum':
        [('merra/tiles/h01v01/2015135/h01v01_2015135_merra_rhum.tif',
          'hash',
          'sha256',
          '058161eb8488f1fb3df7f5c8719833c9d68c56aa082d4605938f62c2ee0035f6')],
    # t_process[tmin] recording:
    'tmin':
        [('merra/tiles/h01v01/2015135/h01v01_2015135_merra_tmin.tif',
          'hash',
          'sha256',
          '35a850769a3bb8f5209574ea4835bf417d8f99024567f4af9cdee9e623d0c567')],
    # t_process[tmax] recording:
    'tmax':
        [('merra/tiles/h01v01/2015135/h01v01_2015135_merra_tmax.tif',
          'hash',
          'sha256',
          '5963fcf346f388fc347355153996a078f1eb5ecbbc094394b72be382ba491865')],
    # t_process[prcp] recording:
    'prcp':
        [('merra/tiles/h01v01/2015135/h01v01_2015135_merra_prcp.tif',
          'hash',
          'sha256',
          '348fd7072ef0a8625f5268e29acbf3a69a959a412327102ef6558c992e62bc9f')],
    # t_process[patm] recording:
    'patm':
        [('merra/tiles/h01v01/2015135/h01v01_2015135_merra_patm.tif',
          'hash',
          'sha256',
          '7d9deca613973cb8ffb8f15a3dfa2013e6783556b520915e89b97fe41de638e3')],
    # t_process[wind] recording:
    'wind':
        [('merra/tiles/h01v01/2015135/h01v01_2015135_merra_wind.tif',
          'hash',
          'sha256',
          'a90c1d87fdb1c0926bd5b3004408a1f9d42ef08c38deb9d0572bc7536dbbf08a')],
}

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
