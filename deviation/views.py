from rest_framework import views
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .standardizer import request_validation, standard_deviation
from .serializers import StandardDeviationSerializer


class StandardDeviationView(views.APIView):
    serializer_class = StandardDeviationSerializer
    permission_classes = [IsAuthenticated, ]

    def post(self, request, *args, **kwargs):
        success = request_validation(request.data)
        if not success:
            response = Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            data = standard_deviation(request.data)
            data = {
                'success': data['success'],
                'result': data['result']
            }
            data = StandardDeviationSerializer(
                data,
                context=True).data
            response = Response(data, status=status.HTTP_200_OK)
        return response
