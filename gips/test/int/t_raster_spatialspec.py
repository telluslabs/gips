import pytest
import os
import subprocess
from gips import utils
from gips.core import SpatialExtent
from ..sys.util import *

def t_raster_spatialspec():
    """Test that shapefile and rastermask return the same tile list"""
    with utils.make_temp_dir(prefix='t_gridded_inventory') as td:
        rastermask = os.path.join(td, 'nhseacost_mask.tif')

        rasterize = (
            'gdal_rasterize -burn 1 -ot Byte -tr 30 30 {} {}'
            .format(NH_SHP_PATH, rastermask)
        )
        status, output = subprocess.getstatusoutput(rasterize)
        assert status == 0

        cls = utils.import_data_class('modis')
        s_extents = SpatialExtent.factory(cls, site=NH_SHP_PATH)
        r_extents = SpatialExtent.factory(cls, rastermask=rastermask)

        assert len(s_extents) == len(r_extents)
        for i in range(len(r_extents)):
            assert s_extents[i].tiles == r_extents[i].tiles
