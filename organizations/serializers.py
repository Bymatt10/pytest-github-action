from rest_framework import serializers

from locations.serializers import LocationSerializer
from organizations.models import Organization


class OrganizationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Organization
        fields = "__all__"


class OrganizationReadSerializer(serializers.ModelSerializer):
    location = LocationSerializer(read_only=True)

    class Meta:
        model = Organization
        fields = "__all__"
