from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework.views import APIView

from quasar_fire_app.serializers.satellite import SatelliteSplitSerializer
from quasar_fire_app.server.set_distance_and_message import SetDistanceAndMessage


class TopSecretSplitPostAPIView(APIView):
    """
    POST: Update the distance from the transmitter to a
    satellite and the message received by it.
    """
    
    serializer_class = SatelliteSplitSerializer

    def post(self, request, satellite_name):
        serializer = self.serializer_class(data=request.data)

        if not serializer.is_valid():
            return Response(status=status.HTTP_404_NOT_FOUND)
        try:
            SetDistanceAndMessage(request, satellite_name=satellite_name)

            return Response(status=status.HTTP_200_OK)
        except APIException as ex:
            return Response(status=status.HTTP_404_NOT_FOUND)
