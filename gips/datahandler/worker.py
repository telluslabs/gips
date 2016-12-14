"""Worker functions for GIPS scheduled tasks.

Called inside worker processes; first implementation is expected to be torque
jobs.
"""

from django.db import transaction, IntegrityError

from gips import utils
from gips.inventory import dbinv


def fetch(driver, asset_type, tile, date):
    """Fetch the asset file specified."""
    # Notify everyone that this process is doing the fetch.
    with transaction.atomic():
        # TODO confirm transaction.atomic prevents DB writes while it's active
        asset = dbinv.models.Asset.objects.get(
                driver=driver, asset=asset_type, tile=tile, date=date)
        if asset.status.status in ('in-progress', 'complete'):
            # TODO log/msg about giving up here
            return asset
        asset.status = dbinv.models.Status.objects.get(status='in-progress')
        asset.save()

    # locate the correct fetch function & execute it, then archive the file and update the DB
    DataClass  = utils.import_data_class(driver)
    AssetClass = DataClass.Asset
    filenames  = AssetClass.fetch(asset_type, tile, date)
    a_obj = AssetClass._archivefile(filenames[0])[0] # for now neglect the 'update' case

    # update DB now that the work is done; no need for an atomic transaction
    # because the only critical action is Model.save(), which is already atomic
    asset.refresh_from_db()
    if asset.status.status != 'in-progress':
        # sanity check; have to keep going but do whine about it
        err_msg = "Expected Asset status to be 'in-progress' but got '{}'"
        utils.verbose_out(err_msg.format(asset.status.status), 1)
    asset.sensor = a_obj.sensor
    asset.name   = a_obj.archived_filename
    asset.status = dbinv.models.Status.objects.get(status='complete')
    asset.save()

    if len(filenames) > 1:
        err_msg = 'Expected to fetch one asset but fetched {} instead'.format(len(filenames))
        raise ValueError(err_msg, filenames)
    return asset


##### TODO unimplemented here down - needs doing for the demo #####

def process(driver, product_type, tile, date):
    """Produce the specified product file."""
    pass


def export(*args, **kwargs):
    """Entirely TBD but does the same things as gips_project."""
    pass


def post_process(*args, **kwargs):
    """Entirely TBD but will support what used to be called zonalsummary ."""
    pass
