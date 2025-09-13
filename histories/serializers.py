from rest_framework import serializers

from histories.models import RainfallHistory
from stations.serializers import StationReadSerializer


class RainfallHistorySerializer(serializers.ModelSerializer):

    class Meta:
        model = RainfallHistory
        fields = "__all__"


class RainfallHistoryReadSerializer(serializers.ModelSerializer):
    station = StationReadSerializer(read_only=True)

    class Meta:
        model = RainfallHistory
        fields = "__all__"
