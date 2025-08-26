from django.contrib import admin

from stations.resources import StationResource
from stations.models import EquipmentStation, RainfallStation, Station

from import_export.admin import ImportExportModelAdmin


class StationAdmin(ImportExportModelAdmin):
    resource_class = StationResource


admin.site.register(Station, StationAdmin)
admin.site.register(EquipmentStation)
admin.site.register(RainfallStation)
