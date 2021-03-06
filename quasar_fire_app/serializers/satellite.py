from django.core.validators import MinValueValidator

from rest_framework import serializers


class SatelliteSerializer(serializers.Serializer):
    name = serializers.CharField(required=True)
    distance = serializers.FloatField(
        required=True,
        allow_null=False,
        validators=[MinValueValidator(0.0)],
    )
    message = serializers.ListField(required=True, allow_null=False)

