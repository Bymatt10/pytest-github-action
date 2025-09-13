from import_export import resources

from histories.models import Station
from stations.models import RainfallStation


class StationResource(resources.ModelResource):
    class Meta:
        model = Station
        exclude = ("created", "modified")

class RainfallStationResource(resources.ModelResource):
    class Meta:
        model = RainfallStation
        exclude = ("day", "month", "year", "created", "modified")