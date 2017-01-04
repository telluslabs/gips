from __future__ import unicode_literals

from django.contrib.gis.db import models
from django.contrib.postgres.fields import HStoreField
from django.core.exceptions import ValidationError

status_strings = ('remote',
                  'requested',
                  'initializing',  # this is only used at the job level
                  'scheduled',
                  'in-progress',
                  'pp-scheduled', # name TBD. only used at job level
                  'post-processing', # only used at job level
                  'complete',
                  'failed')

def valid_status(val):
    if val not in status_strings:
        raise ValidationError("invalid status: {}".format(val))


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
    status = models.TextField(validators=[valid_status])

    class Meta:
        # These four columns uniquely identify an asset file
        unique_together = ('driver', 'asset', 'tile', 'date')

    # TODO: this is clunky and makes multiple round trips, and is repetitive
    #       seems to beg to be a trigger
    def save(self, *args, **kwargs):
        if self.pk is not None:
            orig = Asset.objects.get(pk=self.pk)
            super(Asset, self).save(*args, **kwargs)
            if orig.status != self.status:
                change = AssetStatusChange(asset=self, status=self.status)
                change.save()
        else:
            super(Asset, self).save(*args, **kwargs)
            change = AssetStatusChange(asset=self, status=self.status)
            change.save()


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
    status = models.TextField(validators=[valid_status])

    class Meta:
        # These four columns uniquely identify an asset file
        unique_together = ('driver', 'product', 'tile', 'date')

    # TODO: this is clunky and makes multiple round trips, and is repetitive
    #       seems to beg to be a trigger
    def save(self, *args, **kwargs):
        if self.pk is not None:
            orig = Product.objects.get(pk=self.pk)
            super(Product, self).save(*args, **kwargs)
            if orig.status != self.status:
                change = ProductStatusChange(product=self, status=self.status)
                change.save()
        else:
            super(Product, self).save(*args, **kwargs)
            change = ProductStatusChange(product=self, status=self.status)
            change.save()

class AssetDependency(models.Model):
    """Dependencies of products on specific assets"""
    product = models.ForeignKey(Product)
    asset   = models.ForeignKey(Asset)

    class Meta:
        unique_together = ('product', 'asset')


class AssetStatusChange(models.Model):
    """Record of times product status updates"""

    asset   = models.ForeignKey(Asset)
    status  = models.TextField(validators=[valid_status])
    time    = models.DateTimeField(auto_now_add=True)


class ProductStatusChange(models.Model):
    """Record of times product status updates"""

    product = models.ForeignKey(Product)
    status  = models.TextField(validators=[valid_status])
    time    = models.DateTimeField(auto_now_add=True)


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
    asset_link  = models.TextField(null=True, blank=True)
    asset       = models.CharField(max_length=255, null=True, blank=True)
    description = models.CharField(max_length=255)
    driver      = models.CharField(max_length=255)
    product     = models.CharField(max_length=255)
    band        = models.CharField(max_length=255)
    band_number = models.IntegerField(default=0)
    unit        = models.CharField(max_length=255, null=True, blank=True)


class Result(models.Model):
    """Results from spatial aggregation operations."""

    count       = models.IntegerField(blank=True, null=True)
    date        = models.DateField()
    job         = models.ForeignKey('Job')
    maximum     = models.FloatField(null=True, blank=True)
    mean        = models.FloatField(null=True, blank=True)
    skew        = models.FloatField(null=True, blank=True)
    minimum     = models.FloatField(null=True, blank=True)
    sd          = models.FloatField(null=True, blank=True)
    fid         = models.IntegerField()
    site        = models.CharField(max_length=255)
    vector      = models.ForeignKey(Vector, null=True, blank=True)

    class Meta:
        unique_together = ('job', 'date', 'site')


class Job(models.Model):
    """Description of gips job to be processed"""

    site     = models.CharField(max_length=255)
    variable = models.ForeignKey(DataVariable)
    spatial  = models.TextField()
    temporal = models.TextField()
    # TODO: aggregation method?
    status   = models.TextField(validators=[valid_status])

    class Meta:
        unique_together = ('site', 'variable', 'spatial', 'temporal')

