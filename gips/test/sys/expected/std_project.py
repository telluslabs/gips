import collections

from .. import util

mark_spec = {}
expectations = {}

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

expectations['aod'] = {
    # t_project[aod] recording:
    'aod':
        [('0/2017004_MOD_aod.tif',
          'hash',
          'sha256',
          '2fe93815b6d1686fd357e8685c82ff23689d99200b3aec2654277fb6db86a8c7'),
         ('0/2017005_MOD_aod.tif',
          'hash',
          'sha256',
          '3830875aa1603cc86fc452286d365c1dcd12af60889f0761d8df3493c7541ef7'),
         ('0/2017006_MOD_aod.tif',
          'hash',
          'sha256',
          'ed9fc349c037f39eca87f2e7495024eeaf7fd0e99165ecb0f52cc7927e985977')],
}

expectations['prism'] = {
    # t_project[tmax] recording:
    'tmax':
        [('0/1982337_prism_tmax.tif',
          'hash',
          'sha256',
          '34354af37f2f9802c3c2a6e49437b14b1a61ddf3c378d2306df21dbcd8068abe'),
         ('0/1982336_prism_tmax.tif',
          'hash',
          'sha256',
          'ac083002cacf2fa456514c609e07256b08ac3fdcb8c870485145b34a113f65e0'),
         ('0/1982335_prism_tmax.tif',
          'hash',
          'sha256',
          '6e9b399a305ea1449d2c57752a7e013109b383de7414145017089858f1533dd3')],

    # t_project[pptsum] recording:
    'pptsum':
        [('0/1982337_prism_pptsum.tif',
          'hash',
          'sha256',
          '661586ac559c12a329375583f3ecee7c2837de6f276f9ee91e9b2c93b108f3ea')],

    # t_project[tmin] recording:
    'tmin':
        [('0/1982337_prism_tmin.tif',
          'hash',
          'sha256',
          'e60f8950f9a1ab4a1d192aab7bf4ccf577983d591cf3f2a488de10ce44568667'),
         ('0/1982336_prism_tmin.tif',
          'hash',
          'sha256',
          'a415b4b5df69bfc2ece115784f29151d6be95d8f2cc478d8c8c42e317c394129'),
         ('0/1982335_prism_tmin.tif',
          'hash',
          'sha256',
          'cc22853f539a0f4049d97f3e70f1af2d6aec7254504d42b11f9f41ce12bd1a68')],

    # t_project[ppt] recording:
    'ppt':
        [('0/1982336_prism_ppt.tif',
          'hash',
          'sha256',
          '452953fa26769ed0c3de1c698972baeede2749d6599408a4d2b67ae9bea3ca11'),
         ('0/1982337_prism_ppt.tif',
          'hash',
          'sha256',
          'f083e20b518336c4432c397d9ca35cf0d6a7da618cae230615580902fd70bca6'),
         ('0/1982335_prism_ppt.tif',
          'hash',
          'sha256',
          '46e0db478d2c9f9cb6ecd3d321c2ac9b69d30c6a5d2eb964ac6195d398fed661')],
}

# projection itself isn't terribly slow; possibly waiting on processing may
# be slow though
mark_spec['sentinel2'] = util.slow

expectations['sentinel2'] = collections.OrderedDict([
    # TODO acolite products; should use --acolite flag
    # acoflags fai oc2chl oc3chl rhow spm655 turbidity

    # t_project[ref-toa] recording,
    ('ref-toa',
     [('0/2017010_S2A_ref-toa.tif',
       'hash',
       'sha256',
       '36effec15edef46d27f534113dc35e9fed7b44fc33706cebcac8f14ba29fdc50')],
     ),
    # t_project[rad-toa] recording,
    ('rad-toa',
     [('0/2017010_S2A_rad-toa.tif',
       'hash',
       'sha256',
       '47b14e37f7ada44b978c7bbf3d6fcc51da3ccdcbdd05b01969fe1c548fb8503d')],
     ),
    # t_project[rad] recording,
    ('rad',
     [('0/2017010_S2A_rad.tif',
       'hash',
       'sha256',
       '3245e591f60bc8723264a3ed960ab6c46ecfa55db881c52feda0caafb2338429')],
     ),
    # t_project[ref] recording,
    ('ref',
     [('0/2017010_S2A_ref.tif',
       'hash',
       'sha256',
       'aeb96c9c7fb857864aa71ec49d4b90798846b160f7bdfe16bc507bd2953d7bc9')],
     ),
    # t_project[cfmask] recording,
    ('cfmask',
     [('0/2017010_S2A_cfmask.tif',
       'hash',
       'sha256',
       'dfd06798ff067a6139a6bf6f38234920d643693b95e5c7f319cb1de9ff161292')],
     ),
    # t_project[evi-toa] recording,
    ('evi-toa', # nir, red, blue, TOA version
     [('0/2017010_S2A_evi-toa.tif',
       'hash',
       'sha256',
       '3d4caaf7f9550c95f4e85ad87ed888f8d5bdd0e6be4d4da5a3d2868cf4f1b589')],
     ),
    # t_project[crcm] recording,
    ('crcm', # swir1, swir2, green, surface version
     [('0/2017010_S2A_crcm.tif',
       'hash',
       'sha256',
       '84fc07d6d0f6df0ec3e65300d51e09cf11363cb0ab1cffe26e034ca154e3aa41')],
     ),
])

mark_spec['landsat'] = util.slow
expectations['landsat'] = {
    # t_project[bqashadow] recording:
    'bqashadow':
        [('0/2017213_LC8_bqashadow.tif',
          'hash',
          'sha256',
          '0f4a69505d0d37a32a086848273704ce0d0d6bf5c84d0d72758e107fda55bf36')],

    # t_project[ndvi-toa] recording:
    'ndvi-toa':
        [('0/2017213_LC8_ndvi-toa.tif',
          'hash',
          'sha256',
          '21f2379aaf304fb26dc942c62f05a98bc14756ee89738d28bd8e373bb3cc10ac')],

    # t_project[acca] recording:
    'acca':
        [('0/2017213_LC8_acca.tif',
          'hash',
          'sha256',
          '056f1d96e76ebc147b341046e6021a2f2359361c8e88fafdbe255199242b9e4e')],

    # t_project[rad-toa] recording:
    'rad-toa':
        [('0/2017213_LC8_rad-toa.tif',
          'hash',
          'sha256',
          'b7ac9b05da84806de1b32de0cea35aca1dd6723fa6d5b687a3f607db95395aeb')],

    # t_project[ref-toa] recording:
    'ref-toa':
        [('0/2017213_LC8_ref-toa.tif',
          'hash',
          'sha256',
          '22f17fce8c02354a7180fd2739d1e9c6a5c0cd83c9991b6a1017bb2decc9736c')],
}
