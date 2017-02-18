from django.contrib import admin

# Register your models here.
from wifinder.pois.models import Poi, Status, AvailableField, DisplayRole


@admin.register(Poi)
class PoiAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'city')
    list_editable = ('status',)
    list_filter = ('status', 'type')
    search_fields = ('name', 'city__alternate_names')
    fieldsets = (
        ('Basic Info', {
            'fields': ('status', 'name',
                       ),
            'classes': ('wide', 'extrapretty'),
        }),
        ('Location', {'fields': ('city',
                                 'type', 'desc', 'location', 'address'), }),
        ('Advanced options', {
            'classes': ('collapse',),
            'fields': ('rush_hours', 'floor', 'area', 'staff_count', 'avg_move_in_floor', 'days', 'fiber',
                       'wifi', ('irancell', 'rightel', 'mci'), 'das_in_ibs', 'adsl', 'power', 'ac_type',
                       'activity_duration', 'activity'),
        }),
    )


@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    # fields = ('name', 'name_persian','color')
    list_display = ('name', 'name_persian', 'display_color')


@admin.register(AvailableField)
class AvailableFieldAdmin(admin.ModelAdmin):
    list_display = ('name','title')
    list_editable = ('title',)


@admin.register(DisplayRole)
class DisplayRoleAdmin(admin.ModelAdmin):
    pass
