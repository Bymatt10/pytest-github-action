from import_export import resources

from histories.models import Station


class StationResource(resources.ModelResource):
    class Meta:
        model = Station
        exclude = ("created", "modified")
