from rest_framework import viewsets, filters

from locations.models import Location
from locations.serializers import LocationSerializer, LocationReadSerializer
from django_filters.rest_framework import (
    DjangoFilterBackend,
)


class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer

    filter_backends = [
        DjangoFilterBackend,
        filters.OrderingFilter,
        filters.SearchFilter,
    ]
    search_fields = [
        "name",
    ]
    filterset_fields = [
        "location",
    ]
    ordering_fields = ["id"]

    def paginate_queryset(self, queryset):
        if "paginator" in self.request.query_params:
            return None
        return super().paginate_queryset(
            queryset,
        )

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return LocationSerializer

        return LocationReadSerializer
