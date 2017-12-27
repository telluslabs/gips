import pytest

import util
from util import export_wrapper
import driver_setup

params = [] # (driver, product),...
expectations = {} #  'driver': {'product': [ (path, type, data...),...]...}

@pytest.mark.parametrize("driver, product", params)
def t_project(export_wrapper, driver, product):
    """Test gips_project with warping."""
    record_mode, runner = export_wrapper
    args = ('gips_project',) + driver_setup.STD_ARGS[driver] + (
        '--res', '100', '100', '--outdir', util.OUTPUT_DIR, '--notld',
        '-p', product)
    outcome, actual = runner(*args)
    if not record_mode: # don't evaluate assertions when in record-mode
        assert (outcome.exit_code == 0
                and expectations[driver][product] == actual)

expectations['modis'] = {
    # t_project[satvi] recording:
    'satvi':
        [('0/2012336_MCD_satvi.tif',
          'hash',
          'sha256',
          '893d968ff6359d0d34f8a587246690d1c724832505d66fbee8be8c1a43a6e3df'),
         ('0/2012337_MCD_satvi.tif',
          'hash',
          'sha256',
          '6092d7cfb609f000124b8ef107f278decaa27c3cdb69696bd094940ead97d96e'),
         ('0/2012338_MCD_satvi.tif',
          'hash',
          'sha256',
          '37dd32e0f5e761846f44615ec6e82e2cce8d6c98197f0bd721dcfb266d963b6b')],

    # t_project[ndti] recording:
    'ndti':
        [('0/2012337_MCD_ndti.tif',
          'hash',
          'sha256',
          'db85948227815660b94d570adf0f1119d9f1001284c3de6c8b219c6455bd3c4e'),
         ('0/2012338_MCD_ndti.tif',
          'hash',
          'sha256',
          '5028c194e41d8c07076cee09631b276ef7b86c3c45b0a4f705f5e4c6b72c2812'),
         ('0/2012336_MCD_ndti.tif',
          'hash',
          'sha256',
          '157134ea0e9cbb0b2fcdb4203e17e82ae906a5779eb1f735e8c55d1f60c231e1')],

    # t_project[ndvi] recording:
    'ndvi':
        [('0/2012337_MCD_ndvi.tif',
          'hash',
          'sha256',
          '28a288720a0846348fbd6315e5d9e3801ad76eb2c873dc028e7a52d1fdcdad10'),
         ('0/2012336_MCD_ndvi.tif',
          'hash',
          'sha256',
          '78e090b1cc92304c666a8e480d11fa99985ee3d2113c4fe3be29fb85910b86b9'),
         ('0/2012338_MCD_ndvi.tif',
          'hash',
          'sha256',
          'bbcee4ac1b49466c90264e305c20ce19a021fd177ffc35da5ed92a86555c480e')],

    # t_project[quality] recording:
    'quality':
        [('0/2012338_MCD_quality.tif',
          'hash',
          'sha256',
          '895abfc825d9da56c56202c670f94a16b28f2aaab5590db55ac6e903b6638e91'),
         ('0/2012336_MCD_quality.tif',
          'hash',
          'sha256',
          '4f40fdeb7ded507a68f404ec34a17fb6283c9b90d81ecccc7782746eaba85323'),
         ('0/2012337_MCD_quality.tif',
          'hash',
          'sha256',
          '5cdd315b2a423fbb82c19cfe859325c889a5d05cf0c3cdf71359b257524175a3')],

    # t_project[isti] recording:
    'isti':
        [('0/2012337_MCD_isti.tif',
          'hash',
          'sha256',
          '391367ee5bdd0a96435c09df85db312919121c5d9a28b5bda59a68db7b609871'),
         ('0/2012338_MCD_isti.tif',
          'hash',
          'sha256',
          'cc082d45a2a4dd4a7e53d0970029decf24ce5033b9715930cd250b524ad87757'),
         ('0/2012336_MCD_isti.tif',
          'hash',
          'sha256',
          '16be9705c06a44f3a35e684cded2d2ceb26213510eaf0ccfbafb62ebc39bb153')],

    # t_project[ndvi8] recording:
    'ndvi8':
        [('0/2012337_MOD_ndvi8.tif',
          'hash',
          'sha256',
          '23a72df39da253ac07de5a9e98c88f40e3335f3b1b779ccf91153d1d5573a780')],

    # t_project[snow] recording:
    'snow':
        [('0/2012336_MCD_snow.tif',
          'hash',
          'sha256',
          'b3eeca8fc933d2f43c2d96e869956447d9556737181635167744d0d420dfd813'),
         ('0/2012338_MCD_snow.tif',
          'hash',
          'sha256',
          '98a38e1a75fcea269bd75a952cde9d84af86b14ddb928e4777ff812dba8befbe'),
         ('0/2012337_MCD_snow.tif',
          'hash',
          'sha256',
          'da26696be559bb79c399ad18942ac629a9604d857dd7fc461fd76c4577a06303')],

    # t_project[fsnow] recording:
    'fsnow':
        [('0/2012338_MCD_fsnow.tif',
          'hash',
          'sha256',
          'f2efdf504e004caf05563f3402fdde7e771351d7d93de5970af0a54d0b5bd2c2'),
         ('0/2012336_MCD_fsnow.tif',
          'hash',
          'sha256',
          'a9d2ea29a6d77325246e0baaf298d16cb84d6003a19faed8ba162b475703f563'),
         ('0/2012337_MCD_fsnow.tif',
          'hash',
          'sha256',
          'e8465aa3764c60b21a943f3e078d93c0484272292f075455693ea2084971ace4')],

    # t_project[crcm] recording:
    'crcm':
        [('0/2012337_MCD_crcm.tif',
          'hash',
          'sha256',
          'c00e7b7c6970ae23904ee52afd614a8871f3d771d26830a2aef412163d9d9228'),
         ('0/2012338_MCD_crcm.tif',
          'hash',
          'sha256',
          'ed336a3ba4cf482936ca781ea1a5e0f04ca5ad68919c3dbe6e117edac55ec242'),
         ('0/2012336_MCD_crcm.tif',
          'hash',
          'sha256',
          'f217a9278b195e945e2337663cf7dfe2b09faa0dc68062fbc3614a6954866eaf')],

    # t_project[ndsi] recording:
    'ndsi':
        [('0/2012338_MCD_ndsi.tif',
          'hash',
          'sha256',
          '8e26a8f6d78b9612c8cd3924936c5944f56c67ae1c63f6541d045b41a27baafe'),
         ('0/2012337_MCD_ndsi.tif',
          'hash',
          'sha256',
          '2aaea763ab1d5b54d7079e7ee2381bd987a3c72c5cbbd6f18f97aa320c186e2a'),
         ('0/2012336_MCD_ndsi.tif',
          'hash',
          'sha256',
          '83b6bbf241d080cf6860798da299038be5e6d3e20a8b544e5af51e2eefd3a5c9')],

    # t_project[brgt] recording:
    'brgt':
        [('0/2012337_MCD_brgt.tif',
          'hash',
          'sha256',
          'fc385e6e42538a09655762d1b2557abe35af38aecef1571705cec8b971efbe4d'),
         ('0/2012338_MCD_brgt.tif',
          'hash',
          'sha256',
          'a8f8ef66bc87c2370bd61d5eed64905ba4f832d05579687478ff5f38c65e8038'),
         ('0/2012336_MCD_brgt.tif',
          'hash',
          'sha256',
          '24f8130de39daac6e181cb2f98b48d9a14412700632d3cbd2ffbe2704283b740')],

    # t_project[msavi2] recording:
    'msavi2':
        [('0/2012336_MCD_msavi2.tif',
          'hash',
          'sha256',
          '997b562420fe223677881d577cdb2100ee653ee932b9989b95f3089c0fe38352'),
         ('0/2012338_MCD_msavi2.tif',
          'hash',
          'sha256',
          '26a7ab45723856361d108064fe0c810535de75f272a733d86f66eeb8146dee35'),
         ('0/2012337_MCD_msavi2.tif',
          'hash',
          'sha256',
          'ee7b2006b79f65bdf11d77f678d66765abfcc024b7856ab296f855570efb9940')],

    # t_project[bi] recording:
    'bi':
        [('0/2012336_MCD_bi.tif',
          'hash',
          'sha256',
          'e5f891a6290301508107714657274fc808fcf96cb138c652a9c22552675796a5'),
         ('0/2012337_MCD_bi.tif',
          'hash',
          'sha256',
          '58b9e3809630ba24879bb85e81bc6dc0eed548348373588d70d49de65d246582'),
         ('0/2012338_MCD_bi.tif',
          'hash',
          'sha256',
          '914ca6d15c25a22d3e0a43d0d266f72bd65d102b4d6b015a9f12b8ee3a116c13')],

    # t_project[obstime] recording:
    'obstime':
        [('0/2012337_MOD-MYD_obstime.tif',
          'hash',
          'sha256',
          'a9345d21f3d754d083d3b4d13b059f2ffe07eb42ea9a0d6f3e40ef326e4ea75f'),
         ('0/2012336_MOD-MYD_obstime.tif',
          'hash',
          'sha256',
          'fac305543c4afbf76611900579cd5f37d63e7a45814c997dce40fc46a74f13e5'),
         ('0/2012338_MOD-MYD_obstime.tif',
          'hash',
          'sha256',
          'e18456caaf9a2dd005cc6568f7aa77ac534bfa24ec364d3af28affb4ae652de9')],

    # t_project[lswi] recording:
    'lswi':
        [('0/2012337_MCD_lswi.tif',
          'hash',
          'sha256',
          '586dd3782070b983b9d383161bed82bee21c54ad312d1c993b0329965144deab'),
         ('0/2012336_MCD_lswi.tif',
          'hash',
          'sha256',
          '296c849e70d31127bcefef54ffed72832529f7ae60d50b7c639c5c6d253d30f4'),
         ('0/2012338_MCD_lswi.tif',
          'hash',
          'sha256',
          '992fa3d7b4bdc8cf95fba759a0096f9a913e84762717e93c477baae0d7d3c0ed')],

    # t_project[vari] recording:
    'vari':
        [('0/2012336_MCD_vari.tif',
          'hash',
          'sha256',
          'be5d2273b9f0b9aca79df89b66ca0e7e1a2b8d386e6d34a6eca6eb37810b488d'),
         ('0/2012338_MCD_vari.tif',
          'hash',
          'sha256',
          '016ec5b1ee512d9306251a4c2b3630c90ea18723159a6a254c8e77c4e730abc8'),
         ('0/2012337_MCD_vari.tif',
          'hash',
          'sha256',
          'a6c10e80436b92908637b22b40e7993a0a648e82b96993760a7b26ba43df0667')],

    # t_project[evi] recording:
    'evi':
        [('0/2012338_MCD_evi.tif',
          'hash',
          'sha256',
          '8a1beba0730ac7d113a7edb8b55035a742892bbe678cd0eaaa540e59906a6990'),
         ('0/2012337_MCD_evi.tif',
          'hash',
          'sha256',
          '824a5247b0e8e0730dec6e82b390533649aa796ef04ef4be27ac38cae9a24d04'),
         ('0/2012336_MCD_evi.tif',
          'hash',
          'sha256',
          '361798060d02c97153a9828c1f8ac6b7df396070ec243932e9ed18fd472e9669')],

    # t_project[temp8tn] recording:
    'temp8tn':
        [('0/2012337_MOD_temp8tn.tif',
          'hash',
          'sha256',
          '1600d412e2590b4f4006ac0d98ebf9c6bf83fe16967c2fd721e412d2a14040c6')],

    # t_project[clouds] recording:
    'clouds':
        [('0/2012337_MOD_clouds.tif',
          'hash',
          'sha256',
          '8b13afeec6d1a5612a3eeb51896507e2d4eeb851261881f3854d2b804e97835f'),
         ('0/2012336_MOD_clouds.tif',
          'hash',
          'sha256',
          'cb4fab2519652bebe4830479c95425050f63d519397beb5b0c40349cc6f49372'),
         ('0/2012338_MOD_clouds.tif',
          'hash',
          'sha256',
          '54505d6d4063caa27fda74f5fdbb916c20d281f6e15deea28596c379ffa661e2')],

    # t_project[temp] recording:
    'temp':
        [('0/2012336_MOD-MYD_temp.tif',
          'hash',
          'sha256',
          '614023db948d0b0249057ca9c458356c2222e45224a726f87a7cf512cd87745c'),
         ('0/2012338_MOD-MYD_temp.tif',
          'hash',
          'sha256',
          '51864699b8347a30d9669ec41298665cd893a27516089cc21b4c3f03b3e65b2b'),
         ('0/2012337_MOD-MYD_temp.tif',
          'hash',
          'sha256',
          '29373079984e8aaf55add6a1fdd7bd766eb89a1c74ebc85674da54aeb643e3ef')],

    # t_project[temp8td] recording:
    'temp8td':
        [('0/2012337_MOD_temp8td.tif',
          'hash',
          'sha256',
          'eaa0ff94bb34cbad8d9c187b16c7cd2bd5948d1d94cf1caf30b0396ac7e8a735')],

    # t_project[sti] recording:
    'sti':
        [('0/2012337_MCD_sti.tif',
          'hash',
          'sha256',
          '9850777cae46b42fa3c8361849529e6f230dd1ce86fb6c6676aa8eb2768e71d5'),
         ('0/2012336_MCD_sti.tif',
          'hash',
          'sha256',
          'b7fde6a04ac091946553b25b1a26de806fa7f9c23e915b415034ef811aca1d16'),
         ('0/2012338_MCD_sti.tif',
          'hash',
          'sha256',
          'b2714cadf4e779c433415f194f366ac87877c60b383f46971843b4ab3a610fa9')],

    # t_project[crc] recording:
    'crc':
        [('0/2012338_MCD_crc.tif',
          'hash',
          'sha256',
          'dc9a4885e694fe7117cf10df11b5589745b4eb119d5f58f9d1c14e27d0eda333'),
         ('0/2012337_MCD_crc.tif',
          'hash',
          'sha256',
          '5688d80a613c28c657237186291a88ae786037a77dad0247c0bd734da214c927'),
         ('0/2012336_MCD_crc.tif',
          'hash',
          'sha256',
          '3df0003b6153970e73c46d5e999697ce5af268744274ccd3a4a2c14e3ae932cb')],
}

