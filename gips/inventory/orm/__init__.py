import os, sys
from contextlib import contextmanager
import traceback

import django

from gips.utils import verbose_out


@contextmanager
def std_error_handler():
    """Handle problems with ORM code in a unified way."""
    try:
        yield
    except Exception as e:
        verbose_out(traceback.format_exc(), 4, sys.stderr)
        verbose_out("Error processing database inventory: {}".format(e.message), 1, sys.stderr)
        sys.exit(1)


def use_orm():
    """Check GIPS_ORM to see if the user wants to use the Django ORM.

    Use the ORM only if the user sets GIPS_ORM to 'true' (case
    insensitive) or any nonzero number.
    """
    raw_val = os.environ.get('GIPS_ORM', 'true')
    use_orm = raw_val.lower() == 'true'
    if not use_orm:
        try:
            use_orm = bool(float(raw_val))
        except ValueError:
            pass # "anything else" is considered False
    return use_orm


setup_complete = False

def setup():
    """Set settings module default and run django.setup().

    Prevent this from happening more than once using a global guard."""
    global setup_complete
    if setup_complete:
        return
    if use_orm():
        with std_error_handler():
            os.environ.setdefault("DJANGO_SETTINGS_MODULE", "gips.inventory.orm.settings")
            django.setup()
    setup_complete = True
