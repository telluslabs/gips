#!/usr/bin/env python

from django.forms.models import model_to_dict
from gips.inventory import orm
orm.setup()
from gips.inventory.dbinv.models import Result


def stats_request_results(request_id):
    """Get all the results in the specified result set.
    return Result.objects.filter(feature_set=result_set)

    Input dict:
    feature_set -- string identifier
    """
    if not request_id.has_key('feature_set'):
        raise KeyError('feature_set is a required identifier')
    qs = Result.objects.filter(feature_set=request_id['feature_set'])
    result_list = []
    for result in qs:
        result_list.append(model_to_dict(result))

    return result_list


def stats_request_results_filter(request_id, filters):
    """Get all result objects that match specified filters.

    Inputs:
    request_id:
        feature_set -- string identifier
    filters:
        a dictionary containing one or more django filters
    """
    if not request_id.has_key('feature_set'):
        raise KeyError('feature_set is a required identifier')
    qs = Result.objects.filter(feature_set=request_id['feature_set'])
    qs.filter(**filters)
    result_list = []
    for result in qs:
        result_list.append(model_to_dict(result))

    return result_list
    #return Result.objects.filter(feature_set).filter(filters)

