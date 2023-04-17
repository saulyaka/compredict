from rest_framework import views
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

import normalization.standardizer as standardizer
from .serializers import StandardizationSerializer

from drf_spectacular.utils import extend_schema, OpenApiExample

@extend_schema(
    examples=[OpenApiExample(
        value=[
            {
                "sensor_1": [5.44, 3.22, 6.55, 8.54, 1.24],
                "sensor_2": [0, 0, 0, 0, 0],
                "sensor_3": [0.44, 0.22, 0.55, 0.54, 0.24]
            }
        ], name='request'
    ),
    OpenApiExample(
        value=[
          {
                "success": True,
                "result": {
                    "sensor1": [
                    0.17354382198293136,
                    -0.6981016187458169,
                    0.6093665423473053,
                    1.3907063743519035,
                    -1.475515119936322
                    ],
                    "sensor2": [
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0
                    ],
                    "sensor3": [
                    0.29452117456293736,
                    -1.248208787433402,
                    1.0658861555611072,
                    0.9957620663794554,
                    -1.1079606090700984
                    ]
                }
                }
        ], name='response'
    )],
    responses={
       200:{
                "success": True,
                "result": {
                    "sensor1": [
                    0.17354382198293136,
                    -0.6981016187458169,
                    0.6093665423473053,
                    1.3907063743519035,
                    -1.475515119936322
                    ],
                    "sensor2": [
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0
                    ],
                    "sensor3": [
                    0.29452117456293736,
                    -1.248208787433402,
                    1.0658861555611072,
                    0.9957620663794554,
                    -1.1079606090700984
                    ]
                }
                }
    }
)
class StandardDeviationView(views.APIView):
    serializer_class = StandardizationSerializer
    permission_classes = [IsAuthenticated, ]

    def post(self, request, *args, **kwargs):
        success = standardizer.request_validation(request.data)
        if not success:
            response = Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            data = standardizer.standard_deviation(request.data)
            data = {
                'success': data['success'],
                'result': data['result']
            }
            data = StandardizationSerializer(
                data,
                context=True).data
            response = Response(data, status=status.HTTP_200_OK)
        return response
