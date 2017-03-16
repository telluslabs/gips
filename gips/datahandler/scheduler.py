#!/usr/bin/env python

from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.db.models import Count

import math
from pprint import pprint, pformat

from gips import utils
from gips.core import SpatialExtent, TemporalExtent
from gips.inventory import dbinv, orm
from gips.datahandler import api
from gips.datahandler.logger import Logger
from gips.datahandler import torque


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
            outcomes = torque.submit('query', query_args, 1)
            ids = [{'torque_id': o[0], 'db_id': o[1][0][0]} for o in outcomes]
            Logger().log("Submitted query for job(s):\n{}".format(pformat(ids)))


def schedule_fetch (driver):
    '''
    Submit to torque (or other) fetch jobs for any assets that
    are 'requested'. Mark scheduled assets as 'scheduled'.

    Will be called by a cron'd scheduler job.
    '''

    orm.setup()

    with transaction.atomic():
        # check if another fetch is currently running
        active = dbinv.models.Asset.objects.filter(
            driver=driver,
            status__in=['scheduled', 'in-progress', 'retry']
        )

        # check if jobs still alive
        active_jobs = active.order_by('sched_id').distinct('sched_id')
        for j in active_jobs:
            if j.sched_id and torque.is_job_alive(j.sched_id):
                Logger().log(
                    'Previous {} fetch job still running. Moving on...'
                    .format(driver)
                )
                return
        
        # if anything leftover, clean it up
        needs_cleanup = active.filter(
            assetstatuschange__status='requested',
        ).annotate(
            num_retries=Count('assetstatuschange__status'),
        )
        if needs_cleanup.exists():
            # something went wrong. not 'complete', but no running/scheduled job
            Logger().log('Attempting to reschedule incomplete tasks')

            retries = []
            fails = []
            for a in needs_cleanup:
                if a.num_retries >= 3:
                    fails.append(a)
                    # if it has been retried 3 times, give up
                    a.status = 'failed'
                else:
                    retries.append(a)
                    a.status = 'requested'
                    a.sched_id = ''
                a.save()

            if fails:
                Logger().log(
                    "Fetch failed three times - give up\n{}"
                    .format(pformat([(f.id, f.driver, f.asset, f.tile, f.date)
                                     for f in fails]))
                )
            if retries:
                Logger().log(
                    "Retrying fetch\n{}"
                    .format(pformat([(r.id, r.driver, r.asset, r.tile, r.date)
                                     for r in retries]))
                )
                
    with transaction.atomic():
        # TODO: these should be configured elsewhere
        num_jobs = 10
        per_job = 10
        assets = dbinv.models.Asset.objects.select_for_update().filter(
            driver=driver,
            status='requested',
        ).order_by('id')[:num_jobs*per_job]
        if assets.exists():
            fetch_args = [ [a.pk] for a in assets ]
            outcomes = torque.submit('fetch', fetch_args, per_job, chain=True)
            print outcomes
            dbinv.models.update_status(assets, 'scheduled')
            ids = [
                {
                    'torque_id': o[0],
                    'assets': [a[0] for a in o[1]],
                }
                for o in outcomes
            ]
            for i in ids:
                a = dbinv.models.Asset.objects.filter(
                    id__in=i['assets']
                ).update(
                    sched_id=i['torque_id']
                )
                print "len", a
            Logger().log('scheduled fetch job(s):\n{}'.format(pformat(ids)))


def schedule_process ():
    '''
    Submit to torque (or other?) jobs to process any products that are
    ready to be processed - i.e. are 'requested' and all asset
    dependencies are 'complete'. Mark scheduled products as 'scheduled'.

x    Will be called by a cron'd scheduler job
    '''

    orm.setup()
    from django.db.models import Q
    with transaction.atomic():
        products = dbinv.models.Product.objects.select_for_update().filter(
            status='requested'
        ).exclude(
            ~Q(assetdependency__asset__status='complete')
        )
        if products.exists():
            process_args = [ [p.pk] for p in products ]
            outcomes = torque.submit('process', process_args, 5)
            print outcomes
            dbinv.models.update_status(products, 'scheduled')
            ids = [
                {
                    'torque_id': o[0],
                    'products': [p[0] for p in o[1]]
                }
                for o in outcomes
            ]
            for i in ids:
                p = dbinv.models.Product.objects.filter(
                    id__in=i['products']
                ).update(
                    sched_id=i['torque_id']
                )
            Logger().log('scheduled process job(s):\n{}'.format(pformat(ids)))


