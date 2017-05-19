#!/usr/bin/env python

import sys
import lsb_release as lsb
#import apt
import getpass
import os
import pip
import subprocess
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
    cmd = 'sudo apt-get install -y {}'.format(
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
        dev_opt = '-e'
    else:
        base_url = (
            'git+https://github.com/Applied-GeoSolutions/gips.git@{ver}#egg={ver}'
        ).format(ver=gips_version)
        dev_opt = ''
    url = base_url + '[{extras}]'.format(extras=','.join(extras))
    print url
    cmd = 'pip install --process-dependency-links {} {}'.format(dev_opt, url)
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
    grant_priv = (
        'echo GRANT ALL PRIVILEGES ON DATABASE {db_name} to {db_user}'
    ).format(
        db_name=db_name, db_user=db_user
    )
    for cmd in [user_add, db_create, grant_priv]:
        print('running: ' + cmd)
        status, output = getstatusoutput(cmd)
        if status != 0:
            raise Exception(output)
        print(output)
        print('---')


# TODO: remove this when issue #201 is sorted
def create_netrc(earthdata_user, earthdata_password, **kwargs):
    l = "machine urs.earthdata.nasa.gov login {user} password {password}".format(
        user=earthdata_user,
        password=earthdata_password
    )
    fname = os.path.join(os.getenv("HOME"), '.netrc')
    if os.path.exists(fname):
        with open(fname, 'r+') as netrc:
            for line in netrc:
                if line.strip() == l:
                    # line alread exists
                    return
            netrc.seek(0, 2)
            netrc.write(l + "\n")
    else:
        with open(fname, 'w') as netrc:
            netrc.write(l + "\n")


def enable_cron():
    from crontab import CronTab
    cron = CronTab(user=True)
    # see if the job already exists
    jobs = [j for j in cron.find_command('scheduler')]
    if len(jobs) > 1:
        raise RuntimeError("multiple scheduler jobs in cron")
    from gips.datahandler import scheduler
    schedpath = scheduler.__file__
    # Turn pyc files into py files if we can
    if schedpath.endswith('.pyc') and os.path.exists(schedpath[:-1]):
        schedpath = schedpath[:-1]
    command = sys.executable + " " + schedpath + " > /dev/null 2>&1"
    if len(jobs) == 0:
        job = cron.new(command=command)
    else:
        job = jobs[0]
        job.set_command(command)
    job.setall('* * * * *')
    cron.write()


def enable_daemons(task_queue, queue_name, rqexe=''):
    from gips import datahandler 
    gdh_path = os.path.realpath(datahandler.__path__[0])
    dhdfile = os.path.join(gdh_path, 'gips_dhd.service.template')
    dhdoutfile = '/etc/systemd/system/gips_dhd.service'
    if os.path.exists(dhdoutfile):
        subprocess.call('systemctl stop gips_dhd.service', shell=True)
    dhdout = open(dhdoutfile, 'w')
    with open(dhdfile, 'r') as fin:
        for line in fin:
            dhdout.write(
                line.replace(
                    '$AS_USER', getpass.getuser()
                ).replace(
                    '$PYTHON', sys.executable
                ).replace(
                    '$COMMAND', os.path.join(gdh_path, 'dhd.py')
                )
            )
        dhdout.write("\n")
    print "you can now start gip_dhd with 'sudo systemctl start gips_dhd.service'"

    if task_queue == 'rq':
        rqfile = os.path.join(gdh_path, 'gips_rqworker@.service.template')
        rqoutfile = '/etc/systemd/system/gips_rqworker@.service'
        rqout = open(rqoutfile, 'w')
        with open(rqfile) as rqin:
            for line in rqin:
                rqout.write(
                    line.replace(
                        '$RQ_COMMAND', rqexe
                    ).replace(
                        '$QUEUE', queue_name
                    ).replace(
                        '$AS_USER', getpass.getuser()
                    )
                )
            rqout.write("\n")
        print "you can now start gips_rqworker with 'sudo systemctl start gips_rqworker@{1..4}.service'"
                        

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
        default=('modis', 'merra'),
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
        '--queue-server', default='localhost',
        help='Host running the task queue'
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
    p.add_argument(
	'--create-db', default=False, action='store_true',
	help='Create a postgres database and configure user and privileges'
    )
    p.add_argument(
        '--enable-cron', action='store_true', help='Insert entry for schedulure into crontab'
    )
    p.add_argument(
        '--enable-daemons', action='store_true', help='Setup and launch systemd controls for daemons'
    )
    args = vars(p.parse_args())
    PKGS = GIPPY_PKGS
    if args['task_queue'] == 'rq':
        PKGS += DH_RQ_PKGS
    elif args['task_queue'] == 'torque':
        PKGS += DH_TORQUE_PKGS
    else:
        raise Exception('Unknown task-queue specified "{}"'.format(task_queue))
    
    if args['install_pg']:
        PKGS += PG_PKGS
        
    install_system_requirements(PKGS)

    if args['create_db']:
        setup_postgresql(**args)

    install_gips(
        gips_version=args['gips_version'], extras=('dh-' + args['task_queue'],)
    )

    from gips.scripts.config import configure_environment
    configure_environment(**args)
    # TODO: for driver in drivers: gips_inventory {driver} --rectify
    # TODO: remove this after issue #201 is sorted
    if args['earthdata_user'] and args['earthdata_password']:
        create_netrc(**args)
    #print("Don't forget to add your ~/.netrc file (until issue #201 is sorted)")
    if args['enable_cron']:
        enable_cron()
    if args['enable_daemons']:
        # clunky way to execute this using sudo without running whole script via sudo
        import distutils
        rqexe = distutils.spawn.find_executable('rq')
        cmd = "sudo {} -c 'from install_datahandler import enable_daemons; enable_daemons(\"{}\",\"{}\",\"{}\")'".format(
            sys.executable,
            args['task_queue'],
            args['queue_name'],
            rqexe,
        )
        print cmd
        subprocess.call(cmd, shell=True)


if __name__ == '__main__':
    main()
