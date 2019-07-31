class GipsException(Exception):
    def __init__(self, *args, **kwargs):
        super(GipsException, self).__init__(*args, **kwargs)
        # TODO add a registry of of exc_codes.  For now, default to 1 as an
        # unknown error
        self.exc_code = 1 if 'exc_code' not in kwargs else kwargs['exc_code']

