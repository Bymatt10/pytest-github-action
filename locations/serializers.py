from rest_framework import serializers

from locations.models import Location


class LocationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Location
        fields = "__all__"


class LocationReadSerializer(serializers.ModelSerializer):
    location_type_display = serializers.CharField(
        source="get_location_type_display", read_only=True
    )
    parent = LocationSerializer(read_only=True)

    class Meta:
        model = Location
        fields = "__all__"
