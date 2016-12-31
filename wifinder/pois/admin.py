from django.contrib import admin

# Register your models here.
from wifinder.pois.models import Poi


@admin.register(Poi)
class PoiAdmin(admin.ModelAdmin):
    list_display = ('name', 'status')
    fieldsets = (
        ('Basic Info', {
            'fields': ('status', 'name',
                       ),
            'classes': ('wide', 'extrapretty'),
        }),
        ('Location', {'fields': (('country', 'region', 'city'),

                                'type', 'desc', 'location', 'address'), }),
        ('Advanced options', {
            'classes': ('collapse',),
            'fields': ('rush_hours', 'floor', 'area', 'staff_count', 'avg_move_in_floor', 'days', 'fiber',
                       'wifi', ('irancell', 'rightel', 'mci'), 'das_in_ibs', 'adsl', 'power', 'ac_type',
                       'activity_duration', 'activity'),
        }),
    )
