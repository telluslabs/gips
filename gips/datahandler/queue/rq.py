from __future__ import absolute_import # otherwise this file shadows rq library

import rq
import redis

from .. import worker
from gips import utils


def submit(operation, call_signatures, chain=False):
    """Submit jobs to RQ workers via Redis acting as a message queue.

    Return value is a list of tuples, one for each batch:
        (job identifier, list of db item IDs) <-- eg IDs for Asset or Product models

    operation:  Defines which function will be performed; see queue.submit().
    call_signatures:  An iterable of iterables; each inner iterable gives the
        arguments to one call of the given function; needs to be in a
        format expected by ..worker functions.
    chain: If True, chain jobs to run in sequence.  Otherwise they may
        be worked in parallel depending on the RQ worker setup.
    """
    # assert batch_size is None, 'batch_size not supported for RQ (got {})'.format(nproc)
    # TODO log, don't print
    print 'operation:', operation
    print 'call_signatures:', repr(call_signatures)
    print 'chain:', repr(chain)
    # TODO support everything
    if operation != 'query':
        raise NotImplementedError('query only for now (and even this is fake)')

    # tell RQ what Redis connection to use
    redis_conn = redis.Redis(
            host=utils.get_setting('RQ_REDIS_HOST', 'localhost'),
            port=utils.get_setting('RQ_REDIS_PORT', 6379),
            db=utils.get_setting('RQ_REDIS_DB', 0),
            password=utils.get_setting('RQ_REDIS_PASSWORD', None)) # no password by default
    q = rq.Queue(
            name=utils.get_setting('RQ_QUEUE_NAME', 'datahandler'),
            # copy 8h walltime from torque
            default_timeout=utils.get_setting('RQ_TASK_TIMEOUT', 8 * 3600),
            connection=redis_conn)

    # delay execution
    task_function = worker.__dict__[operation]
    job = q.enqueue(worker.look_busy, 1)

    # job.id = UUID of job
    # job.result = return value of job (None before it finishes, dunno what happens if it fails)
    print 'job enqueued (id = {}), sleeping for 2 sec'.format(job.id)
    import time
    time.sleep(2) # Now, wait a while, until the worker is finished
    print 'woke from sleep, job.results: "{}"'.format(job.result) # => snarky remark + '1'
    raise NotImplementedError('return value is TBD')
