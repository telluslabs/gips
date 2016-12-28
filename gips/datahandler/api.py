"""GIPS scheduler API, for scheduling work and checking status of same."""

from datetime import timedelta
from pprint import pprint

from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction

from gips import utils
from gips.core import SpatialExtent, TemporalExtent

from gips.inventory import dbinv, orm
from gips.datahandler import torque

#from pdb import set_trace


def submit_job (site, variable, spatial, temporal):
    """Pass a work spec in to the scheduler, and the work will be done.

    site:           geokit site id
    variable:       DataVariable.name
    spatial:        dictionary of parameters specifying a spatial extent
                    (see gips.core.SpatialExtent.factory)
    temporal:       dictionary of TemporalExtent parameters ('dates' and 'days')
    """
    orm.setup()
    job = dbinv.models.Job.objects.create(
        site=site,
        variable=dbinv.models.DataVariable.objects.get(name=variable),
        spatial=repr(spatial),
        temporal=repr(temporal),
        status='requested',
    )

    return job.pk


def schedule_query ():
    '''
    Submit to torque (or other) query job for any new 'job'.
    Runs query_service(...) to determine assets that need to be
    fetched and products that need to be processed.

    Will be called by a cron'd scheduler job.
    '''
    orm.setup()
    with transaction.atomic():
        jobs = dbinv.models.Job.objects.filter(status='requested')
        if jobs.exists():
            query_args = [ [j.pk] for j in jobs ]
            jobs.update(status='initializing')
            return torque.submit('query', query_args, 1)


def schedule_fetch ():
    '''
    Submit to torque (or other) fetch jobs for any assets that
    are 'requested'. Mark scheduled assets as 'scheduled'.

    Will be called by a cron'd scheduler job.
    '''

    orm.setup()
    # TODO: this needs to be throttleable
    with transaction.atomic():
        assets = dbinv.models.Asset.objects.filter(status='requested')
        if assets.exists():
            fetch_args = [ [a.driver, a.asset, a.tile, a.date]
                           for a in assets ]
            assets.update(status='scheduled')
            return torque.submit('fetch', fetch_args) # for now, submit all to same job


def schedule_process ():
    '''
    Submit to torque (or other?) jobs to process any products that are
    ready to be processed - i.e. are 'requested' and all asset
    dependencies are 'complete'. Mark scheduled products as 'scheduled'.

    Will be called by a cron'd scheduler job
    '''

    orm.setup()
    from django.db.models import Q
    with transaction.atomic():
        products = dbinv.models.Product.objects.filter(
            status='requested'
        ).exclude(
            ~Q(assetdependency__asset__status='complete')
        )
        if products.exists():
            # TODO: process() fails if passed unicode strings. why?
            def de_u(u):
                return u.encode('ascii', 'ignore')
            process_args = [ [de_u(p.driver), de_u(p.product), de_u(p.tile), p.date]
                             for p in products ]
            products.update(status='scheduled')
            return torque.submit('process', process_args, 2)


def schedule_export_and_aggregate ():
    '''
    Check all Jobs to see if  ready for post-processing (all assets fetched and
    all products processed). If so, submit export and aggregate jobs
    to torque (or other?) 

    Will be called by a cron'd scheduler job

    '''
    orm.setup()
    with transaction.atomic():
        jobs = dbinv.models.Job.objects.filter(status='in-progress')
        for job in jobs:
            status = processing_status(
                job.variable.driver.encode('ascii', 'ignore'),
                eval(job.spatial),
                eval(job.temporal),
                [job.variable.product.encode('ascii', 'ignore')]
            )
            if (
                    status['requested'] == 0
                    and status['scheduled'] == 0
                    and status['in-progress'] == 0
            ):
                # nothing being worked on. must be done pre-processing
                print "Submitting job", job.pk, "for export and aggregate"
                job.status = 'pp-scheduled'
                job.save()
                # TODO: need a better way to configure / determine nproc
                nproc = 4
                torque.submit('export_and_aggregate', [[job.pk, nproc]], nproc=nproc)


def processing_status(driver_name, spatial_spec, temporal_spec, products):
        """ status of products matching this time-space-product query
        :drivername: The name of the Data class to use (e.g., landsat, modis)
        :spatial_spec: The dict of SpatialExtent.factory parameters
        :temporal_spec: The TemporalExtent constructor parameters
        :products: List of requested products of interest
        """
        orm.setup()
        dataclass = utils.import_data_class(driver_name)
        spatial = SpatialExtent.factory(dataclass, **spatial_spec)
        temporal = TemporalExtent(**temporal_spec)

        # convert spatial_extents into just a stack of tiles
        tiles = set()
        for se in spatial:
            tiles = tiles.union(se.tiles)
            

        status = {s: 0 for s in dbinv.models.status_strings}
        criteria = {
            'driver': driver_name,
            'tile__in': tiles,
            'date__gte': temporal.datebounds[0],
            'date__lte': temporal.datebounds[1],
            'product__in': products,
        }
        for p in dbinv.models.Product.objects.filter(**criteria):
            # TODO: check for daybounds should be built in to query!
            if (
                    p.date.timetuple().tm_yday >= temporal.daybounds[0]
                    and p.date.timetuple().tm_yday <= temporal.daybounds[1]
            ):
                status[p.status] += 1
        return status


