from __future__ import unicode_literals

from django.contrib.gis.db import models
from django.contrib.postgres.fields import HStoreField
from django.core.exceptions import ValidationError

def valid_status(val):
    if val not in ('remote',
                   'requested',
                   'in-progress',
                   'complete',
                   'failed'):
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
            super(Asset, self).save(*args, **kwargs)
            if orig.status != self.status:
                change = ProductStatusChange(product=self, status=self.status)
                change.save()
        else:
            super(Asset, self).save(*args, **kwargs)
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

    class Meta:
        unique_together = ('asset', 'status')

        
class ProductStatusChange(models.Model):
    """Record of times product status updates"""

    product = models.ForeignKey(Product)
    status  = models.TextField(validators=[valid_status])
    time    = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('product', 'status')

        
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
    vector      = models.ForeignKey(Vector, null=True, blank=True)

    class Meta:
        unique_together = ('feature_set', 'date', 'product', 'site')
