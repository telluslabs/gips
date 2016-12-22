#!/usr/bin/env python

from django.forms.models import model_to_dict
from gips.inventory import orm
orm.setup()
from gips.inventory.dbinv.models import Result


def stats_request_results(request_id):
    """Get all the results in the specified result set.

    Input dict:
    job -- Job primary key
    """
    if not request_id.has_key('job'):
        raise KeyError('Job ID is a required identifier')
    qs = Result.objects.filter(job=request_id['job'])
    result_list = []
    for result in qs:
        result_list.append(model_to_dict(result))

    return result_list


def stats_request_results_filter(request_id, filters):
    """Get all result objects that match specified filters.

    Inputs:
    request_id:
        job -- string identifier
    filters:
        a dictionary containing one or more django filters
    """
    if not request_id.has_key('job'):
        raise KeyError('Job ID is a required identifier')
    qs = Result.objects.filter(job=request_id['job'])
    qs.filter(**filters)
    result_list = []
    for result in qs:
        result_list.append(model_to_dict(result))

    return result_list
    #return Result.objects.filter(feature_set).filter(filters)

