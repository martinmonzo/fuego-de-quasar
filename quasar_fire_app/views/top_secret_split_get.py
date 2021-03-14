from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework.views import APIView

from quasar_fire_app.serializers.satellite import SatelliteSplitSerializer
from quasar_fire_app.server.get_location_and_message import GetLocationAndMessage


class TopSecretSplitGetAPIView(APIView):
    """GET: Retrieve the location (X,Y) of the transmitter and the message sent by it."""
    
    serializer_class = SatelliteSplitSerializer

    def get(self, request):
        try:
            response = GetLocationAndMessage(request).response

            return Response(
                response,
                status=status.HTTP_200_OK,
            )
        except APIException as ex:
            return Response(
                {'error': 'There is no enough information.'},
                status=status.HTTP_404_NOT_FOUND,
            )
