import os, glob, sys, traceback, datetime, time, itertools

import django.db.transaction

from gips.utils import verbose_out, basename


"""API for the DB inventory for GIPS.

Provides a clean interface layer for GIPS callers to do CRUD ops on the
inventory DB, mostly by interfacing with dbinv.models.  Due to Django
bootstrapping weirdness, some imports have to be done in each function's
body.
"""


def _grouper(iterable, n, fillvalue=None):
    """Collect data into fixed-length chunks or blocks.

    e.g.:  grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx"
    Taken nearly verbatim from the python itertools docs:
    https://docs.python.org/2/library/itertools.html"""
    args = [iter(iterable)] * n
    return itertools.izip_longest(fillvalue=fillvalue, *args)


def _chunky_transaction(iterable, function, chunk_sz=1000, item_desc="items"):
    """Iterate over items in chunks; each chunk is 1 database transaction."""
    iter_cnt = 0
    chunk_start_time = start_time = time.time()
    for chunk in _grouper(iterable, chunk_sz):
        with django.db.transaction.atomic():
            for item in chunk:
                if item is None:
                    break # need this due to izip_longest padding chunks with Nones
                function(item)
        # after each chunk report stats
        iter_cnt += chunk_sz
        new_chunk_start_time = time.time()
        print "{} {} scanned; chunk time {:0.2f}s, total time {:0.2f}s".format(
                iter_cnt, item_desc,
                new_chunk_start_time - chunk_start_time,
                new_chunk_start_time - start_time)
        chunk_start_time = new_chunk_start_time


def rectify_assets(asset_class):
    """Rectify the asset inventory database against the filesystem archive.

    For the current driver, go through each asset in the filesystem
    and ensure it has an entry in the inventory database.  Also
    remove any database entries that match no archived files.
    """
    # can't load this at module compile time because django initialization is crazytown
    from . import models
    mao = models.Asset.objects
    driver = asset_class.Repository.name.lower()
    # this assumes this directory layout:  /path-to-repo/tiles/*/*/
    path_glob = os.path.join(asset_class.Repository.data_path(), '*', '*')

    def rectify_asset(f_name): # work function for _chunky_transaction()
        a = asset_class(f_name)
        (asset, created) = mao.update_or_create(
                asset=a.asset, sensor=a.sensor, tile=a.tile, date=a.date,
                name=f_name, driver=driver)
        asset.save()
        touched_rows.add(asset.pk)
        if created:
            counts['add'] += 1
            verbose_out("Asset added to database:  " + f_name, 4)
        else:
            counts['update'] += 1
            verbose_out("Asset found in database:  " + f_name, 4)

    start_time = time.time()
    for (ak, av) in asset_class._assets.items():
        print "Starting on {} assets at {:0.2f}s".format(ak, time.time() - start_time)
        counts = {'add': 0, 'update': 0} # A flaw in python scoping makes this necessary
        touched_rows = set() # for removing entries that don't match the filesystem
        # little optimization to make deleting stale records go faster:
        starting_keys = set(mao.filter(driver=driver, asset=ak).values_list('id', flat=True))

        _chunky_transaction(glob.iglob(os.path.join(path_glob, av['pattern'])), rectify_asset)

        # Remove things from DB that are NOT in FS:
        print "Deleting stale asset records . . . "
        delete_start_time = time.time()
        deletia_keys = starting_keys - touched_rows
        _chunky_transaction(deletia_keys, lambda key: mao.get(pk=key).delete())
        delete_time = time.time() - delete_start_time

        del_cnt = len(deletia_keys)
        if del_cnt > 0:
            print "Deleted {} stale asset records in {:0.2f}s.".format(del_cnt, delete_time)
        else:
            print "No stale asset records found; search time {:0.2f}s".format(delete_time)
        msg = "{} complete, inventory records changed:  {} added, {} updated, {} deleted"
        print msg.format(ak, counts['add'], counts['update'], del_cnt) # no -v for this important data


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
