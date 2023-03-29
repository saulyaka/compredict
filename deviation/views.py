from rest_framework import views
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
import numpy as np
import itertools, re
from numpy.core._exceptions import UFuncTypeError
from .serializers import StandardDeviationSerializer


class StandardDeviationView(views.APIView):
    serializer_class = StandardDeviationSerializer
    # permission_classes = [IsAuthenticated, ]

    def post(self, request, *args, **kwargs):
        success = self.request_validation(request.data)
        if not success:
            response = Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            data = self.standard_deviation()
            data = {
                'success': data['success'],
                'result': data['result']
            }
            data = StandardDeviationSerializer(
                data,
                context=True).data
            response = Response(data, status=status.HTTP_200_OK)
        return response

    def standard_deviation(self):
        inputs = {int(m.group(1)): v for k, v in self.request.data.items()
        if (m := re.match(r"sensor_(\d*)", k))}
        
        # create a dataset
        try:
            array = np.fromiter(
            itertools.chain.from_iterable(inputs.values()),
                dtype=float).reshape(len(self.request.data), -1)
        except ValueError:
            return {
            'success': False,
            'result': None
            }

        # calculate the mean and standard deviation for each column
        means = np.mean(array, axis=1, keepdims=True)
        stds = np.std(array, axis=1, keepdims=True)

        # subtract the mean from each column
        array -= means

        # standardize the dataset by subtracting the mean and dividing by the standard deviation
        array /= stds

        # prepare data for serializer
        result = {f"sensor{i}": v for i, v in zip(inputs, array)}
        return {
            'success': True,
            'result': result
        }

    def request_validation(self, data):
        """
        First level validation: Check if there is dictionary 
        and all dict lists are the same length > 0.
        """
        if not isinstance(data, dict):
            return False
        if data:
            length = len(next(iter(data.values())))
            if not all(len(v) == length for v in data.values()):
                return False
        return True
