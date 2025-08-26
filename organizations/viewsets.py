from rest_framework import viewsets, filters

from organizations.models import Organization
from organizations.serializers import OrganizationSerializer
from django_filters.rest_framework import (
    DjangoFilterBackend,
)


class OrganizationViewSet(viewsets.ModelViewSet):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer

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
