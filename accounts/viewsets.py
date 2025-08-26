from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from accounts.models import User
from accounts.serializers import AccountSerializer, AccountReadSerializer
from rest_framework.response import Response
from django_filters.rest_framework import (
    DjangoFilterBackend,
)


class AccountViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = AccountSerializer

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    search_fields = [
        "username",
        "first_name",
        "last_name",
    ]
    filterset_fields = ["is_active", "is_staff", "is_superuser", "role", "coach"]
    ordering_fields = ["id"]

    def paginate_queryset(self, queryset):
        if "paginator" in self.request.query_params:
            return None
        return super().paginate_queryset(
            queryset,
        )

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return AccountSerializer

        return AccountReadSerializer

    @action(detail=False)
    def me(self, request):
        serializer = AccountReadSerializer(request.user, context={"request": request})
        return Response(status=status.HTTP_200_OK, data=serializer.data)
