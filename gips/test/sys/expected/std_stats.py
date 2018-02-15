from .. import util

expectations = {}
mark_spec = {}

expectations['modis'] = {
    # t_stats[modis-satvi] recording:
    'satvi':
        [('satvi_stats.txt',
          'text-full',
          ['date,band,min,max,mean,sd,skew,count\r\n',
           '2012-336,satvi,-0.1199,0.2757,0.188845,0.0394886,-2.85581,221002.0\r\n',
           '2012-337,satvi,-0.1179,0.2955,0.189273,0.0399094,-2.7273,221002.0\r\n',
           '2012-338,satvi,-0.1125,0.2985,0.187186,0.0408718,-2.44579,218582.0\r\n'])],

    # t_stats[modis-ndti] recording:
    'ndti':
        [('ndti_stats.txt',
          'text-full',
          ['date,band,min,max,mean,sd,skew,count\r\n',
           '2012-336,ndti,-1.0048,0.8895,0.31602,0.0595381,-2.46398,221002.0\r\n',
           '2012-337,ndti,-0.643,0.9544,0.31893,0.0596861,-0.906354,221002.0\r\n',
           '2012-338,ndti,-0.5051,0.9999,0.320866,0.064446,-0.195554,218582.0\r\n'])],

    # t_stats[modis-ndvi] recording:
    'ndvi':
        [('ndvi_stats.txt',
          'text-full',
          ['date,band,min,max,mean,sd,skew,count\r\n',
           '2012-336,ndvi,-0.8893,0.8144,0.598198,0.130008,-4.50499,221002.0\r\n',
           '2012-337,ndvi,-0.9126,0.8198,0.598463,0.132692,-4.61097,221002.0\r\n',
           '2012-338,ndvi,-1.0001,0.8117,0.595837,0.134746,-4.68736,220979.0\r\n'])],

    # t_stats[modis-quality] recording:
    'quality':
        [('quality_stats.txt',
          'text-full',
          ['date,band,min,max,mean,sd,skew,count\r\n',
           '2012-336,Snow_BRDF_Albedo,0.0,0.0,0.0,0.0,nan,221002.0\r\n',
           '2012-337,Snow_BRDF_Albedo,0.0,0.0,0.0,0.0,nan,221002.0\r\n',
           '2012-338,Snow_BRDF_Albedo,0.0,0.0,0.0,0.0,nan,220979.0\r\n'])],

    # t_stats[modis-isti] recording:
    'isti':
        [('isti_stats.txt',
          'text-full',
          ['date,band,min,max,mean,sd,skew,count\r\n',
           '2012-336,isti,0.0583,3.2766,0.522676,0.0837755,13.2684,220980.0\r\n',
           '2012-337,isti,0.0232,3.2766,0.519636,0.0845782,12.4045,221002.0\r\n',
           '2012-338,isti,-0.0001,3.0399,0.517872,0.0852503,7.69029,218582.0\r\n'])],

    # t_stats[modis-ndvi8] recording:
    'ndvi8':
        [('ndvi8_stats.txt',
          'text-full',
          ['date,band,min,max,mean,sd,skew,count\r\n',
           '2012-337,ndvi,-1.9475,3.2766,0.612297,0.162128,-3.72226,220758.0\r\n'])],

    # t_stats[modis-crcm] recording:
    'crcm':
        [('crcm_stats.txt',
          'text-full',
          ['date,band,min,max,mean,sd,skew,count\r\n',
           '2012-336,crcm,-0.8857,1.6238,0.960025,0.21929,-3.32392,221002.0\r\n',
           '2012-337,crcm,-0.8639,1.5786,0.966857,0.222374,-3.25955,221002.0\r\n',
           '2012-338,crcm,-0.8744,1.8977,0.963618,0.23254,-2.82714,218582.0\r\n'])],

    # t_stats[modis-ndsi] recording:
    'ndsi':
        [('ndsi_stats.txt',
          'text-full',
          ['date,band,min,max,mean,sd,skew,count\r\n',
           '2012-336,ndsi,-0.7313,1.0045,-0.58418,0.123674,6.27293,221002.0\r\n',
           '2012-337,ndsi,-0.731,0.9434,-0.58564,0.12352,6.14429,221002.0\r\n',
           '2012-338,ndsi,-0.7775,0.9329,-0.581803,0.125509,5.997,218582.0\r\n'])],

    # t_stats[modis-evi] recording:
    'evi':
        [('evi_stats.txt',
          'text-full',
          ['date,band,min,max,mean,sd,skew,count\r\n',
           '2012-336,evi,-0.0689,0.4391,0.251258,0.0534915,-2.19097,221002.0\r\n',
           '2012-337,evi,-0.0704,0.4432,0.250715,0.0535784,-2.20674,221002.0\r\n',
           '2012-338,evi,-0.0727,0.4339,0.248372,0.0536924,-2.14955,220979.0\r\n'])],

    # t_stats[modis-msavi2] recording:
    'msavi2':
        [('msavi2_stats.txt',
          'text-full',
          ['date,band,min,max,mean,sd,skew,count\r\n',
           '2012-336,msavi2,0.014,0.6976,0.503178,0.0608721,-2.7989,219182.0\r\n',
           '2012-337,msavi2,-0.0001,0.6996,0.502591,0.0601847,-2.75199,219026.0\r\n',
           '2012-338,msavi2,0.014,0.693,0.499838,0.0606011,-2.67091,219027.0\r\n'])],

    # t_stats[modis-bi] recording:
    'bi':
        [('bi_stats.txt',
          'text-full',
          ['date,band,min,max,mean,sd,skew,count\r\n',
           '2012-336,bi,0.0033,0.1717,0.0948656,0.0173088,-1.23546,221002.0\r\n',
           '2012-337,bi,0.0033,0.1714,0.0944838,0.0173897,-1.24311,221002.0\r\n',
           '2012-338,bi,0.0038,0.1705,0.0938487,0.0174975,-1.19669,220979.0\r\n'])],

    # t_stats[modis-obstime] recording:
    'obstime':
        [('obstime_stats.txt',
          'text-full',
          ['date,band,min,max,mean,sd,skew,count\r\n',
           '2012-336,Observation Time Daytime Terra,10.8,10.8,10.8,1.90735e-07,-0.999996,716.0\r\n',
           '2012-336,Observation Time Nighttime Terra,255.0,0.0,nan,nan,nan,0.0\r\n',
           '2012-336,Observation Time Daytime Aqua,255.0,0.0,nan,nan,nan,0.0\r\n',
           '2012-336,Observation Time Nighttime Aqua,1.4,1.4,1.4,2.38419e-08,inf,6685.0\r\n',
           '2012-337,Observation Time Daytime Terra,255.0,0.0,nan,nan,nan,0.0\r\n',
           '2012-337,Observation Time Nighttime Terra,255.0,0.0,nan,nan,nan,0.0\r\n',
           '2012-337,Observation Time Daytime Aqua,255.0,0.0,nan,nan,nan,0.0\r\n',
           '2012-337,Observation Time Nighttime Aqua,255.0,0.0,nan,nan,nan,0.0\r\n',
           '2012-338,Observation Time Daytime Terra,10.6,10.6,10.6,3.8147e-07,-1.0,184032.0\r\n',
           '2012-338,Observation Time Nighttime Terra,255.0,0.0,nan,nan,nan,0.0\r\n',
           '2012-338,Observation Time Daytime Aqua,12.3,12.3,12.3,1.90735e-07,-0.999996,216873.0\r\n',
           '2012-338,Observation Time Nighttime Aqua,1.2,2.8,1.61335,0.700361,1.10413,181365.0\r\n'])],

    # t_stats[modis-lswi] recording:
    'lswi':
        [('lswi_stats.txt',
          'text-full',
          ['date,band,min,max,mean,sd,skew,count\r\n',
           '2012-336,lswi,-0.9413,1.004,0.0704005,0.0795676,-0.897423,221002.0\r\n',
           '2012-337,lswi,-0.9644,0.879,0.068998,0.0814312,-1.75006,221002.0\r\n',
           '2012-338,lswi,-1.0001,0.8591,0.0695461,0.0851064,-1.65515,218582.0\r\n'])],

    # t_stats[modis-vari] recording:
    'vari':
        [('vari_stats.txt',
          'text-full',
          ['date,band,min,max,mean,sd,skew,count\r\n',
           '2012-336,vari,-0.2931,3.2766,-0.0579385,0.0896767,11.2112,221002.0\r\n',
           '2012-337,vari,-0.3266,3.2766,-0.0573387,0.109661,15.3818,221002.0\r\n',
           '2012-338,vari,-0.3817,3.2766,-0.0567795,0.115018,15.8625,220979.0\r\n'])],

    # t_stats[modis-brgt] recording:
    'brgt':
        [('brgt_stats.txt',
          'text-full',
          ['date,band,min,max,mean,sd,skew,count\r\n',
           '2012-336,brgt,0.0062,0.1361,0.0467873,0.0103586,0.699293,221002.0\r\n',
           '2012-337,brgt,0.0062,0.1379,0.0465373,0.0103964,0.708942,221002.0\r\n',
           '2012-338,brgt,0.0064,0.1351,0.0464351,0.0105081,0.660629,220979.0\r\n'])],

    # t_stats[modis-temp8tn] recording:
    'temp8tn':
        [('temp8tn_stats.txt',
          'text-full',
          ['date,band,min,max,mean,sd,skew,count\r\n',
           '2012-337,8-day nighttime 1km grid Land-surface Temperature,267.02,280.38,273.055,1.35905,0.334532,212758.0\r\n'])],

    # t_stats[modis-clouds] recording:
    'clouds':
        [('clouds_stats.txt',
          'text-full',
          ['date,band,min,max,mean,sd,skew,count\r\n',
           '2012-336,Cloud Cover,0.0,0.0,0.0,0.0,nan,219250.0\r\n',
           '2012-337,Cloud Cover,0.0,0.0,0.0,0.0,nan,221002.0\r\n',
           '2012-338,Cloud Cover,0.0,0.0,0.0,0.0,nan,220060.0\r\n'])],

    # t_stats[modis-temp] recording:
    'temp':
        [('temp_stats.txt',
          'text-full',
          ['date,band,min,max,mean,sd,skew,count\r\n',
           '2012-336,Temperature Daytime Terra,267.44,267.9,267.67,0.140381,-0.244244,716.0\r\n',
           '2012-336,Temperature Nighttime Terra,65535.0,0.0,nan,nan,nan,0.0\r\n',
           '2012-336,Temperature Daytime Aqua,65535.0,0.0,nan,nan,nan,0.0\r\n',
           '2012-336,Temperature Nighttime Aqua,258.94,263.7,261.912,1.39539,-0.717615,6685.0\r\n',
           '2012-336,Temperature Best Quality,0.0,0.0,0.0,0.0,nan,221255.0\r\n',
           '2012-337,Temperature Daytime Terra,65535.0,0.0,nan,nan,nan,0.0\r\n',
           '2012-337,Temperature Nighttime Terra,65535.0,0.0,nan,nan,nan,0.0\r\n',
           '2012-337,Temperature Daytime Aqua,65535.0,0.0,nan,nan,nan,0.0\r\n',
           '2012-337,Temperature Nighttime Aqua,65535.0,0.0,nan,nan,nan,0.0\r\n',
           '2012-337,Temperature Best Quality,0.0,0.0,0.0,0.0,nan,221255.0\r\n',
           '2012-338,Temperature Daytime Terra,275.34,286.28,282.987,2.17515,-1.16826,184032.0\r\n',
           '2012-338,Temperature Nighttime Terra,65535.0,0.0,nan,nan,nan,0.0\r\n',
           '2012-338,Temperature Daytime Aqua,277.56,283.86,281.873,0.980026,-0.679654,216873.0\r\n',
           '2012-338,Temperature Nighttime Aqua,270.04,280.26,277.74,1.43805,-1.36599,181365.0\r\n',
           '2012-338,Temperature Best Quality,0.0,13.0,4.60988,3.26751,1.22493,221255.0\r\n'])],

    # t_stats[modis-temp8td] recording:
    'temp8td':
        [('temp8td_stats.txt',
          'text-full',
          ['date,band,min,max,mean,sd,skew,count\r\n',
           '2012-337,8-day daytime 1km grid Land-surface Temperature,273.32,283.76,279.933,1.98691,-1.00057,218113.0\r\n'])],

    # t_stats[modis-sti] recording:
    'sti':
        [('sti_stats.txt',
          'text-full',
          ['date,band,min,max,mean,sd,skew,count\r\n',
           '2012-336,sti,-0.0024,3.2766,1.94182,0.235117,0.707709,221002.0\r\n',
           '2012-337,sti,0.2173,3.2766,1.95394,0.239902,0.761782,221002.0\r\n',
           '2012-338,sti,0.3288,3.2766,1.96524,0.263691,0.833778,218582.0\r\n'])],

    # t_stats[modis-crc] recording:
    'crc':
        [('crc_stats.txt',
          'text-full',
          ['date,band,min,max,mean,sd,skew,count\r\n',
           '2012-336,crc,-0.8526,2.1525,1.29852,0.263609,-2.37667,221002.0\r\n',
           '2012-337,crc,-0.868,2.2016,1.30555,0.268596,-2.32839,221002.0\r\n',
           '2012-338,crc,-0.8795,2.8088,1.30562,0.283586,-1.87226,218582.0\r\n'])],

}

