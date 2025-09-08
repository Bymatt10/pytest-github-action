from django.contrib import admin

from histories.resources import RainfallHistoryResource
from histories.models import RainfallHistory

from import_export.admin import ImportExportModelAdmin
from unfold.admin import ModelAdmin
from unfold.contrib.import_export.forms import ExportForm, ImportForm


class RainfallHistoryAdmin(ModelAdmin, ImportExportModelAdmin):
    list_display = ("station", "month", "value", "created")
    ordering = ["-id"]
    search_fields = ("station__name",)
    list_filter = ("station",)
    list_per_page = 12

    resource_class = RainfallHistoryResource

    compressed_fields = True
    import_form_class = ImportForm
    export_form_class = ExportForm


admin.site.register(RainfallHistory, RainfallHistoryAdmin)
