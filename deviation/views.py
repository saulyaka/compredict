from rest_framework import views
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
import numpy as np
from numpy.core._exceptions import UFuncTypeError
from .serializers import StandardDeviationSerializer

class StandardDeviationView(views.APIView):
    serializer_class = StandardDeviationSerializer
    permission_classes = [IsAuthenticated, ]

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
        result = {}
        i = 1
        unsuccess = {
            'success': False,
            'result': None
        }
        # create a dataset
        my_array = np.empty((0, self.length))
        for key in self.request.data:
            new_row = np.array(self.request.data[key])
            if sum(new_row) == 0:
                return unsuccess
            my_array = np.append(my_array, [new_row], axis=0)

        # calculate the mean and standard deviation for each column
        try:
            means = np.mean(my_array, axis=1)
        except UFuncTypeError:
            return unsuccess
        stds = np.std(my_array, axis=1)

        # subtract the mean from each column
        my_array -= means.reshape(-1, 1)

        # standardize the dataset by subtracting the mean and dividing by the standard deviation
        my_array /= stds.reshape(-1, 1)

        # prepare data for serializer
        for row in my_array:
            result[f'sensor{i}'] = list(row)
            i += 1
        print(result)
        return {
            'success': True,
            'result': result
        }

    def request_validation(self, data):
        """
        First level validation: Check if there is dictionary 
        and all dict lists are the same length > 0.
        """
        # Lookin for the lenght
        if len(data) > 0:
            for key in data:
                self.length = len(data[key])
                break
        else:
            return False

        # Checking other lenght
        for key in data:
            if len(data[key]) != self.length:
                return False

        # Exlude empty list
        return self.length > 0
