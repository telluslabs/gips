import os

import django

setup_complete = False

def setup():
    global setup_complete
    if not setup_complete:
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "gips.inventory.orm.settings")
        django.setup()
        setup_complete = True
