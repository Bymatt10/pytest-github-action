from rest_framework import viewsets, filters
from django_filters.rest_framework import (
    DjangoFilterBackend,
)

from histories.models import RainfallHistory
from histories.serializers import RainfallHistorySerializer, RainfallHistoryReadSerializer


class RainfallHistoryViewSet(viewsets.ModelViewSet):
    queryset = RainfallHistory.objects.all()
    serializer_class = RainfallHistorySerializer

    filter_backends = [
        DjangoFilterBackend,
        filters.OrderingFilter,
        filters.SearchFilter,
    ]
    # search_fields = [
    #     "name",
    # ]
    filterset_fields = ["station", "month"]
    ordering_fields = ["id"]

    def paginate_queryset(self, queryset):
        if "paginator" in self.request.query_params:
            return None
        return super().paginate_queryset(
            queryset,
        )

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return RainfallHistorySerializer
        return RainfallHistoryReadSerializer
