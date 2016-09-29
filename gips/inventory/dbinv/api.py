import os, glob, sys, traceback, datetime, time

import django.db.transaction

from gips.utils import verbose_out, basename


"""API for the DB inventory for GIPS.

Provides a clean interface layer for GIPS callers to do CRUD ops on the
inventory DB, mostly by interfacing with dbinv.models.  Due to Django
bootstrapping weirdness, some imports have to be done in each function's
body.
"""


# TODO rename to rectify_assets and change docstring
def rectify_assets(asset_class):
    """Rectify the asset inventory database against the filesystem archive.

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


def rectify_products(data_class):
    """Rectify the product inventory database against the filesystem archive.

    For the current driver, go through each product in the filesystem
    and ensure it has an entry in the inventory database.  Also
    remove any database entries that match no extant file.  Attempt to
    follow the process in Data() closely, in particular find_files and
    ParseAndAddFiles.
    """
    # for now don't support SAR*, TODO to support SAR*, filter these files:
    #   files that match assets from data_class.Asset._assets[*]['pattern']
    #   *.index, *.xml, and *.hdr files
    if data_class.name in ('SAR', 'SARAnnual'):
        msg = "DB Inventory does not support driver '{}'.".format(data_class.name)
        raise RuntimeError(msg)

    # can't load this at module compile time because django initialization is crazytown
    from . import models
    # search_glob for supported drivers:  /path-to-repo/tiles/*/*/*.tif
    search_glob = os.path.join(data_class.Asset.Repository.data_path(),
                               '*', '*', data_class._pattern)
    assert search_glob[-1] not in ('*', '?') # sanity check in case new drivers don't conform
    file_iter = glob.iglob(search_glob)

    def match_failure_report(f_name, reason):
        msg = "Product file match failure:  '{}'\nReason:  {}"
        verbose_out(msg.format(f_name, reason), 2, sys.stderr)

    driver = data_class.name.lower()
    touched_rows = [] # for removing entries that don't match the filesystem
    add_cnt = 0
    update_cnt = 0
    # TODO break up transaction into manageable sizes?  This is going to get LARGE.
    # maybe google 'python chunk iterator'.
    iter_cnt = 0
    start_time = time.time()
    with django.db.transaction.atomic():
        for full_fn in file_iter:
            # after each chunk of work, report on progress & elapsed time
            iter_cnt += 1
            if iter_cnt % 1000 == 0:
                print "{} files scanned; total elapsed time {:0.2f}".format(iter_cnt, time.time() - start_time)
            base_fn = basename(full_fn)
            bfn_parts = base_fn.split('_')
            if not len(bfn_parts) == 4:
                match_failure_report(full_fn,
                        "Failure to parse:  Wrong number of '_'-delimited substrings.")
                continue
                # TODO support products whose len(parts) == 3

            # extract metadata about the file
            (tile, date_str, sensor, product) = bfn_parts
            date_pattern = data_class.Asset.Repository._datedir
            try:
                date = datetime.datetime.strptime(date_str, date_pattern).date()
            except Exception:
                verbose_out(traceback.format_exc(), 4, sys.stderr)
                msg = "Failure to parse date:  '{}' didn't adhere to pattern '{}'."
                match_failure_report(full_fn, msg.format(date_str, date_pattern))
                continue

            (product, created) = models.Product.objects.update_or_create(
                product=product,
                sensor=sensor,
                tile=tile,
                date=date,
                name=full_fn,
                driver=driver,
            )
            product.save()
            touched_rows.append(product.pk)
            if created:
                add_cnt += 1
                verbose_out("Product added to database:  " + full_fn, 4)
            else:
                update_cnt += 1
                verbose_out("Product found in database:  " + full_fn, 4)

    with django.db.transaction.atomic():
        # Remove things from DB that are NOT in FS; do it in a loop to avoid an explosion.
        query = models.Product.objects.filter(driver=driver)
        deletia_keys = set(query.values_list('id', flat=True)) - set(touched_rows)
        del_cnt = len(deletia_keys)
        if del_cnt > 0:
            for key in deletia_keys:
                models.Product.objects.get(pk=key).delete()
        msg = "Products complete, inventory records changed:  {} added, {} updated, {} deleted"
        print msg.format(add_cnt, update_cnt, del_cnt) # no -v for this important data


def list_tiles(driver):
    """List tiles for which there are extant asset files for the given driver."""
    from .models import Asset
    return Asset.objects.filter(driver=driver).values_list(
            'tile', flat=True).distinct().order_by('tile')


def list_dates(driver, tile):
    """For the given driver & tile, list dates for which assets exist."""
    from .models import Asset
    return Asset.objects.filter(driver=driver, tile=tile).values_list(
            'date', flat=True).distinct().order_by('date')


def add_asset(**values):
    """(very) thin convenience method that wraps models.Asset().save().

    Arguments:  asset, sensor, tile, date, name, driver; passed directly
    into models.Asset().
    """
    from .models import Asset
    a = Asset(**values)
    a.save()
    return a # in case the user needs it


def add_product(**values):
    """(very) thin convenience method that wraps models.Product().save().

    Arguments:  driver, product, sensor, tile, date, name; passed
    directly into models.Product().
    """
    from .models import Product
    p = Product(**values)
    p.save()
    return p # in case the user needs it


def update_or_add_asset(driver, asset, tile, date, sensor, name):
    """Update an existing model or create it if it's not found.

    Convenience method that wraps update_or_create.  The first four
    arguments are used to make a unique key to search for a matching model.
    """
    from . import models
    query_vals = {
        'driver': driver,
        'asset':  asset,
        'tile':   tile,
        'date':   date,
    }
    update_vals = {'sensor': sensor, 'name': name}
    (asset, created) = models.Asset.objects.update_or_create(defaults=update_vals, **query_vals)
    return asset # in case the user needs it


def update_or_add_product(driver, product, tile, date, sensor, name):
    """Update an existing model or create it if it's not found.

    Convenience method that wraps update_or_create.  The first four
    arguments are used to make a unique key to search for a matching model.
    """
    from . import models
    query_vals = {
        'driver':   driver,
        'product':  product,
        'tile':     tile,
        'date':     date,
    }
    update_vals = {'sensor': sensor, 'name': name}
    (asset, created) = models.Product.objects.update_or_create(defaults=update_vals, **query_vals)
    return asset # in case the user needs it


def product_search(**criteria):
    """Perform a search for asset models matching the given criteria.

    Under the hood just calls models.Asset.objects.filter(**criteria);
    see Django ORM docs for more details.
    """
    from gips.inventory.dbinv import models
    return models.Product.objects.filter(**criteria)


def asset_search(**criteria):
    """Perform a search for asset models matching the given criteria.

    Under the hood just calls models.Asset.objects.filter(**criteria);
    see Django ORM docs for more details.
    """
    from gips.inventory.dbinv import models
    return models.Asset.objects.filter(**criteria)
