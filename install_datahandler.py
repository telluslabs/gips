#!/usr/bin/env python

import sys
import lsb_release as lsb
import apt
import pip
from glob import glob
from commands import getstatusoutput


GIPS_VERSION = "bs-deploy-lxc-edit" # branch or tag to install from

LSB_INFO = lsb.get_lsb_information()

GIPPY_PKGS = (
    "gfortran libboost-all-dev "
    "libfreetype6-dev libgnutls-dev libatlas-base-dev "
    "libgdal-dev libgdal1-dev gdal-bin python-numpy "
    "python-scipy python-gdal swig2.0"
).split(" ")

PG_PKGS = (
    "libpq-dev python-dev postgresql postgresql-contrib"
).split(" ")

DH_RQ_PKGS = ('redis-server',)

DH_TORQUE_PKGS = (
    "torque-client torque-common torque-mom torque-pam "
    "torque-scheduler torque-server"
).split(" ")

if LSB_INFO['ID'] == "Ubuntu":
    UBU_REL = LSB_INFO['RELEASE']

if UBU_REL == "14.04":
    SYS_PKGS.append("swig")
elif UBU_REL == "16.04":
    pass
else:
    sys.stdout.write("only Ubuntu 16.04 or 14.04 are supported at this time.")
    sys.exit(-1)


def install_system_requirements(PKGS):
    '''
    Install system required packages.

    Using system call for now.  Was using python-apt library but started
    getting error that didn't occur in system call (see
    'this_worked_until_recently' below). 
    '''
    cmd = 'apt-get install -y {}'.format(
        ' '.join(PKGS)
    )
    print('running: ' + cmd)
    status, output = getstatusoutput(cmd)
    if status != 0:
        print output
        sys.exit(-9999)
    # geting error message about libgif7
    #    Sorry, package installation failed [E:Can't find a source to download
    #               version '5.1.4-0.3~16.04' of 'libgif7:amd64'] 
    this_worked_until_recently = '''
    cache = apt.cache.Cache()
    cache.update()
    for pkg_name in PKGS:
        pkg = cache[pkg_name]
        if pkg.is_installed:
            print("{pkg_name} already installed".format(pkg_name=pkg_name))
        else:
            print('+++  mark_install {}'.format(pkg_name))
            cache[pkg_name].mark_install()

    try:
        cache.commit()
    except Exception, arg:
        sys.stderr.write("Sorry, package installation failed [{err}]\n".format(err=str(arg)))
        sys.stdout.flush()
        sys.exit(-9999)
    '''


def install_gips(gips_version=GIPS_VERSION, extras=()):
    if gips_version == '.':
        base_url = gips_version
    else:
        base_url = (
            'git+https://github.com/Applied-GeoSolutions/gips.git@{ver}#egg={ver}'
        ).format(ver=gips_version)
    url = base_url + '[{extras}]'.format(extras=','.join(extras))
    print url
    cmd = 'pip install --process-dependency-links {}'.format(url)
    print('running: ' + cmd)
    status, output = getstatusoutput(cmd)
    if status != 0:
        print output
        sys.exit(-9999)

    """
    pip_args = ['install', '--process-dependency-links', url]
    pip.main(args=pip_args)
    """


def setup_postgresql(db_host, db_name, db_user, db_password, **kwargs):
    user_add = (
        'echo "CREATE USER {db_user} WITH PASSWORD '
        "'{db_password}' "
        '\; " | sudo -u postgres -- psql'
    ).format(
        db_user=db_user, db_password=db_password
    )
    db_create = (
        'echo "CREATE DATABASE {db_name} OWNER {db_user} \; " | '
        'sudo -u postgres -- psql'
    ).format(
        db_name=db_name, db_user=db_user
    )
    for cmd in [user_add, db_create]:
        print('running: ' + cmd)
        status, output = getstatusoutput(cmd)
        if status != 0:
            raise Exception(output)
        print(output)
        print('---')


def main():
    import argparse
    p = argparse.ArgumentParser(description='GIPS deployment script')
    h = ('Directory where all drivers will be initially configured to store '
         'files.')
    p.add_argument('-r', '--repos-path', help=h, default='/var/gipsdata/')
    p.add_argument(
        '-e', '--email', default='icooke@ags.io',
        help='Set email address (used for anonymous FTP sources)',
    )
    p.add_argument(
        '-d', '--drivers', nargs='*',
        default=('modis', 'merra', 'landsat', 'aod'),
        help='List of drivers to enable for this installation',
    )
    p.add_argument(
        '-U', '--earthdata-user',
        help='Set username for EARTHDATA login', default=''
    )
    p.add_argument(
        '-P', '--earthdata-password',
        help='Set password for EARTHDATA login', default=''
    )
    p.add_argument(
        '-u', '--update',
        help='Overwrite any existing settings file with these options',
        default=False, action='store_true',
    )
    p.add_argument(
        '-T', '--task-queue', default='rq',
        help=('Which task queue to use for this gips.datahandler install.  '
              'Choices are "rq" or "torque"'),
    )
    p.add_argument(
        '-Q', '--queue-name', default='datahandler',
        help='Identifier of the queue to be used.'
    )
    p.add_argument(
        '-G', '--gips-version', default=(GIPS_VERSION),
        help='Version (tag or branch) of GIPS to install.'
    )
    p.add_argument(
        '--install-pg', default=False, action='store_true',
        help=('Install and setup postgres on the local machine.  '
              'Using the configuration specified in the `--db-X` options.')
    )
    p.add_argument(
        '--db-host', default='localhost', help='database server name/ip'
    ) 
    p.add_argument(
        '--db-user', default='geokit', help='database user name'
    )
    p.add_argument(
        '--db-password', default='geokitp4ss', help='database user password'
    )
    p.add_argument(
        '--db-port', default='5432', help='database server TCP port.'
    ) 
    p.add_argument(

        '--db-name', default='gkdb', help='Name of database on DB server.'
    ) 
    args = vars(p.parse_args())
    PKGS = GIPPY_PKGS
    if args['task_queue'] == 'rq':
        PKGS += DH_RQ_PKGS
    elif args['task_queue'] == 'torque':
        PKGS += DH_TORQUE_PKGS
    else:
        raise Exception('Unknown task-queue specified "{}"'.format(task_queue))
    
    if 'install_pg' in args:
        PKGS += PG_PKGS

    install_system_requirements(PKGS)
    install_gips(
        gips_version=GIPS_VERSION, extras=('dh-' + args['task_queue'],)
    )
    setup_postgresql(**args)

    from gips.scripts.config import configure_environment
    configure_environment(**args)
    # TODO: for driver in drivers: gips_inventory {driver} --rectify
    print("Don't forget to add your ~/.netrc file (until issue #201 is sorted)")


if __name__ == '__main__':
    main()