def query_service(driver_name, spatial, temporal, products,
                  query_type='missing', action='request-product'):
    '''
    Query (if configured) the data service for files that could be retrieved.

    driver_name -- name of a configured gips data source driver
    spatial -- dictionary of parameters specifying a spatial extent
               (see gips.core.SpatialExtent.factory)
    temporal -- dictionary of TemporalExtent parameters ('dates', and 'days')
    products -- list of products which to query
    query_type --
        + 'remote' get info for all remote items
        + 'missing' only get info for tile-dates that we don't have
        + 'update' get info for missing or updated items
    action --
        + 'request-asset' to set status 'requested' if status not 'in-progress' or 'complete'.
        + 'force-request-asset' to set status 'requested' no matter what current status is.
        + 'request-product' set status 'requested' for product (and implies 'request-asset')
        + 'force-request-product' set status 'requested' no matter what current status is.
        + 'get-info' - do nothing but return that which would have been requested.
    '''
    from time import time

    def tprint(tslist):
        last = tslist[0]
        print('---')
        print(str((0, last)))
        for ts in tslist[1:]:
            print('{:0.05f}: {}'.format(ts[0] - last[0], ts))
            last = ts
        print('_-_-_\ntotal: {:0.05f}'.format(tslist[-1][0] - tslist[0][0]))

    tstamps = [(time(), 'init')]

    orm.setup()
    with utils.error_handler(
            'DataHandler query parameter error: {}, {}, {}, {}'
            .format(driver_name, spatial, temporal, products)
    ):
        if type(products) in [str, unicode]:
            products = [products]
        datacls = utils.import_data_class(driver_name)
        spatial_exts = SpatialExtent.factory(datacls, **spatial)
        temporal_ext = TemporalExtent(**temporal)

    tstamps.append((time(), 'space-time params'))

    # convert spatial_extents into just a stack of tiles
    tiles = set()
    for se in spatial_exts:
        tiles = tiles.union(se.tiles)

    tstamps.append((time(), 'union tiles'))
    tprint(tstamps)

    # based on query_type, determine how adamantly to query
    update = False
    force = False
    if query_type == 'remote':
        force = True
    elif query_type == 'missing':
        pass
    elif query_type == 'update':
        force = True
        update = True
    else:
        raise NotImplemented('query_service: query_type "{}" not implemented'
                             .format(query_type))
    # query data service
    items = datacls.query_service(
        products, tiles, temporal_ext,
        update=update, force=force, grouped=True
    )

    tstamps.append((time(), 'queried service'))
    tprint(tstamps)

    # actions: status,[force-]request-asset,[force-]request-product,delete,
    request_asset = False
    request_product = False
    if action.endswith('request-asset') or action.endswith('request-product'):
        request_asset = True
        if action.endswith('request-product'):
            request_product = True
    elif action == 'get-info':
        tprint(tstamps)
        return items
    else:
        raise NotImplemented('query_service: action "{}" not implemented'
                             .format(action))
    force = action.startswith('force')

    # set status 'requested' on items (products and/or assets)
    req_status = 'requested'
    for i in items:
        print i
        (p, t, d) = i
        assets = []
        for a in items[i]:
            print a
            if request_asset:
                params = {
                    'driver': driver_name, 'asset': a['asset'],
                    'tile': a['tile'], 'date': a['date']
                }
                with transaction.atomic():
                    try:
                        asset = dbinv.models.Asset.objects.get(**params)
                        if force or asset.status not in ('scheduled', 'in-progress', 'complete'):
                            asset.status = req_status
                            asset.save()
                    except ObjectDoesNotExist:
                        params['status'] = req_status
                        asset = dbinv.models.Asset(**params)
                        asset.save()
                assets.append(asset)
        if request_product:
            params = {
                'driver': driver_name, 'product': p,
                'tile': t, 'date': d
            }
            with transaction.atomic():
                try:
                    product = dbinv.models.Product.objects.get(**params)
                    if product.status not in ('scheduled', 'in-progress', 'complete'):
                        product.status = req_status
                        product.save()
                except ObjectDoesNotExist:
                    params['status'] = req_status
                    product = dbinv.models.Product(**params)
                    product.save()
                    for asset in assets:
                        dep = dbinv.models.AssetDependency(product=product, asset=asset)
                        dep.save()
    tstamps.append((time(), 'marked requested'))
    tprint(tstamps)
    return items
