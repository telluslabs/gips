"""Worker functions for GIPS scheduled tasks.

Called inside worker processes; first implementation is expected to be torque
jobs.
"""

from django.db import transaction, IntegrityError

from gips import utils
from gips.inventory import dbinv
from gips.datahandler import api


def query (job):
    """Determine which assets to fetch and products to process"""
    with transaction.atomic():
        job = dbinv.models.Job.objects.get(pk=job)
        if job.status != 'scheduled':
            # TODO log/msg about giving up here
            return job # not sure this is useful for anything
        job.status = 'initializing' 
        job.save()

    api.query_service(job.variable.driver, job.spatial, job.temporal, [job.variable.product])

    job.refresh_from_db()
    if job.status != 'initializing':
        # sanity check; have to keep going, but whine about it
        err_msg = "Expected Job status to be 'initializing, but got {}"
        utils.verbose_out(err_msg.format(job.status), 1)
    job.status = 'in-progress'
    job.save()

    return job
    
        
def fetch(driver, asset_type, tile, date):
    """Fetch the asset file specified."""
    # Notify everyone that this process is doing the fetch.
    with transaction.atomic():
        # TODO confirm transaction.atomic prevents DB writes while it's active
        asset = dbinv.models.Asset.objects.get(
                driver=driver, asset=asset_type, tile=tile, date=date)
        if asset.status != 'scheduled':
            # TODO log/msg about giving up here
            return asset
        # TODO: this status change needs to be made earlier or could be scheduled twice
        asset.status = 'in-progress'
        asset.save()

    # locate the correct fetch function & execute it, then archive the file and update the DB
    DataClass  = utils.import_data_class(driver)
    AssetClass = DataClass.Asset
    filenames  = AssetClass.fetch(asset_type, tile, date)
    a_obj = AssetClass._archivefile(filenames[0])[0] # for now neglect the 'update' case

    # update DB now that the work is done; no need for an atomic transaction
    # because the only critical action is Model.save(), which is already atomic
    asset.refresh_from_db()
    if asset.status != 'in-progress':
        # sanity check; have to keep going but do whine about it
        err_msg = "Expected Asset status to be 'in-progress' but got '{}'"
        utils.verbose_out(err_msg.format(asset.status), 1)
    asset.sensor = a_obj.sensor
    asset.name   = a_obj.archived_filename
    asset.status = 'complete'
    asset.save()

    if len(filenames) > 1:
        err_msg = 'Expected to fetch one asset but fetched {} instead'.format(len(filenames))
        raise ValueError(err_msg, filenames)
    return asset


def process(driver, product_type, tile, date):
    """Produce the specified product file."""
    # Notify everyone that this process is doing the fetch.
    with transaction.atomic():
        product = dbinv.models.Product.objects.get(
                driver=driver, product=product_type, tile=tile, date=date)
        if product.status != 'scheduled':
            return product
        product.status = 'in-progress'
        product.save()

    DataClass = utils.import_data_class(driver)
    data = DataClass(tile, date) # should autopopulate with the right assets
    data.process([product_type])

    # sanity check
    product.refresh_from_db()
    if product.status != 'complete': # check process()'s work
        # sanity check; have to keep going but do whine about it
        err_msg = "Expected product status to be 'complete' but got '{}'"
        utils.verbose_out(err_msg.format(product.status), 1)

    return product


def export(*args, **kwargs):
    """Entirely TBD but does the same things as gips_project."""
    pass


def post_process(*args, **kwargs):
    """Entirely TBD but will support what used to be called zonalsummary ."""
    pass
