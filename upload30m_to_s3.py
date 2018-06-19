import os
import re
import click


SENSORS = {'LE7': 'l7rt', 'LC8':'l8rt', 'S2A':'s2rt', 'S2B':'s2rt'}
PATTERN = "^\d{7}_(\w{3})_\w{3,4}-masked_(.*)\.tif$"


@click.command()
@click.option('--s3')
@click.option('--inname')
@click.option('--name')
@click.option('--sensor')
@click.option('--date')
def upload(s3, inname, name, sensor, date):

    s3prefix = "s3://" + s3
    startpathpatt = "/archive/export/{{}}_{}_{{}}".format(inname)
    startpath = startpathpatt.format(sensor, date)

    for basename, _, filenames in os.walk(startpath):

        for filename in filenames:
            filepath = os.path.join(basename, filename)

            match = re.match(PATTERN, filename)

            if not match:
                continue

            sensorabbrev = match.groups()[0]
            sensorname = SENSORS[sensorabbrev]
            bandname = match.groups()[1]

            date = basename.split('/')[-2].split('_')[-1].replace('-','')

            tile_h = str(int(basename.split('/')[-1][:2]))
            tile_v = str(int(basename.split('/')[-1][2:]))

            #s3path = "{0}/{5}/{1}/conus_ard/{2}/{5}_{1}_conus_ard_{2}_{3}_{4}.tif"\
            #         .format(s3prefix, bandname, date, tile_h, tile_v, sensorname)

            #s3path = "{0}/{5}/{1}/{6}/{2}/{5}_{1}_{6}_{2}_{3}_{4}.tif"\
            #         .format(s3prefix, bandname, date, tile_h, tile_v, sensorname, name)

            s3path = "{0}/{1}/{2}/{3}/{4}/{1}_{2}_{3}_{4}_{5}_{6}.tif"\
                     .format(s3prefix, sensorname, bandname, name, date, tile_h, tile_v)


            cmd = "aws s3 cp {} {}".format(filepath, s3path)
            print cmd
            status = os.system(cmd)
            assert status == 0, "command failed: {}".format(cmd)


if __name__ == "__main__":
    upload()
