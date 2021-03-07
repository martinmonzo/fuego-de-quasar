from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework.views import APIView

from quasar_fire_app.serializers.satellite import SatelliteSplitSerializer
from quasar_fire_app.server.set_distance_and_message import SetDistanceAndMessage
from quasar_fire_app.server.get_location_and_message import GetLocationAndMessage


class TopSecretSplitAPIView(APIView):
    """
    GET: Retrieve the location (X,Y) of the transmitter and the message sent by it.
    POST: Update the distance fromt the transmitter to the satellite.
    """
    post_serializer_class = SatelliteSplitSerializer

    def get(self, request, satellite_name):
        try:
            response = GetLocationAndMessage(request).response

            position = response['position']
            message = response['message']

            return Response(
                {
                    'position': {
                        'x': position['x'],
                        'y': position['y'],
                    },
                    'message': message,
                },
                status=status.HTTP_200_OK,
            )
        except APIException as ex:
            return Response(
                {'error': 'There is no enough information.'},
                status=status.HTTP_404_NOT_FOUND,
            )

    def post(self, request, satellite_name):
        serializer = self.post_serializer_class(data=request.data)

        if not serializer.is_valid():
            return Response(status=status.HTTP_404_NOT_FOUND)
        try:
            SetDistanceAndMessage(request, satellite_name=satellite_name)

            return Response(status=status.HTTP_200_OK)
        except APIException as ex:
            return Response(status=status.HTTP_404_NOT_FOUND)
