from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.views import APIView

from quasar_fire_app.domain.get_message import get_message
from quasar_fire_app.domain.get_location import get_location


class SatelliteSerializer(serializers.Serializer):
    name = serializers.CharField()
    distance = serializers.FloatField(min_value=0)
    message = serializers.ListField(
        child=serializers.CharField(),
        allow_empty=False,
        min_length=1,
    )


class HelloSerializer(serializers.Serializer):
    satellites = serializers.ListField(
        child=SatelliteSerializer(),
        allow_empty=False,
        min_length=3,
        max_length=3,
    )


class HelloApiView(APIView):
    """Test API View"""

    # serializer_class = HelloSerializer

    def get(self, request, format=None):
        """
        
        """

        import pdb;pdb.set_trace()
        location = get_location([50, 30, 5])
        # serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            name = serializer.validated_data.get('name')
            message = f'Hello {name}!'
            return Response({'message': message})
        else:
            return Response(
                serializer.errors,
                status=400
            )




        l1 = ["", "como", "", "pepe?"]
        l2 = ["", "", "estas", ""]
        l3 = ["hola", "", "", ""]
        messages = [l1,l2,l3]

        mensaje = get_message(messages)
        
        an_apiview = [
            'Uses HTTP method as function (get, post)',
            'Is similar to a traditional Django View',
            'Gives you the most control over your application logic',
            'Is mapped manually to URLs',
        ]

        return Response({'message': mensaje, 'an_apiview': an_apiview})

    def post(self, request):
        """
        
        """
        post_params = [
            (
                'event_id',
                fields.CharField(
                    required=False,
                    help_text='Facebook event ID to link the EB event to.',
                ),
            ),
            (
                'ticket_url',
                fields.CharField(
                    required=True,
                    help_text='Eventbrite URL to an event listing page.',
                    error_messages={'required': 'missing_info_to_process ticket_url'},
                ),
            ),
        ]
        import pdb;pdb.set_trace()
        return Response({'message': 'Hello!', 'method': 'THIS IS A POST'})