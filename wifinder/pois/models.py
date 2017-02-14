from __future__ import unicode_literals

import sequences
from cities_light.models import Country, City, Region
from colorfield.fields import ColorField
from colorful.fields import RGBColorField
from django.db import models
# Create your models here.
from django.utils.encoding import python_2_unicode_compatible
from geoposition.fields import GeopositionField


class Status(models.Model):
    name = models.CharField(max_length=50)
    name_persian = models.CharField(max_length=100)
    active = models.BooleanField(default=True)
    color = RGBColorField(default='#808080')

    def __str__(self):
        return self.name

    def display_color(self):
        return '<span style="width:5px;height:5px;color:%(color)s">%(color)s</span>' % {'color': self.color}

    display_color.short_description = 'Color'
    display_color.allow_tags = True


@python_2_unicode_compatible
class Poi(models.Model):
    TYPES = (('indoor', 'Indoor'), ('outdoor', 'Outdoor'))

    name = models.CharField(max_length=100)
    status = models.ForeignKey(Status)

    city = models.ForeignKey(City)
    type = models.CharField(max_length=800, choices=TYPES, null=True, blank=True)
    desc = models.CharField(max_length=200, null=True, blank=True)
    location = GeopositionField()
    address = models.CharField(max_length=200, null=True, blank=True)

    rush_hours = models.CharField(max_length=100, null=True, blank=True)
    floor = models.CharField(max_length=100, null=True, blank=True)
    area = models.CharField(max_length=100, null=True, blank=True)
    staff_count = models.CharField(max_length=100, null=True, blank=True)
    avg_move_in_floor = models.CharField(max_length=100, null=True, blank=True)
    days = models.CharField(max_length=100, null=True, blank=True)

    fiber = models.NullBooleanField(default=False)
    wifi = models.NullBooleanField(default=False)
    irancell = models.NullBooleanField(default=False)
    rightel = models.NullBooleanField(default=False)
    mci = models.NullBooleanField(default=False)
    das_in_ibs = models.NullBooleanField(default=False)
    adsl = models.NullBooleanField(default=False)
    power = models.NullBooleanField(default=False)
    ac_type = models.NullBooleanField(default=False)

    activity_duration = models.CharField(max_length=100, null=True, blank=True)
    activity = models.CharField(max_length=100, null=True, blank=True)

    @property
    def country(self):
        """Poi.objects.values('city__country__name').annotate(c=Count('city__country__name'))"""
        return self.city.country

    @property
    def region(self):
        """Poi.objects.values('city__region__name').annotate(c=Count('city__region__name'))"""
        return self.city.region

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        """Increase version based on updating poi"""
        sequences.get_next_value('version')
        return super(Poi, self).save(force_insert, force_update, using, update_fields)


class AvailableField(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class DisplayRole(models.Model):
    name = models.CharField(max_length=100)
    fields = models.ManyToManyField(AvailableField)
    statuses = models.ManyToManyField(Status)

    def __str__(self):
        return self.name
