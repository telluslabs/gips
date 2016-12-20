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

def generate_script(operation, args_batch):
    """Produce torque script from given worker function and arguments."""
    lines = []
    lines.append('#!' + utils.settings().REMOTE_PYTHON) # shebang
    lines += ['#PBS ' + d for d in pbs_directives]      # #PBS directives
    lines.append(import_block)  # python imports, std lib, 3rd party, and gips
    lines.append(setup_block)   # config & setup code

    # star of the show, the actual fetch
    for args in args_batch:
        lines.append("worker.{}{}".format(operation, tuple(args)))

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
    if operation not in ('query', 'fetch', 'process', 'export', 'export_and_aggregate'):
        err_msg = ("'{}' is an invalid operation (valid operations are "
                   "'fetch', 'process', 'export', and 'postprocess')".format(operation))
        raise ValueError(err_msg)

    if batch_size is None:
        chunks = [args_ioi]
    else:
        chunks = list(utils.grouper(args_ioi, batch_size))

    # clean last chunk:  needed due to izip_longest padding chunks with Nones:
    chunks.append([i for i in chunks.pop() if i is not None])

    outcomes = []

    for chunk in chunks:
        job_script = generate_script(operation, chunk)

        # open a pipe to the qsub command, then end job_string to it
        proc = Popen('qsub', shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE, close_fds=True)
        proc.stdin.write(job_script)
        out, err = proc.communicate()
        outcomes.append((proc.returncode, out, err))

    # TODO confirm qsub exited 0 (raise otherwise)
    # TODO return best thing for checking on status
    # TODO log err someplace

    return outcomes
