import pytest

import util
from util import repo_wrapper
import driver_setup
from .expected import modis as expectations

params = [] # (driver, product)

params += [('modis', p) for p in (
    'ndvi8', 'temp8td', 'temp8tn', #Terra 8-day Products
    'quality', #Nadir BRDF-Adjusted 16-day Products'
    'clouds', #Standard Products'
    'fsnow', 'obstime', 'snow', 'temp', #Terra/Aqua Daily Products'
    #Index Products'
    'bi', 'brgt', 'crc', 'crcm', 'evi', 'isti', 'lswi',
    'msavi2', 'ndsi', 'ndti', 'ndvi', 'satvi', 'sti', 'vari',
    #'indices', deprecated; not testing as a result
    #'landcover', is annual, not available for the scene under test
)]

#params += [('modis', p) for p in (
#)]

expectations = {
  'modis': {
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
  },
}

@pytest.mark.parametrize("driver, product", params)
def t_process(repo_wrapper, driver, product):
    """Test gips_process output."""
    record_mode, _, runner = repo_wrapper
    driver_setup.setup_repo_data(driver)
    args = ('gips_process',) + driver_setup.STD_ARGS[driver] + ('-p', product)
    outcome, actual = runner(*args)
    if not record_mode: # don't evaluate assertions when in record-mode
        assert (outcome.exit_code == 0
                and expectations[driver][product] == actual)
