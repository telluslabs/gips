"""Torque-based backend for the GIPS work scheduler."""

# originally copied from:
# https://raw.githubusercontent.com/jdherman/hpc-submission-scripts/master/submit-pbs-loop.py

from subprocess import Popen, PIPE

from gips import utils

pbs_directives = [
    # for meaning of directives see
    #   http://docs.adaptivecomputing.com/torque/4-0-2/Content/topics/commands/qsub.htm
    '-N bsbreeder_job',
    '-A bsbreeder_test_contract:bsbreeder_test_task',
    '-k oe',
    '-j oe',
    '-V',
    '-l walltime=1:00:00',
    '-l nodes=1:ppn=1',
]

import_block = """
import os
import datetime
import gippy
from gips.inventory import dbinv, orm
from gips.datahandler import worker
"""

setup_block = """
os.environ['GIPS_ORM'] = 'true'
gippy.Options.SetVerbose(4) # substantial verbosity for testing purposes
orm.setup()
"""

def generate_script(operation, args):
    if operation != 'fetch':
        raise NotImplementedError('only fetch is supported')
    if operation not in ('fetch', 'process', 'export', 'postprocess'):
        err_msg = ("'{}' is an invalid operation (valid operations are "
                   "'fetch', 'process', 'export', and 'postprocess')".format(operation))
        raise ValueError(err_msg)
    lines = []
    lines.append('#!' + utils.settings().REMOTE_PYTHON) # shebang
    lines += ['#PBS ' + d for d in pbs_directives]      # #PBS directives
    lines.append(import_block)  # python imports, std lib, 3rd party, and gips
    lines.append(setup_block)   # config & setup code

    # star of the show, the actual fetch
    lines.append("worker.{}({}, {}, {}, {})".format(operation, *[repr(i) for i in args]))

    return '\n'.join(lines) # stitch into single string & return


def submit(operation, args_ioi, batch_size=None):
    """Submit jobs to the configured Torque system.

    operation:  Defines which function will be performed, and must be one of
        'fetch', 'process', 'export', or 'postprocess'.
    args_ioi:  An iterable of iterables; each inner iterable gives the
        arguments to one call to the chosen function.
    batch_size:  The work is divided among torque jobs; each job receives
        batch_size function calls to perform in a loop.  Leave None for one job
        that works the whole batch.
    """
    if operation != 'fetch':
        raise NotImplementedError('only fetch is supported')
    if operation not in ('fetch', 'process', 'export', 'postprocess'):
        err_msg = ("'{}' is an invalid operation (valid operations are "
                   "'fetch', 'process', 'export', and 'postprocess')".format(operation))
        raise ValueError(err_msg)

    # TODO loop starts here - wire in chunking here

    # Open a pipe to the qsub command.
    proc = Popen('qsub', shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE, close_fds=True)

    job_script = generate_script(operation, args_ioi[0])

    # Send job_string to qsub
    proc.stdin.write(job_script)
    out, err = proc.communicate()

    # TODO confirm qsub exited 0 (raise otherwise)
    # TODO return best thing for checking on status
    # TODO log err someplace

    return [(proc.returncode, out, err)]
