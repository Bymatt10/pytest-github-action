from rest_framework import serializers

from organizations.serializers import OrganizationSerializer
from stations.models import EquipmentStation, RainfallStation, Station


class StationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Station
        fields = "__all__"


class StationReadSerializer(serializers.ModelSerializer):
    organization = OrganizationSerializer(read_only=True)

    class Meta:
        model = Station
        fields = "__all__"


class EquipmentStationSerializer(serializers.ModelSerializer):

    class Meta:
        model = EquipmentStation
        fields = "__all__"


class RainfallStationSerializer(serializers.ModelSerializer):

    class Meta:
        model = RainfallStation
        fields = "__all__"


class RainfallStationReadSerializer(serializers.ModelSerializer):
    station = StationSerializer(read_only=True)

    class Meta:
        model = RainfallStation
        fields = "__all__"
