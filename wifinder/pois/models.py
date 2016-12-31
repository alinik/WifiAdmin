from __future__ import unicode_literals

from cities_light.models import Country, City, Region
from django.db import models
# Create your models here.
from django.utils.encoding import python_2_unicode_compatible
from geoposition.fields import GeopositionField


@python_2_unicode_compatible
class Poi(models.Model):
    STATUS = (
        ('nominal', 'Nominal'),
        ('sa_done', 'S.A Done'),
        ('ap_installation_done', 'A.P.Installation.Done'),
        ('bh_installation_done', 'B.H.Installation.Done'),
        ('onair', 'On - Air'),
        ('switched_off', 'Switched Off'),
        ('undefined', 'undefined'))
    TYPES = (('indoor', 'Indoor'), ('outdoor', 'Outdoor'))

    name = models.CharField(max_length=50)
    status = models.CharField(max_length=50, choices=STATUS)

    country = models.ForeignKey(Country)
    city = models.ForeignKey(City)
    region = models.ForeignKey(Region)
    type = models.CharField(max_length=30, choices=TYPES,null=True)
    desc = models.CharField(max_length=200,null=True,blank=True)
    location = GeopositionField()
    address = models.CharField(max_length=200, null=True)

    rush_hours = models.CharField(max_length=100, null=True)
    floor = models.CharField(max_length=100, null=True)
    area = models.CharField(max_length=100, null=True)
    staff_count = models.CharField(max_length=100, null=True)
    avg_move_in_floor = models.CharField(max_length=100, null=True)
    days = models.CharField(max_length=100, null=True)

    fiber = models.NullBooleanField(default=False)
    wifi = models.NullBooleanField(default=False)
    irancell = models.NullBooleanField(default=False)
    rightel = models.NullBooleanField(default=False)
    mci = models.NullBooleanField(default=False)
    das_in_ibs = models.NullBooleanField(default=False)
    adsl = models.NullBooleanField(default=False)
    power = models.NullBooleanField(default=False)
    ac_type = models.NullBooleanField(default=False)

    activity_duration = models.CharField(max_length=100, null=True)
    activity = models.CharField(max_length=100, null=True)
