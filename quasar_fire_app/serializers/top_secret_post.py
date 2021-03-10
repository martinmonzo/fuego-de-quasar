from rest_framework import serializers

from quasar_fire_app.serializers.satellite import SatelliteSplitSerializer


class TopSecretPostSerializer(serializers.Serializer):
    satellites = serializers.ListField(
        child=SatelliteSplitSerializer(),
        allow_empty=False,
        min_length=3,
        max_length=3,
    )
