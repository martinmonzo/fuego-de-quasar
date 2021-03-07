from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework.views import APIView

from quasar_fire_app.serializers.satellite import SatelliteSplitSerializer
from quasar_fire_app.server.set_distance_and_message import SetDistanceAndMessageAction


class TopSecretSplitAPIView(APIView):
    """
    GET: Retrieve the location (X, Y) of the transmitter and the message sent by it.
    POST: Update the distance fromt the transmitter to the satellite.
    """

    post_serializer_class = SatelliteSplitSerializer

    def get(self, request, satellite_name):
        pass

    def post(self, request, satellite_name):
        serializer = self.post_serializer_class(data=request.data)

        if not serializer.is_valid():
            return Response(status=status.HTTP_404_NOT_FOUND)
        try:
            SetDistanceAndMessageAction(request, satellite_name=satellite_name)

            return Response(status=status.HTTP_200_OK)
        except APIException as ex:
            return Response(status=status.HTTP_404_NOT_FOUND)
