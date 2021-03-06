from rest_framework import serializers

from quasar_fire_app.serializers.satellite import SatelliteSerializer


class TopSecretPostSerializer(serializers.Serializer):
    satellites = serializers.ListField(
        child=SatelliteSerializer(),
        allow_empty=False,
        min_length=3,
        max_length=3,
    )
