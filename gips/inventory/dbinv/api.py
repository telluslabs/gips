import os, glob
from sys import stderr
from contextlib import contextmanager
import traceback

import django
import django.db.transaction

# TODO put this in scripts/*.py:  gips.orm.setup() # must come before importing models
import gips.inventory.orm
from gips.utils import verbose_out


@contextmanager
def std_error_handler(fs_fallback=None):
    """Handle problems with API code in a unified way.

    Optionally provide a callback to run if the DB API call fails."""
    try:
        yield
    except Exception as e:
        verbose_out(traceback.format_exc(), 4, stderr)
        verbose_out("Error in database inventory API: {}".format(e.message), 1, stderr)
        verbose_out("Falling back to filesystem inventory.", 1, stderr)
        if fs_fallback is not None:
            fs_fallback()


def rectify(asset_class):
    """Rectify the inventory database against the filesystem archive.

    For the current driver, go through each asset in the filesystem
    and ensure it has an entry in the inventory database.  Also
    remove any database entries that match no archived files.
    """
    # can't load this at module compile time because django initialization is crazytown
    from . import models
    # this assumes this directory layout:  /path-to-repo/tiles/*/*/
    path_glob = os.path.join(asset_class.Repository.data_path(), '*', '*')

    for (ak, av) in asset_class._assets.items():
        file_iter = glob.iglob(os.path.join(path_glob, av['pattern']))
        touched_rows = [] # for removing entries that don't match the filesystem
        with django.db.transaction.atomic():
            add_cnt = 0
            update_cnt = 0
            for f_name in file_iter:
                a = asset_class(f_name)
                (asset, created) = models.Asset.objects.update_or_create(
                    asset=a.asset,
                    sensor=a.sensor,
                    tile=a.tile,
                    date=a.date,
                    name=f_name,
                    driver=asset_class.Repository.name.lower(),
                )
                asset.save()
                touched_rows.append(asset.pk)
                if created:
                    add_cnt += 1
                    verbose_out("Asset added to database:  " + f_name, 4)
                else:
                    update_cnt += 1
                    verbose_out("Asset found in database:  " + f_name, 4)
            # Remove things from DB that are NOT in FS:
            deletia = models.Asset.objects.filter(asset=ak).exclude(pk__in=touched_rows)
            del_cnt = deletia.count()
            if del_cnt > 0:
                deletia.delete()
            msg = "{} complete, inventory records changed:  {} added, {} updated, {} deleted"
            print msg.format(ak, add_cnt, update_cnt, del_cnt) # no -v for this important data


def list_tiles(driver):
    """List tiles for which there are extant asset files for the given driver."""
    from .models import Asset
    return Asset.objects.filter(driver=driver).values_list('tile', flat=True).distinct()


def add_asset(**values):
    """(very) thin convenience method that wraps models.Asset().save().

    Arguments:  asset, sensor, tile, date, name, driver; passed directly
    into models.Asset().
    """
    from .models import Asset
    a = Asset(**values)
    a.save()
    return a # in case the user needs it


def asset_search(**criteria):
    """Perform a search for asset models matching the given criteria.

    Under the hood just calls models.Asset.objects.filter(**criteria);
    see Django ORM docs for more details.
    """
    from gips.inventory.dbinv import models
    return models.Asset.objects.filter(**criteria)
