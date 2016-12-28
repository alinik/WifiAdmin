from __future__ import unicode_literals

from django.db import models
# Create your models here.
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class Poi(models.Model):
    status = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    province = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    poi_type = models.CharField(max_length=100)
    type = models.CharField(max_length=100)
    desc = models.CharField(max_length=100)
    lat = models.CharField(max_length=100)
    lon = models.CharField(max_length=100)
    address = models.CharField(max_length=100)

# class PoiAddInfo(models.Model):
    poi = models.OneToOneField
    rush_hours = models.CharField(max_length=100)
    floor = models.CharField(max_length=100)
    area = models.CharField(max_length=100)
    staff_count = models.CharField(max_length=100)
    avg_move_in_floor = models.CharField(max_length=100)
    days = models.CharField(max_length=100)

    fiber = models.NullBooleanField(default=False)
    wifi = models.NullBooleanField(default=False)
    irancell = models.NullBooleanField(default=False)
    rightel = models.NullBooleanField(default=False)
    mci = models.NullBooleanField(default=False)
    das_in_ibs = models.NullBooleanField(default=False)
    adsl = models.NullBooleanField(default=False)
    power = models.NullBooleanField(default=False)
    ac_type = models.NullBooleanField(default=False)

    activity_duration = models.CharField(max_length=100)
    activity = models.CharField(max_length=100)
