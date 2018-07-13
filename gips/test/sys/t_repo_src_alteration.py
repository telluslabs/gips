#TODO save the last remaining test?
#import os
#import logging
#from datetime import datetime
#
#import pytest
#
#from .util import *
#
#def t_modis_archive(careful_repo_env, repo_env, expected):
#    """Test gips_archive modis using faked source/asset files."""
#    files = ( # list of fake files
#        'MCD43A4.A2012337.h12v04.006.2016112013509.hdf',
#        'MOD11A2.A2012337.h12v04.005.2012346152330.hdf',
#        'MYD10A1.A2012337.h12v04.005.2012340112013.hdf',
#        'MOD11A1.A2012337.h12v04.005.2012339204007.hdf',
#        'MYD11A1.A2012337.h12v04.005.2012341072847.hdf',
#        'MOD10A1.A2012337.h12v04.005.2012340033542.hdf',
#        'MCD43A2.A2012337.h12v04.006.2016112013509.hdf',
#        'MOD10A1.A2012336.h12v04.005.2012339213007.hdf',
#        'MCD43A2.A2012336.h12v04.006.2016112010833.hdf',
#        'MYD11A1.A2012336.h12v04.005.2012341040543.hdf',
#        'MYD10A1.A2012336.h12v04.005.2012340031954.hdf',
#        'MOD11A1.A2012336.h12v04.005.2012339180517.hdf',
#        'MCD43A4.A2012336.h12v04.006.2016112010833.hdf',
#        'MCD43A2.A2012338.h12v04.006.2016112020013.hdf',
#        'MYD11A1.A2012338.h12v04.005.2012341075802.hdf',
#        'MOD10A1.A2012338.h12v04.005.2012341091201.hdf',
#        'MOD11A1.A2012338.h12v04.005.2012341041222.hdf',
#        'MYD10A1.A2012338.h12v04.005.2012340142152.hdf',
#        'MCD43A4.A2012338.h12v04.006.2016112020013.hdf', # this one should test --update
#    )
#    # put the faked assets into place in the stage, and a fake stale asset into the archive
#    for f in files:
#        careful_repo_env.writefile(os.path.join('modis/stage', f),
#                                   content='This file is named ' + f + '!')
#    stale_file_path = os.path.join(
#            DATA_REPO_ROOT,
#            'modis/tiles/h12v04/2012338/MCD43A4.A2012338.h12v04.005.2012120921015.hdf')
#    careful_repo_env.writefile(stale_file_path, content='This STALE file is named ' + f + '!')
#    careful_repo_env.run('gips_inventory', 'modis', '--rectify') # put the stale file in the DB
#
#    # run the test
#    stage_dir = os.path.join(DATA_REPO_ROOT, 'modis/stage')
#    actual = careful_repo_env.run('gips_archive', 'modis', '--update', cwd=stage_dir)
#    inv_actual = repo_env.run('gips_inventory', 'modis')
#
#    assert (expected._post_archive_inv_stdout == inv_actual.stdout and
#            expected.created == actual.created and
#            expected.deleted == actual.deleted)
