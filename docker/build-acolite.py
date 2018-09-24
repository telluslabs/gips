#!/usr/bin/env python2

from __future__ import print_function

import os
import subprocess
import urllib
import tarfile

wd = '.'
bn = 'acolite_py_linux_20180925.0.tar.gz'
untarred_bn = 'acolite_py_linux'
url = 'http://odnature.naturalsciences.be/downloads/remsem/acolite/' + bn
tag = 'aco-gips'

# download acolite tarball
fp = os.path.join(wd, bn)
if os.path.exists(bn):
    print(bn, 'found, skipping download')
else:
    print(bn, 'not found, downloading . . .')
    urllib.urlretrieve(url, fp)
    print(bn, 'download complete')

# untar it, but only if we haven't already
untarred_fp = os.path.join(wd, untarred_bn)
sigil = os.path.join(untarred_fp, '.build-acolite.py-sigil')
if (os.path.exists(untarred_fp)
        and os.stat(fp).st_mtime < os.stat(sigil).st_mtime):
    print('skipping untar;', bn, 'already untarred into', untarred_bn)
else:
    print('untarring', bn, '. . .')
    tar = tarfile.open(fp)
    tar.extractall()
    tar.close()
    open(sigil, 'a').close() # python idiom for `touch $sigil`
    print(fp, 'untar complete')

print('building', tag, '. . .')
args = ('docker build -t ' + tag + ' -f docker/acolite.docker .').split(' ')
# more args if needed:
#docker build --no-cache --build-arg GIPS_UID=$(id -u)
#    -t gips_test_$CI_COMMIT_REF_SLUG -f docker/gips-ci.docker .
subprocess.check_call(args)
print(tag, 'build complete')
