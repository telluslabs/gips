#!/usr/bin/env python

import pprint

from gips.datahandler import api

def print_outcomes(kind, outcomes):
    if outcomes is not None and len(outcomes) > 0: # then there was something to do:
        print kind, "job(s) located and submitted:"
        [pprint.pprint(outcome) for outcome in outcomes]


def main ():
    outcomes = api.schedule_query()
    print_outcomes('Query', outcomes)

    outcomes = api.schedule_fetch()
    print_outcomes('Fetch', outcomes)

    outcomes = api.schedule_process()
    print_outcomes('Process', outcomes)

    #outcomes = api.schedule_export_and_aggregate()
    #print_outcomes('Export & Aggregate', outcomes)

if __name__ == '__main__':
    main()

    
