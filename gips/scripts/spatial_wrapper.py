#!/usr/bin/env python
import argparse
import sys
import os
# Setup django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "gips.inventory.orm.settings")
import django
django.setup()
from gips.tools import SpatialAggregator
from gips.utils import VerboseOut
from gips.inventory.dbinv.models import Result, DataVariable, Vector, Job
from gips import settings

def make_result(result, g_dv, g_id):
    key = result[0]
    bands = result[1]

    date = key[0]
    fid = int(key[2])

    for band in bands.keys():
        stats = bands[band]

        minimum = float(stats[0]) if stats[0] != 'nan' else None
        maximum = float(stats[1]) if stats[1] != 'nan' else None
        mean = float(stats[2]) if stats[2] != 'nan' else None
        sd = float(stats[3]) if stats[3] != 'nan' else None
        skew = float(stats[4]) if stats[4] != 'nan' else None
        count = float(stats[5]) if stats[5] != 'nan' else None

        r = Result(
            date=date,
            fid=fid,
            minimum=minimum,
            maximum=maximum,
            job=get_job(g_id),
            mean=mean,
            sd=sd,
            skew=skew,
            count=count,
        )
        try:
            r.save()
        except django.db.utils.IntegrityError:
            # Result already exists, skip it
            pass


def get_job(job):
    try:
        job = Job.objects.get(id=job)
    except django.core.exceptions.ObjectDoesNotExist:
        VerboseOut('Job with id {} does not exist'.format(job))
        exit(1)

    return job


def main():
    path = os.path.dirname(os.path.abspath(__file__))
    desc = '''A wrapper for the Spatial Aggregator tool which creates Result
        objects from the output.'''
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument(
        '-d',
        '--projdir',
        required=True,
        help='Gips inventory directory',
        default=path

    )
    parser.add_argument(
        '-j',
        '--job',
        type=int,
        help='Job ID',
        required=True
    )
    parser.add_argument(
        '-n',
        '--num-procs',
        help='Number of processors to use',
        default=1
    )

    init_args = parser.parse_args()
    projdir = init_args.projdir
    job = get_job(init_args.job)
    g_id = job.pk
    g_dv = job.variable
    nprocs = init_args.num_procs

    proj_name = os.path.basename(os.path.dirname(projdir))

    args = {
        'bands': [g_dv.band_number],
        'products': [g_dv.product],
        'projdir': projdir,
        'processes': nprocs,

    }

    results = SpatialAggregator.aggregate(**args)
    for r in results:
        make_result(r, g_dv, g_id)

if __name__ == "__main__":
    main()
