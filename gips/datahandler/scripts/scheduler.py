#!/usr/bin/env python

from gips.datahandler import api

def main ():
    schedule_query()
    schedule_fetch()
    schedule_process()
    #schedule_export_and_aggregate()

if __name__ == '__main__':
    main()

    
