from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend

from stations.models import Station, EquipmentStation, RainfallStation
from stations.serializers import (
    StationSerializer,
    EquipmentStationSerializer,
    RainfallStationSerializer,
)


class StationViewSet(viewsets.ModelViewSet):
    queryset = Station.objects.all()
    serializer_class = StationSerializer

    filter_backends = [
        DjangoFilterBackend,
        filters.OrderingFilter,
        filters.SearchFilter,
    ]
    search_fields = ["name", "code"]
    filterset_fields = ["organization"]
    ordering_fields = ["id", "name", "created"]

    def paginate_queryset(self, queryset):
        if "paginator" in self.request.query_params:
            return None
        return super().paginate_queryset(queryset)


class EquipmentStationViewSet(viewsets.ModelViewSet):
    queryset = EquipmentStation.objects.all()
    serializer_class = EquipmentStationSerializer

    filter_backends = [
        DjangoFilterBackend,
        filters.OrderingFilter,
        filters.SearchFilter,
    ]
    search_fields = ["name", "code", "brand", "model"]
    filterset_fields = ["station"]
    ordering_fields = ["id", "name", "created"]

    def paginate_queryset(self, queryset):
        if "paginator" in self.request.query_params:
            return None
        return super().paginate_queryset(queryset)


class RainfallStationViewSet(viewsets.ModelViewSet):
    queryset = RainfallStation.objects.all()
    serializer_class = RainfallStationSerializer

    filter_backends = [
        DjangoFilterBackend,
        filters.OrderingFilter,
        filters.SearchFilter,
    ]
    filterset_fields = ["station", "month", "year"]
    ordering_fields = ["id", "registration_date", "created"]

    def paginate_queryset(self, queryset):
        if "paginator" in self.request.query_params:
            return None
        return super().paginate_queryset(queryset)
