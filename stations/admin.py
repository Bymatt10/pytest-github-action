from django.contrib import admin
from unfold.admin import ModelAdmin

from stations.resources import RainfallStationResource, StationResource
from stations.models import EquipmentStation, RainfallStation, Station

from import_export.admin import ImportExportModelAdmin
from unfold.contrib.import_export.forms import ExportForm, ImportForm

from unfold.admin import TabularInline


class EquipmentStationInline(TabularInline):
    extra = 0
    model = EquipmentStation
    hide_title = True


class StationAdmin(ModelAdmin, ImportExportModelAdmin):
    list_display = ("name", "code", "organization", "created")
    ordering = ["-id"]
    search_fields = ("name",)
    list_filter = ("organization",)
    resource_class = StationResource
    inlines = (EquipmentStationInline,)

    compressed_fields = True
    import_form_class = ImportForm
    export_form_class = ExportForm


class RainfallStationAdmin(ModelAdmin, ImportExportModelAdmin):
    list_display = ("station", "registration_date", "value", "created")
    ordering = ["-id"]
    resource_class = RainfallStationResource

    compressed_fields = True
    import_form_class = ImportForm
    export_form_class = ExportForm

admin.site.register(Station, StationAdmin)
admin.site.register(RainfallStation, RainfallStationAdmin)
