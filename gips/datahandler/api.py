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


# entry point for Tom's bit for the demo; Tom doesn't go "further up" at the
# moment.
def schedule(assets=None, products=None, export_spec=None, aggregation=None, config=None):
    """Pass a work spec in to the scheduler, and the work will be done.

    Schedules the work by defining and starting a series of jobs managed by a
    supporting task queueing or batching system.

    assets:         list of the form (driver, asset_type, tile, date)
    products:       list of the form (driver, product_type, tile, date)
    export_spec:    TBD gips_project
    aggregation:    TBD zonal summary
    config:         TBD scheduling params such as how the work should be
                    divided; leave as None for a sensible default, which is
                    in turn TBD.

    """
    # TODO does this function set 'requested' on workers?


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
        products, tiles, temporal_ext, update=update, force=force
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
        if request_asset:
            params = {
                'driver': driver_name, 'asset': i['asset'],
                'tile': i['tile'], 'date': i['date']
            }
            try:
                with transaction.atomic():
                    asset = dbinv.models.Asset.objects.get(**params)
                    if force or asset.status not in ('in-progress', 'complete'):
                        asset.status = req_status
                        asset.save()
            except ObjectDoesNotExist:
                params['status'] = req_status
                asset = dbinv.models.Asset(**params)
                asset.save()
        if request_product:
            params.update({'product': i['product'], 'sensor': i['sensor']})
            params.pop('asset')

            if 'status' in params:
                params.pop('status')
            try:
                with transaction.atomic():
                    product = dbinv.models.Product.objects.get(**params)
                    if product.status not in ('in-progress', 'complete'):
                        product.status = req_status
                        product.save()
            except ObjectDoesNotExist:
                params['status'] = req_status
                product = dbinv.models.Product(**params)
                product.save()
    tstamps.append((time(), 'marked requested'))
    tprint(tstamps)
    return items
