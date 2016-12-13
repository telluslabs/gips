from __future__ import unicode_literals

from django.contrib.gis.db import models
from django.contrib.postgres.fields import HStoreField


class Status(models.Model):
    """Status of asset or product"""

    # present valid status values (taken from fixtures/dbinv_status.json):
    # requested, in-progress, complete, failed
    status = models.TextField()


class Asset(models.Model):
    """Inventory for assets, which are downloaded files from data sources.

    Assets undergo little or no processing.  GIPS generates products
    from assets.
    """
    # max_length chosen somewhat arbitrarily since neither of our expected DB backends care (django
    # ORM is a stickler for no discernible reason).
    driver = models.TextField(db_index=True)   # eg 'modis' or 'landsat'
    asset  = models.TextField(db_index=True)   # 'MYD11A1'
    sensor = models.TextField(db_index=True)   # 'MYD'
    tile   = models.TextField(db_index=True)   # 'h12v04'
    date   = models.DateField(db_index=True)   # of observation, not production
    name   = models.TextField()                # file name including full path
    status = models.ForeignKey(Status)         #

    class Meta:
        # These four columns uniquely identify an asset file
        unique_together = ('driver', 'asset', 'tile', 'date')


class Product(models.Model):
    """Inventory for products, which GIPS generates from Assets.

    Main difference from Assets is to replace the asset field with a
    product field.
    """
    # max_length chosen somewhat arbitrarily since neither of our expected DB backends care (django
    # ORM is a stickler for no discernible reason).
    driver  = models.TextField(db_index=True)   # eg 'modis' or 'landsat'
    product = models.TextField(db_index=True)   # 'fsnow'
    sensor  = models.TextField(db_index=True)   # 'MYD'
    tile    = models.TextField(db_index=True)   # 'h12v04'
    date    = models.DateField(db_index=True)   # of observation, not production
    name    = models.TextField()                # file name including full path
    status  = models.ForeignKey(Status)         #

    class Meta:
        # These four columns uniquely identify an asset file
        unique_together = ('driver', 'product', 'tile', 'date')


class Vector(models.Model):
    geom       = models.GeometryField()
    name       = models.CharField(max_length=255)
    attributes = HStoreField()
    site       = models.CharField(max_length=255, null=True, blank=True)
    source     = models.CharField(max_length=255)
    type       = models.CharField(max_length=255)
    fid        = models.IntegerField()

    class Meta:
        unique_together = ('fid', 'source')


class DataVariable(models.Model):
    """Inventory of Data Variables.

    Data variables are individual product bands specified by the driver
    """

    name        = models.CharField(max_length=255, unique=True)
    description = models.CharField(max_length=255)
    driver      = models.CharField(max_length=255)
    product     = models.CharField(max_length=255)
    band        = models.CharField(max_length=255)
    band_number = models.IntegerField(default=0)


class Result(models.Model):
    """Results from spatial aggregation operations."""

    feature_set = models.CharField(max_length=255)
    count       = models.IntegerField(blank=True, null=True)
    date        = models.DateField()
    maximum     = models.FloatField(null=True, blank=True)
    mean        = models.FloatField(null=True, blank=True)
    skew        = models.FloatField(null=True, blank=True)
    minimum     = models.FloatField(null=True, blank=True)
    product     = models.ForeignKey(DataVariable)
    sd          = models.FloatField(null=True, blank=True)
    fid         = models.IntegerField()
    site        = models.CharField(max_length=255)
    vector      = models.ForeignKey(Vector)

    class Meta:
        unique_together = ('feature_set', 'date', 'product', 'site')