expectations['merra'] = {
    # t_stats[merra-srad] recording:
    'srad':
        [('srad_stats.txt',
          'text-full',
          ['date,band,min,max,mean,sd,skew,count\r\n',
           '2015-135,srad,3.4e+38,-3.4e+38,nan,nan,nan,0.0\r\n'])],

    # t_stats[merra-tave] recording:
    'tave':
        [('tave_stats.txt',
          'text-full',
          ['date,band,min,max,mean,sd,skew,count\r\n',
           '2015-135,tave,3.4e+38,-3.4e+38,nan,nan,nan,0.0\r\n'])],

    # t_stats[merra-prcp] recording:
    'prcp':
        [('prcp_stats.txt',
          'text-full',
          ['date,band,min,max,mean,sd,skew,count\r\n',
           '2015-135,prcp,3.4e+38,-3.4e+38,nan,nan,nan,0.0\r\n'])],

    # t_stats[merra-rhum] recording:
    'rhum':
        [('rhum_stats.txt',
          'text-full',
          ['date,band,min,max,mean,sd,skew,count\r\n',
           '2015-135,rhum,3.4e+38,-3.4e+38,nan,nan,nan,0.0\r\n'])],

    # t_stats[merra-tmin] recording:
    'tmin':
        [('tmin_stats.txt',
          'text-full',
          ['date,band,min,max,mean,sd,skew,count\r\n',
           '2015-135,tmin,3.4e+38,-3.4e+38,nan,nan,nan,0.0\r\n'])],

    # t_stats[merra-tmax] recording:
    'tmax':
        [('tmax_stats.txt',
          'text-full',
          ['date,band,min,max,mean,sd,skew,count\r\n',
           '2015-135,tmax,3.4e+38,-3.4e+38,nan,nan,nan,0.0\r\n'])],

    # t_stats[merra-shum] recording:
    'shum':
        [('shum_stats.txt',
          'text-full',
          ['date,band,min,max,mean,sd,skew,count\r\n',
           '2015-135,shum,3.4e+38,-3.4e+38,nan,nan,nan,0.0\r\n'])],

    # t_stats[merra-patm] recording:
    'patm':
        [('patm_stats.txt',
          'text-full',
          ['date,band,min,max,mean,sd,skew,count\r\n',
           '2015-135,patm,3.4e+38,-3.4e+38,nan,nan,nan,0.0\r\n'])],
}

