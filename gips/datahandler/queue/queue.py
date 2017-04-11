"""Interface for task queues; currently supporting RQ and TORQUE.

The API has three functions, each of which is a pass-through to specific
code that talks to RQ or TORQUE, depending on the GIPS setting
TASK_QUEUE.
"""

from gips import utils

def get_queue():
    """Return the appropriate module based on GIPS setting TASK_QUEUE.

    The default is 'torque'; the other valid value is 'rq'; ValueError
    is raised otherwise.
    """
    configured_queue = utils.get_setting('TASK_QUEUE', default='torque')
    if configured_queue == 'torque':
        from . import torque
        return torque
    elif configured_queue == 'rq':
        from . import rq
        return rq
    else:
        raise ValueError('Unknown TASK_QUEUE `{}`'.format(configured_queue))


def get_job_name(*args, **kwargs):
    return get_queue().get_job_name(*args, **kwargs)

def is_job_alive(*args, **kwargs):
    return get_queue().is_job_alive(*args, **kwargs)

def submit(*args, **kwargs):
    return get_queue().submit(*args, **kwargs)
