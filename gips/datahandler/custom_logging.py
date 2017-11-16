from . import queue

class DataHandlerLoggingFilter(object):
    def filter(self, log_record):
        """Doesn't filter out records, instead adds an attribute, dh_id.

        dh_id is a job ID if one is available, otherwise the process ID.
        Reports errors in dh_id; otherwise logging breaks completely.
        """
        try:
            log_record.dh_id = '{}:{}'.format(queue.tq_setting(), queue.get_job_name())
        except queue.NoCurrentJobError:
            log_record.dh_id = 'pid:{}'.format(log_record.process)
        except Exception as e:
            log_record.dh_id = 'DH ID error:' + repr(e)

        return True