expectations['aod'] = {
    # t_stats[aod-aod] recording:
    'aod':
        [('aod_stats.txt',
          'text-full',
          ['date,band,min,max,mean,sd,skew,count\r\n',
           '2017-004,,45.0,107.0,68.2053,27.2408,0.683439,2.70847e+06\r\n',
           '2017-005,,34.0,130.0,68.7497,33.5872,0.965031,4.54937e+06\r\n',
           '2017-006,,176.0,176.0,176.0,0.0,nan,927590.0\r\n'])],
}

expectations['prism'] = {
    # t_stats[prism-tmax] recording:
    'tmax':
        [('tmax_stats.txt',
          'text-full',
          ['date,band,min,max,mean,sd,skew,count\r\n',
           '1982-335,,6.68,10.74,9.45062,0.989373,-1.16521,221810.0\r\n',
           '1982-336,,7.63,11.52,10.2559,0.957033,-1.03102,221810.0\r\n',
           '1982-337,,12.97,15.32,14.5481,0.598565,-0.984863,221810.0\r\n'])],

    # t_stats[prism-pptsum] recording:
    'pptsum':
        [('pptsum_stats.txt',
          'text-full',
          ['date,band,min,max,mean,sd,skew,count\r\n',
           '1982-337,Cumulative Precipitate(3 day window),0.0,0.29,0.00668477,0.0376131,6.09544,221810.0\r\n'])],

    # t_stats[prism-tmin] recording:
    'tmin':
        [('tmin_stats.txt',
          'text-full',
          ['date,band,min,max,mean,sd,skew,count\r\n',
           '1982-335,,2.57,3.83,3.04506,0.268788,0.766181,221810.0\r\n',
           '1982-336,,-0.02,3.38,1.64335,0.757131,0.14854,221810.0\r\n',
           '1982-337,,1.11,3.17,2.11856,0.465469,0.147961,221810.0\r\n'])],

    # t_stats[prism-ppt] recording:
    'ppt':
        [('ppt_stats.txt',
          'text-full',
          ['date,band,min,max,mean,sd,skew,count\r\n',
           '1982-335,,0.0,0.0,0.0,0.0,nan,221810.0\r\n',
           '1982-336,,0.0,0.0,0.0,0.0,nan,221810.0\r\n',
           '1982-337,,0.0,0.29,0.00668477,0.0376131,6.09544,221810.0\r\n'])],

}

