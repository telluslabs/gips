from __future__ import print_function

_verbosity = 1

def set_verbosity(verbosity):
    global _verbosity
    _verbosity = verbosity

def vprint(verbosity, *args, **kwargs):
    """Like print() but with verbosity governance:

    Pass in args and kwargs exactly like print(), except the first
    argument must be a verbosity level, and a new optional kwarg, 'f',
    can more conveniently set the output stream:

    vprint(verbosity, value, ...,
           sep=' ', end='\n', file=sys.stdout, f=['e'|'o'])

    f=['o'|'e'] prints to stdout or stderr respectively.  Specifying
    both 'f' and 'file' is ambiguous, so ValueError is raised in that
    case.
    """
    # if needed rewrite kwargs['f'] to kwargs['file']
    if 'f' in kwargs:
        if 'file' in kwargs:
            raise ValueError("Can't decide between f and file in kwargs")
        kwargs['file'] = {'o': sys.stdout, 'e': sys.stderr}[kwargs.pop('f')]
    if verbosity > _verbosity:
        return
    print(*args, **kwargs)
