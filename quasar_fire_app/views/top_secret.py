from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework.views import APIView

from quasar_fire_app.serializers.top_secret_post import TopSecretPostSerializer
from quasar_fire_app.server.set_and_get_location_and_message_by_satellites import SetAndGetLocationAndMessageBySatellites


class TopSecretAPIView(APIView):
    """POST: Retrieve the location (X,Y) of the transmitter and the message sent by it."""

    serializer_class = TopSecretPostSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if not serializer.is_valid():
            return Response(status=status.HTTP_404_NOT_FOUND)
        try:
            response = SetAndGetLocationAndMessageBySatellites(request).response
            
            return Response(
                response,
                status=status.HTTP_200_OK,
            )
        except APIException as ex:
            return Response(status=status.HTTP_404_NOT_FOUND)
