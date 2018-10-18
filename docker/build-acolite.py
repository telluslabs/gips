#!/usr/bin/env python2

from __future__ import print_function

import sys
import os
import subprocess
import urllib
import tarfile

a_cnt = len(sys.argv)
if a_cnt not in (1, 2):
    raise IOError('expected zero or one argument')
tag = sys.argv[1] if a_cnt == 2 else 'aco-gips'

wd = 'docker/'
bn = 'acolite_py_linux_20180925.0.tar.gz'
untarred_bn = 'acolite_py_linux'

tarball_rp = os.path.join(wd, bn)
url = 'http://odnature.naturalsciences.be/downloads/remsem/acolite/' + bn
untarred_rp = os.path.join(wd, untarred_bn)

# untar it, but only if we haven't already
if os.path.exists(untarred_rp):
    print('skipping download;', tarball_rp,
          'already untarred into', untarred_rp)
else:
    # download acolite tarball if needed
    if os.path.exists(tarball_rp):
        print(tarball_rp, 'found, skipping download')
    else:
        print(tarball_rp, 'not found, downloading . . .')
        urllib.urlretrieve(url, tarball_rp)
        print(tarball_rp, 'download complete')

    print('untarring', tarball_rp, '. . .')
    tar = tarfile.open(tarball_rp)
    tar.extractall(wd)
    tar.close()
    os.remove(tarball_rp)
    print(tarball_rp, 'untar complete; tarball removed to save space')

# wow docker, HAVE to have your dockerfile in the context
cmd = 'docker build -t ' + tag + ' -f docker/acolite.docker docker/'
print('Starting `' + cmd + '` . . .')
# more args if needed:
#docker build --no-cache --build-arg GIPS_UID=$(id -u)
#    -t gips_test_$CI_COMMIT_REF_SLUG -f docker/gips-ci.docker .
subprocess.check_call(cmd.split(' '))
print(tag, 'build complete')
