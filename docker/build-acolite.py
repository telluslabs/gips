#!/usr/bin/env python2

from __future__ import print_function

import sys
import os
import subprocess
import tarfile
import argparse

import requests

# change this when versions update:
url = 'http://odnature.naturalsciences.be/downloads/remsem/acolite/acolite_py_linux_20181210.0.tar.gz'

# takes one arg, a name for the built image
parser = argparse.ArgumentParser()
parser.add_argument('tag', type=str, nargs='?', default='aco-gips')
pa = parser.parse_args()

wd = 'docker/'
untarred_bn = 'acolite_py_linux'
bn = os.path.basename(url)
tarball_rp = os.path.join(wd, bn)
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
        # stolen from gips.utils becuase python's stdlib is terrible at it
        r = requests.get(url)
        r.raise_for_status()
        with open(tarball_rp, 'wb') as fo:
            [fo.write(c) for c in r.iter_content() if c]
        print(tarball_rp, 'download complete')

    print('untarring', tarball_rp, '. . .')
    tar = tarfile.open(tarball_rp)
    tar.extractall(wd)
    tar.close()
    os.remove(tarball_rp)
    print(tarball_rp, 'untar complete; tarball removed to save space')

# wow docker, HAVE to have your dockerfile in the context
cmd = 'docker build -t ' + pa.tag + ' -f docker/acolite.docker docker/'
print('Starting `' + cmd + '` . . .')
# more args if needed:
#docker build --no-cache --build-arg GIPS_UID=$(id -u)
#    -t gips_test_$CI_COMMIT_REF_SLUG -f docker/gips-ci.docker .
subprocess.check_call(cmd.split(' '))
print(pa.tag, 'build complete')