mark_spec['landsat'] = util.slow
expectations['landsat'] = {
    # t_stats[landsat-bqashadow] recording:
    'bqashadow':
        [('bqashadow_stats.txt',
          'text-full',
          ['date,band,min,max,mean,sd,skew,count\r\n',
           '2017-213,+shadow_smear,1.0,1.0,1.0,0.0,nan,220848.0\r\n'])],

    # t_stats[landsat-ndvi-toa] recording:
    'ndvi-toa':
        [('ndvi-toa_stats.txt',
          'text-full',
          ['date,band,min,max,mean,sd,skew,count\r\n',
           '2017-213,ndvi,-0.4883,0.8611,0.640444,0.223033,-2.00842,220848.0\r\n'])],

    # t_stats[landsat-ref-toa] recording:
    'ref-toa':
        [('ref-toa_stats.txt',
          'text-full',
          ['date,band,min,max,mean,sd,skew,count\r\n',
           '2017-213,COASTAL,0.0802,0.5848,0.103512,0.0411366,4.58853,220848.0\r\n',
           '2017-213,BLUE,0.0809,0.8259,0.114876,0.0599464,4.5467,220848.0\r\n',
           '2017-213,GREEN,0.053,0.8445,0.100936,0.0643648,4.42221,220848.0\r\n',
           '2017-213,RED,0.0231,0.6875,0.0563213,0.0549959,4.26371,220848.0\r\n',
           '2017-213,NIR,0.0142,1.0063,0.26515,0.0857833,-0.796907,220848.0\r\n',
           '2017-213,SWIR1,0.001,0.8389,0.161572,0.0813276,1.61928,220848.0\r\n',
           '2017-213,SWIR2,0.0003,0.596,0.071522,0.0625481,3.07293,220848.0\r\n',
           '2017-213,CIRRUS,0.0002,0.0152,0.00160228,0.000582327,7.07733,220848.0\r\n'])],

    # t_stats[landsat-acca] recording:
    'acca':
        [('acca_stats.txt',
          'text-full',
          ['date,band,min,max,mean,sd,skew,count\r\n',
           '2017-213,finalmask,1.0,1.0,1.0,0.0,nan,199899.0\r\n',
           '2017-213,cloudmask,1.0,1.0,1.0,0.0,nan,20949.0\r\n',
           '2017-213,ambclouds,1.0,1.0,1.0,0.0,nan,15396.0\r\n',
           '2017-213,pass1,1.0,1.0,1.0,0.0,nan,4642.0\r\n'])],

    # t_stats[landsat-rad-toa] recording:
    'rad-toa':
        [('rad-toa_stats.txt',
          'text-full',
          ['date,band,min,max,mean,sd,skew,count\r\n',
           '2017-213,COASTAL,56.1,409.4,72.4368,28.7988,4.58855,220848.0\r\n',
           '2017-213,BLUE,43.6,445.1,61.8659,32.3072,4.54671,220848.0\r\n',
           '2017-213,GREEN,25.6,408.0,48.7223,31.1024,4.42216,220848.0\r\n',
           '2017-213,RED,12.7,378.6,30.9724,30.2874,4.26369,220848.0\r\n',
           '2017-213,NIR,4.7,339.8,89.4949,28.9755,-0.796908,220848.0\r\n',
           '2017-213,SWIR1,0.0,54.9,10.4936,5.32891,1.61942,220848.0\r\n',
           '2017-213,SWIR2,-0.1,14.2,1.62182,1.50423,3.07054,220848.0\r\n',
           '2017-213,CIRRUS,-0.1,1.4,0.0702492,0.0691392,3.70532,220848.0\r\n'])],
}
