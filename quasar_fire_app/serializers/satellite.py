from django.core.validators import MinValueValidator

from rest_framework import serializers


class SatelliteSplitSerializer(serializers.Serializer):
    distance = serializers.FloatField(
        required=True,
        allow_null=False,
        validators=[MinValueValidator(0.0)],
    )
    message = serializers.ListField(required=True, allow_null=False)


class SatelliteSerializer(SatelliteSplitSerializer):
    name = serializers.CharField(required=True)
