"""GIPS scheduler API, for scheduling work and checking status of same."""

from gips import utils

from gips.datahandler import torque


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

