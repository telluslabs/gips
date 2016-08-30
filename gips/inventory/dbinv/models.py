from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Asset(models.Model):
    """Inventory for assets, which are downloaded files from data sources.

    Assets undergo little or no processing.  GIPS generates products from assets.
    """
    # max_length chosen somewhat arbitrarily since neither of our expected DB backends care (django
    # ORM is a stickler for no discernible reason).
    driver = models.CharField(db_index=True, max_length=15)   # eg 'modis' or 'landsat'
    asset  = models.CharField(db_index=True, max_length=7)    # 'MYD11A1'
    sensor = models.CharField(db_index=True, max_length=7)    # 'MYD'
    tile   = models.CharField(db_index=True, max_length=15)   # 'h12v04'
    date   = models.DateField(db_index=True)                  # of observation, not production
    name   = models.CharField(max_length=255)                 # full path to file name

    class Meta:
        # These four columns uniquely identify an asset file
        unique_together = ('driver', 'asset', 'tile', 'date')
