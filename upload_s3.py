#!/usr/bin/python

import os
import re
import click


STARTPATH = "/archive/export/{}_ard_{}"

SENSORS = {'LE7': 'l7rt', 'LC8': 'l8rt', 'S2A': 's2rt', 'S2B': 's2rt'}

PATTERN = "^\d{7}_(\w{3})_\w{3,4}-masked_(.*)\.tif$"

S3PATTERN = "{0}/{5}/{1}/conus_ard/{2}/{5}_{1}_conus_ard_{2}_{3}_{4}.tif"


@click.command()
#@click.option('--sensor', required=True)
#@click.option('--date', required=True)
@click.option('--startpath', required=True)
@click.option('--s3prefix', required=True)
def upload(startpath,  s3prefix):
    s3prefix = 's3://' + s3prefix
    #startpath = STARTPATH.format(sensor, date)

    for basename, _, filenames in os.walk(startpath):

        for filename in filenames:
            filepath = os.path.join(basename, filename)

            match = re.match(PATTERN, filename)

            if not match:
                continue

            sensorabbrev = match.groups()[0]
            sensorname = SENSORS[sensorabbrev]
            bandname = match.groups()[1]

            date = basename.split('/')[-2].split('_')[-1].replace('-', '')

            tile_h = str(int(basename.split('/')[-1][:2]))
            tile_v = str(int(basename.split('/')[-1][2:]))

            s3path = S3PATTERN.format(
                s3prefix, bandname, date, tile_h, tile_v, sensorname)

            cmd = "aws s3 cp {} {}".format(filepath, s3path)
            status = os.system(cmd)
            assert status == 0, "command failed: {}".format(cmd)


if __name__ == "__main__":
    try:
        upload()
    except Exception as e:
        print(e)
        raise