expectations['merra'] = {
    # t_project[srad] recording:
    'srad':
        [('0/2015135_merra_srad.tif',
          'hash',
          'sha256',
          'bfc0b906f7299ff8e6fcbbe474de0fb7b877d36f2e619e2e6ac10bd84ac5b55d')],

    # t_project[tave] recording:
    'tave':
        [('0/2015135_merra_tave.tif',
          'hash',
          'sha256',
          'c96d89ebf5d7ec90193c8a113609bfc39473d72041b6145a8cd41ee49e4f6a4d')],

    # t_project[prcp] recording:
    'prcp':
        [('0/2015135_merra_prcp.tif',
          'hash',
          'sha256',
          'b7e68237ee3557c421856203cc22807f1ce74790ea2948f8d095cbf8a7f18a53')],

    # t_project[rhum] recording:
    'rhum':
        [('0/2015135_merra_rhum.tif',
          'hash',
          'sha256',
          '3b45ba1cd87d4781ff95b08562a00189506c76add24156f8e3719ff8872c3d3a')],

    # t_project[tmin] recording:
    'tmin':
        [('0/2015135_merra_tmin.tif',
          'hash',
          'sha256',
          '253e37e9b2c03a77a0a4fdfe5aaa0e3ff025471f64fd28d6ffb33dd8ecdd68a9')],

    # t_project[tmax] recording:
    'tmax':
        [('0/2015135_merra_tmax.tif',
          'hash',
          'sha256',
          '8371d473f0e506e6ab0fe872542b8cd0d65bc2ed2b37bbeb747c966c41e9c232')],

    # t_project[shum] recording:
    'shum':
        [('0/2015135_merra_shum.tif',
          'hash',
          'sha256',
          '208465fbf10da2e935807e00991fa6375c3c6b67d9950362a9ffe502d7690fd6')],

    # t_project[patm] recording:
    'patm':
        [('0/2015135_merra_patm.tif',
          'hash',
          'sha256',
          '5778a4d89b22ea76dc25654c8092a61bbb09634f06f66b578460a93444e513a7')],

    # t_project[wind] recording:
    'wind':
        [('0/2015135_merra_wind.tif',
          'hash',
          'sha256',
          '88029a425fbeb59149a29be793087b51ea46583bb89e62c1baca629ccfc3a36a')],
}


params += [('modis', p) for p in expectations['modis'].keys()]
params += [('merra', p) for p in expectations['merra'].keys()]

