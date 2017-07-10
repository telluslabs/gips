"""GIPS scheduler API, for scheduling work and checking status of same."""

import itertools
from datetime import timedelta, datetime
from pprint import pprint, pformat

from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.db.models import Count
from django.forms.models import model_to_dict

from gips import utils
from gips.core import SpatialExtent, TemporalExtent

from gips.inventory import dbinv, orm
from gips.datahandler.logger import Logger
#from pdb import set_trace


def get_catalog ():
    """Return list of installed DataVariables as dicts"""
    orm.setup()
    dv_list = []
    dvs = dbinv.models.DataVariable.objects.all()
    for dv in dvs:
        d = model_to_dict(dv)
        d['asset'] = eval(d['asset'])
        # xmlrpclib doesn't like datetime.date, convert to datetime.datetime
        d['start_date'] = datetime.fromordinal(d['start_date'].toordinal())
        dv_list.append(d)
    return dv_list


def submit_request (site, variable, spatial, temporal):
    """Pass a work spec in to the scheduler, and the work will be done.

    site:           geokit site id
    variable:       DataVariable.name
    spatial:        dictionary of parameters specifying a spatial extent
                    (see gips.core.SpatialExtent.factory)
    temporal:       dictionary of TemporalExtent parameters ('dates' and 'days')
    """
    Logger().log("submit_job: {} {} {} {}".format(site, variable,
                                                  spatial, temporal))
    orm.setup()
    job, created = dbinv.models.Job.objects.get_or_create(
        site=site,
        variable=dbinv.models.DataVariable.objects.get(name=variable),
        spatial=repr(spatial),
        temporal=repr(temporal),
        defaults={'status':'requested'},
    )

    Logger().log("submit_job: returned jobid {}".format(job.pk))
    return job.pk


def status_counts(driver_name, spatial_spec, temporal_spec, assets=None, products=None):
    """Status of assets and/or products matching the given criteria:

    :driver_name:   eg 'landsat' or 'modis'; used to choose a Data class.
    :spatial_spec:  Dict; used for SpatialExtent.factory(..., **spatial_spec)
    :temporal_spec: Dict; used for TemporalExtent(**temporal_spec)
    :products:      List of requested product types, eg ['fsnow', ...]

    The return value is (asset_dict, product_dict), each mapping status
    strings to counts of items with that status.  For instance:
    {'requested': 1, 'complete': 2, ...}.
    Leave either kind of item as None to return a single dict instead of a tuple.
    """
    if (assets, products) == (None, None):
        raise ValueError("At least one of (assets, products) must be specified")
    orm.setup()
    dataclass = utils.import_data_class(driver_name)
    spatial = SpatialExtent.factory(dataclass, **spatial_spec)
    temporal = TemporalExtent(**temporal_spec)

    # convert spatial_extents into just a stack of tiles
    tiles = set()
    for se in spatial:
        tiles = tiles.union(se.tiles)

    base_criteria = {
        'driver': driver_name,
        'tile__in': tiles,
        'date__gte': temporal.datebounds[0],
        'date__lte': temporal.datebounds[1],
    }

    # TODO: check for daybounds should be built in to query!
    low_daybound, high_daybound = temporal.daybounds[0:2]

    ret_val = ()

    if assets is not None:
        a_counts = {s: 0 for s in dbinv.models.status_values['asset']}
        for a in dbinv.models.Asset.objects.filter(asset__in=assets, **base_criteria):
            if low_daybound <= a.date.timetuple().tm_yday <= high_daybound:
                a_counts[a.status] += 1
        ret_val += (a_counts,)

    if products is not None:
        p_counts = {s: 0 for s in dbinv.models.status_values['product']}
        for p in dbinv.models.Product.objects.filter(product__in=products, **base_criteria):
            if low_daybound <= p.date.timetuple().tm_yday <= high_daybound:
                p_counts[p.status] += 1
        ret_val += (p_counts,)

    return ret_val[0] if len(ret_val) == 1 else ret_val # return a tuple only if necessary


def get_status(jobid):
    """Return a status report for the given job.

    Returns (job-status, asset-status, product-status).  Job status is a
    short string or a prose error string.  Asset & product status are
    both dicts.  The keys are all the possible values for status flags.
    The values are the counts of the items in that state for the job.
    """
    orm.setup()
    try:
        job = dbinv.models.Job.objects.get(pk=jobid)
    except dbinv.models.Job.DoesNotExist:
        return "jobid does not exist", {}, {}

    if job.status in('requested', 'initializing', 'scheduled'):
        return job.status, {}, {}

    asset_status, product_status = status_counts(
        job.variable.driver.encode('ascii', 'ignore'),
        eval(job.spatial),
        eval(job.temporal),
        eval(job.variable.asset), # by convention a list
        [job.variable.product.encode('ascii', 'ignore')]
    )
    return job.status, asset_status, product_status
    

def get_results(job_id, filters=None):
    """Get all the results in the specified result set.

    job_id:  Job primary key
    filters: dict to filter results; passed in via django ORM, ie:
             Result.objects.filter(job=job_id, **filters)
    """
    orm.setup()
    qs = dbinv.models.Result.objects.filter(job=job_id)
    if filters:
        qs = qs.filter(**filters)
    result_list = []
    for result in qs:
        r = model_to_dict(result)
        # xmlrpclib doesn't like datetime.date, convert to datetime.datetime
        r['date'] = datetime.fromordinal(r['date'].toordinal())
        result_list.append(r)

    return result_list


def query_service(driver_name, spatial, temporal, products,
                  query_type='missing', action='request-product'):
    '''
    Query (if configured) the data service for files that could be retrieved.

    driver_name -- name of a configured gips data source driver
    spatial -- dictionary of parameters specifying a spatial extent
               (see gips.core.SpatialExtent.factory)
    temporal -- dictionary of TemporalExtent parameters ('dates', and 'days')
    products -- list of products which to query

    Note that query_type and action may not be perfectly implemented,
    and at present, are probably not called with anything other than the
    defaults.

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
    log = Logger().log

    log("query_service starting; args: " + repr((
        driver_name, spatial, temporal, products, query_type, action)))
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
    # query data service for assets
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
        asset_status_picks = ('requested', 'scheduled', 'in-progress', 'retry', 'complete')
        for (p, t) in itertools.product(products, tiles):
            asset_types = datacls.products2assets([p])
            all_dates = [datacls.Asset.dates(a, t, temporal_ext.datebounds, temporal_ext.daybounds)
                            for a in asset_types]
            # clunky syntax for set intersection of each item in all_dates
            # Needed because products can only exist for dates on which all their asset
            # dependencies also exist.
            dates = set(all_dates[0]).intersection(*all_dates)
            for d in dates:
                with transaction.atomic():
                    # first see if asset needs are satisfied/satisfyable
                    relevant_assets = dbinv.models.Asset.objects.filter(
                            asset__in=asset_types, driver=driver_name, tile=t, date=d)

                    # only proceed if the prereqs are expected to be met
                    if (len(asset_types)
                            > relevant_assets.filter(status__in=asset_status_picks).count()):
                        continue

                    product, created = dbinv.models.Product.objects.get_or_create(
                            driver=driver_name, product=p, tile=t, date=d)
                    if product.status not in ('scheduled', 'in-progress', 'complete'):
                        product.status = req_status
                        product.save()
                    if created: # new products need to have dependencies marked
                        [dbinv.models.AssetDependency(product=product, asset=a).save()
                            for a in relevant_assets]

    tstamps.append((time(), 'marked requested'))
    tprint(tstamps)
    return items
