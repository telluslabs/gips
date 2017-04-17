from __future__ import absolute_import # otherwise this file shadows rq library

import os

import rq
import redis
import gippy

from gips import utils
from gips.inventory import orm
from .. import worker
from .. import queue

def get_job_name():
    """Returns the current job ID, if one exists."""
    job = rq.get_current_job()
    if job is None:
        raise queue.NoCurrentJobError('rq.get_current_job() returned None; no current job found')
    return job.id

def is_job_alive(job_id):
    """Tells whether the given job is currently running.

    Job metadata in RQ has a TTL, so if no job matches the job ID,
    False is returned because it's assumed the ID matched a job whose
    metadata has since been removed from Redis.
    """
    job = get_queue().fetch_job(job_id)
    return job is not None and job.is_started


_queue = None

def get_queue():
    """Set up the RQ Queue object and return it.  Uses GIPS settings."""
    # tell RQ what Redis connection to use
    global _queue
    if _queue is None:
        redis_conn = redis.Redis(
                host=utils.get_setting('RQ_REDIS_HOST', 'localhost'),
                port=utils.get_setting('RQ_REDIS_PORT', 6379),
                db=utils.get_setting('RQ_REDIS_DB', 0),
                password=utils.get_setting('RQ_REDIS_PASSWORD', None)) # no password by default
        _queue = rq.Queue(
                name=utils.get_setting('RQ_QUEUE_NAME', 'datahandler'),
                # copy 8h walltime from torque
                default_timeout=utils.get_setting('RQ_TASK_TIMEOUT', 8 * 3600),
                connection=redis_conn)
    return _queue


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
    if operation not in ('query', 'fetch', 'process'):
        raise NotImplementedError('Not all methods supported')

    q = get_queue()
    outcomes = []
    job = None # prime the pump for chain=True
    for cs in call_signatures:
        job = q.enqueue(work, operation, *cs, depends_on=(job if chain else None))
        # reminder: cs[0] ought to be the primary key of a model in dbinv.models
        outcomes.append((job.id, cs[0]))

    return outcomes
