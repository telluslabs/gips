"""Worker functions for GIPS scheduled tasks.

Called inside worker processes; first implementation is expected to be torque
jobs.
"""
import os, shutil

from django.db import transaction, IntegrityError

from gips import utils
from gips.datahandler import api
from gips.core import SpatialExtent, TemporalExtent
from gips.inventory import DataInventory, ProjectInventory
from gips.inventory import dbinv, orm
from gips.scripts.spatial_wrapper import aggregate


def query (job):
    """Determine which assets to fetch and products to process"""
    with transaction.atomic():
        job = dbinv.models.Job.objects.get(pk=job)
        if job.status != 'initializing':
            # TODO log/msg about giving up here
            return job # not sure this is useful for anything
        job.status = 'scheduled'
        job.save()

    api.query_service(job.variable.driver, eval(job.spatial), eval(job.temporal), [job.variable.product])

    job.refresh_from_db()
    if job.status != 'scheduled':
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
    if len(filenames) == 0:
        asset.status = 'failed'
        asset.save()
        return asset  # TODO: seems odd that this function returns
                      #       asset...discuss with tolson and fisk.

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


def _export(**kwargs):
    """Performs a 'gips_project' with the given paramenters."""

    class Arguments(object):
        pass

    args = Arguments()
    args.__dict__ = kwargs


    DataClass = utils.import_data_class(kwargs['command'])

    # TODO trash and recreate output dir

    extents = SpatialExtent.factory(
        DataClass, args.site, args.key, args.where, args.tiles, args.pcov,
        args.ptile
    )

    # create tld: SITENAME--KEY_DATATYPE_SUFFIX
    if args.notld:
        tld = args.outdir
    else:
        key = '' if args.key == '' else '--' + args.key
        suffix = '' if args.suffix == '' else '_' + args.suffix
        res = '' if args.res is None else '_%sx%s' % (args.res[0], args.res[1])
        bname = (
            extents[0].site.LayerName() +
            key + res + '_' + args.command + suffix
        )
        tld = os.path.join(args.outdir, bname)

    for extent in extents:
        t_extent = TemporalExtent(args.dates, args.days)
        inv = DataInventory(DataClass, extent, t_extent, **vars(args))
        datadir = os.path.join(tld, extent.site.Value())
        if inv.numfiles > 0:
            inv.mosaic(
                datadir=datadir, tree=args.tree, overwrite=args.overwrite,
                res=args.res, interpolation=args.interpolation,
                crop=args.crop, alltouch=args.alltouch,
            )
        else:
            utils.verbose_out(
                'No data found for {} within temporal extent {}'
                .format(str(t_extent), str(t_extent)),
                2,
            )
    # TODO nothing meaningful to return?


def _aggregate(job_id, outdir):
    aggregate(outdir, job_id)


def export_and_aggregate(job_id, export_kwargs):
    """Entirely TBD but does the same things as gips_project + zonal summary."""
    with transaction.atomic():
        job = dbinv.models.Job.objects.get(pk=job_id)
        if job.status != 'pp_scheduled':
            # TODO log/msg about giving up here
            return job # not sure this is useful for anything
        job.status = 'post-processing'
        job.save()

    # setup output dir
    outdir = export_kwargs.setdefault('outdir',
                                      os.path.join(utils.settings().EXPORT_DIR, str(job_id)))
    # poor man's binary semaphore since mkdir is atomic;
    # exception on a priori existence is what we want here
    os.makedirs(outdir)

    # run
    _export(**export_kwargs)
    _aggregate(job_id, outdir)

    # bookkeeping & cleanup
    job.refresh_from_db()
    if job.status != 'post-processing':
        # sanity check; have to keep going, but whine about it
        err_msg = "Expected Job status to be 'post-processing', but got {}"
        utils.verbose_out(err_msg.format(job.status), 1)
    job.status = 'complete'
    job.save()

    shutil.rmtree(outdir)
