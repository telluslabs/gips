from __future__ import absolute_import # otherwise this file shadows rq library

import rq
import redis

from .. import worker
from gips import utils


def submit(operation, args_ioi, batch_size=None, nproc=None, chain=False):
    assert nproc is None, 'nproc not supported for RQ (got {})'.format(nproc)
    print 'operation:', operation
    print 'args_ioi:', repr(args_ioi)
    print 'batch_size:', repr(batch_size)
    print 'chain:', repr(chain)
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
            connection=redis_conn)

    # delay execution
    # TODO job id?  is that usable for what I want to do?
    job = q.enqueue(worker.look_busy, 1)
    print 'job enqueued (id = {}), sleeping for 2 sec'.format(job.id)
    import time
    time.sleep(2) # Now, wait a while, until the worker is finished
    print 'woke from sleep, job.results: "{}"'.format(job.result) # => snarky remark + '1'
    raise NotImplementedError('return value is TBD')
