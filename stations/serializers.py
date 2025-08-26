from rest_framework import serializers

from stations.models import EquipmentStation, RainfallStation, Station


class StationSerializer(serializers.ModelSerializer):

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
