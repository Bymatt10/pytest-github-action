from rest_framework import viewsets, filters

from stations.models import EquipmentStation, RainfallStation, Station
from stations.serializers import (
    EquipmentStationSerializer,
    RainfallStationSerializer,
    StationSerializer,
)

from django_filters.rest_framework import (
    DjangoFilterBackend,
)


class StationViewSet(viewsets.ModelViewSet):
    queryset = Station.objects.all()
    serializer_class = StationSerializer

    filter_backends = [
        DjangoFilterBackend,
        filters.OrderingFilter,
        filters.SearchFilter,
    ]
    search_fields = [
        "name",
    ]
    filterset_fields = [
        "organization",
    ]
    ordering_fields = ["id"]

    def paginate_queryset(self, queryset):
        if "paginator" in self.request.query_params:
            return None
        return super().paginate_queryset(
            queryset,
        )


class EquipmentStationViewSet(viewsets.ModelViewSet):
    queryset = EquipmentStation.objects.all()
    serializer_class = EquipmentStationSerializer

    filter_backends = [
        DjangoFilterBackend,
        filters.OrderingFilter,
        filters.SearchFilter,
    ]
    search_fields = [
        "name",
    ]
    filterset_fields = [
        "stattion",
    ]
    ordering_fields = ["id"]

    def paginate_queryset(self, queryset):
        if "paginator" in self.request.query_params:
            return None
        return super().paginate_queryset(
            queryset,
        )


class RainfallStationViewSet(viewsets.ModelViewSet):
    queryset = RainfallStation.objects.all()
    serializer_class = RainfallStationSerializer

    filter_backends = [
        DjangoFilterBackend,
        filters.OrderingFilter,
        filters.SearchFilter,
    ]
    # search_fields = [
    #     "name",
    # ]
    filterset_fields = ["station", "day", "month", "year"]
    ordering_fields = ["id"]

    def paginate_queryset(self, queryset):
        if "paginator" in self.request.query_params:
            return None
        return super().paginate_queryset(
            queryset,
        )
