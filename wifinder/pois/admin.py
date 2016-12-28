from django.contrib import admin

# Register your models here.
from wifinder.pois.models import Poi


@admin.register(Poi)
class PoiAdmin(admin.ModelAdmin):
    pass