def schedule_export_and_aggregate ():
    '''
    Check all Jobs to see if  ready for post-processing (all assets fetched and
    all products processed). If so, submit export and aggregate jobs
    to torque (or other?) 

    Will be called by a cron'd scheduler job

    '''
    orm.setup()
    # check if any in-progress jobs have finished fetch/process
    jobs = dbinv.models.Job.objects.filter(
        status='in-progress',
    )
    for job in jobs:
        status = api.processing_status(
            job.variable.driver.encode('ascii', 'ignore'),
            eval(job.spatial),
            eval(job.temporal),
            [job.variable.product.encode('ascii', 'ignore')],
        )
        if (
                status['requested'] == 0
                and status['scheduled'] == 0
                and status['in-progress'] == 0
                and status['retry'] == 0
        ):
            Logger().log('job {} has finished fetch and process'.format(job.pk))
            # nothing being worked on. must be done pre-processing
            DataClass = utils.import_data_class(job.variable.driver.encode('ascii', 'ignore'))
            spatial_spec = eval(job.spatial)
            extents = SpatialExtent.factory(DataClass, **spatial_spec)
                
            num_ext = len(extents)
            print "num_ext", num_ext
            # TODO: make this configurable
            ext_per = 10 if num_ext > 15 else num_ext
            make_args = lambda i: [
                job.pk,
                i*ext_per,
                (i+1)*ext_per if (i+1)*ext_per < num_ext else num_ext
            ]
            job_args = [make_args(i)
                        for i in range(int(math.ceil(num_ext / ext_per)))]
            with transaction.atomic():
                for j in job_args:
                    pp = dbinv.models.PostProcessJobs(
                        job = job,
                        args = repr(tuple(j)),
                        status = 'scheduled',
                    )
                    pp.save()
            # put this in a seperate transaction. the postprocessjobs need to exist before
            # submitting jobs
            with transaction.atomic():
                outcomes = torque.submit('export_and_aggregate', job_args, 1)
                for o in outcomes:
                    pp = dbinv.models.PostProcessJobs.objects.select_for_update().get(
                        job = job,
                        args = repr(tuple(o[1][0])),
                    )
                    pp.sched_id = o[0]
                    pp.save()
                job.refresh_from_db()
                job.status = 'post-processing'
                job.save()

                Logger().log('scheduled postprocess job(s):\n{}'.format(pformat(outcomes)))

    # check whether any post-processing jobs have finished
    with transaction.atomic():
        jobs = dbinv.models.Job.objects.select_for_update().filter(
            status='post-processing',
        )
        for job in jobs:
            tasks = job.postprocessjobs_set.all()
            failed = False
            complete = True
            for task in tasks:
                if task.status != 'complete':
                    complete = False
                if task.status in ('scheduled', 'in-progress'):
                    # make sure jobs are still queued / running
                    if not torque.is_job_alive(task.sched_id):
                        Logger().log("task {} for job {} failed to complete"
                                     .format(task.sched_id, job.pk))
                        task.status = 'failed'
                        task.save()
                        failed = True
                    else:
                        # something is still working. move on
                        break 
                    
            if failed:
                job.status = 'failed'
                job.save()
            elif complete:
                job.status = 'complete'
                job.save()


def print_outcomes(kind, outcomes):
    if outcomes is not None and len(outcomes) > 0: # then there was something to do:
        print kind, "job(s) located and submitted:"
        [pprint(outcome) for outcome in outcomes]


def main ():
    outcomes = schedule_query()
    print_outcomes('Query', outcomes)

    for driver in utils.settings().REPOS.keys():
        outcomes = schedule_fetch(driver)
        print_outcomes('Fetch', outcomes)

    outcomes = schedule_process()
    print_outcomes('Process', outcomes)

    outcomes = schedule_export_and_aggregate()
    print_outcomes('Export & Aggregate', outcomes)

if __name__ == '__main__':
    main()

    
 
