from __future__ import absolute_import # otherwise this file shadows rq library

import os

import rq
import redis
import gippy

from .. import worker
from gips import utils
from gips.inventory import orm


def work(operation, *args):
    """Set up a good environment, then call worker.operation(*args).

    Meant to be executed in an RQ worker process."""
    os.environ['GIPS_ORM'] = 'true'
    gippy.Options.SetVerbose(4) # substantial verbosity for testing purposes
    orm.setup()
    return worker.__dict__[operation](*args)


def submit(operation, call_signatures, chain=False):
    """Submit jobs to RQ workers via Redis acting as a message queue.

    Return value is a list of tuples:
        (job identifier, db item ID) <-- eg IDs for Asset or Product models

    operation:  Defines which function will be performed; see
        queue.submit().
    call_signatures:  An iterable of iterables; each inner iterable
        gives the arguments to one call of the given function; needs to
        be in a format expected by ..worker functions (first item is
        always a model ID).
    chain: If True, chain jobs to run in sequence.  Otherwise they may
        be worked in parallel depending on the RQ worker setup.
    """
    # TODO support everything
    if operation != 'query':
        raise NotImplementedError('query only for now (and even this is fake)')
    if chain:
        raise NotImplementedError('chain=True is a TODO')

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
    outcomes = []
    for cs in call_signatures:
        job = q.enqueue(work, operation, *cs)
        # reminder: cs[0] ought to be the primary key of a model in dbinv.models
        outcomes.append((job.id, cs[0]))

    return outcomes
