from rest_framework import serializers

from histories.models import RainfallHistory


class RainfallHistorySerializer(serializers.ModelSerializer):

    class Meta:
        model = RainfallHistory
        fields = "__all__"
