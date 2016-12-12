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

test_job_string = """
# from gips.datahandler import worker

iterations = 20

def backslash_breeder(n, v=''):
    if n <= 1:
        return repr(v)
    else:
        return repr(backslash_breeder(n - 1, v))

print len(backslash_breeder(iterations))
"""

def submit(operation, args, batch_size=None):
    """Submit jobs to the configured Torque system.

    operation:  Defines which function will be performed, and must be one of
        'fetch', 'process', 'export', or 'postprocess'.
    args:  An iterable of tuples; each tuple represents the arguments to
        one call to the chosen function.
    batch_size:  The work is divided among torque jobs; each job receives
        batch_size function calls to perform in a loop.  Leave None for one job
        that works the whole batch.
    """
    if operation not in ('fetch', 'process', 'export', 'postprocess'):
        err_msg = ("'{}' is an invalid operation (valid operations are "
                   "'fetch', 'process', 'export', and 'postprocess')".format(operation))
        raise ValueError(err_msg)

    # TODO type & arity checking of args

    # Open a pipe to the qsub command.
    proc = Popen('qsub', shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE, close_fds=True)

    remote_python = utils.settings().REMOTE_PYTHON
    job_string = '\n'.join(['#!' + remote_python] + ['#PBS ' + d for d in pbs_directives])

    # TODO wire in operation/args/batch_size here

    job_string += test_job_string

    # Send job_string to qsub
    proc.stdin.write(job_string)
    out, err = proc.communicate()

    # Print your job and the system response to the screen as it's submitted
    print "SCRIPT TEXT (job_string):"
    print job_string
    print "OUT:"
    print out
    print "ERR:"
    print err
