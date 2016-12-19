#!/usr/bin/env python

from gips.datahandler import api

def main ():
    api.schedule_query()
    api.schedule_fetch()
    api.schedule_process()
    #api.schedule_export_and_aggregate()

if __name__ == '__main__':
    main()

    
