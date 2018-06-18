HOWTO get a MERRA2 time-series for a point
---

1. Buffer your point to a small (1m radius) polygon (`cc_issue.shp`), in a
   projection with units in meters.
2. Run

        (venv) icooke@rio:~$ gips_export merra \
            --fetch \
            -s cc_issue.shp \
            -d 2017-5-1,2017-5-2 \
            --res 1000 1000 \
            --alltouch \
            -p prcp


        GIPS Data Export (v0.11.0-dev)
        No files found; nothing to archive.
          Dates: 2 dates (2017-05-01 - 2017-05-02)
          Products: prcp
            DATE     Coverage  Product  
        2017        
            121     prcp  
            122     prcp  
        
        
        2 files on 2 dates
        (venv) icooke@rio:~$
3. Followed by

        (venv) icooke@rio:~$ gips_stats cc_issue_1000.0x1000.0_merra/0/
        GIPS Image Statistics (v0.1.0)
        Stats for Project directory: cc_issue_1000.0x1000.0_merra/0/
        (venv) icooke@rio:~$ cat cc_issue_1000.0x1000.0_merra/0/prcp_stats.txt 
        date,band,min,max,mean,sd,skew,count
        2017-121,prcp,6.29303,6.29303,6.29303,0.0,nan,1.0
        2017-122,prcp,7.63732,7.63732,7.63732,0.0,nan,1.0

* _N.B._
  The `--alltouch` option is what makes this work out.  w/o that you'd
  have to hit a pixel center in order to get a value.  Additionally, you could
  consider using an alternate interpolation for the sampling of the merra data.
  The default is nearest neighbor.  Others are:
```
  --interpolation {0,1,2}
                        If warping interpolate using: 0-NN, 1-Bilinear,
                        2-Cubic (default: 0)
```
