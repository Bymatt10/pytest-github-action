from django.contrib import admin

from histories.resources import RainfallHistoryResource
from histories.models import RainfallHistory

from import_export.admin import ImportExportModelAdmin


class RainfallHistoryAdmin(ImportExportModelAdmin):
    resource_class = RainfallHistoryResource


admin.site.register(RainfallHistory, RainfallHistoryAdmin)
