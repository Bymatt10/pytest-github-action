from import_export import resources

from histories.models import RainfallHistory


class RainfallHistoryResource(resources.ModelResource):
    class Meta:
        model = RainfallHistory
        exclude = ("created", "modified")
