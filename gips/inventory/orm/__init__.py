import os, sys
from contextlib import contextmanager
import traceback

import django

from gips import utils


def use_orm():
    """Check GIPS_ORM to see if the user wants to use the Django ORM.

    Defaults to True.
    """
    return getattr(utils.settings(), 'GIPS_ORM', True)

setup_complete = False
driver_for_dbinv_feature_toggle = 'unspecified'

def setup():
    """Set settings module default and run django.setup().

    Prevent this from happening more than once using a global guard."""
    global setup_complete
    if setup_complete:
        return
    if use_orm():
        busted_drivers = ('sarannual',)

        if driver_for_dbinv_feature_toggle in busted_drivers:
            raise Exception("Inventory database does not support '{}'.  Set"
                    " GIPS_ORM = False to use the filesystem inventory"
                    " instead.".format(driver_for_dbinv_feature_toggle))
        with utils.error_handler("Error initializing Django ORM"):
            os.environ.setdefault("DJANGO_SETTINGS_MODULE", "gips.inventory.orm.settings")
            django.setup()
    setup_complete = True
