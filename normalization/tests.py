from rest_framework.test import APITestCase
from unittest.mock import Mock, patch
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
import json
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

class TestCaseBase(APITestCase):
    @property
    def bearer_token(self):
        # assuming there is a user in User model
        user = User.objects.create_user(
            username='iamuser',
            email='test@user.me',
            password='12345678'
        )

        refresh = RefreshToken.for_user(user)
        return {"HTTP_AUTHORIZATION": f'Bearer {refresh.access_token}'}
    

class DeviationTestClass(TestCaseBase):
    url = reverse('normalization')

    def test_normalization_no_auth(self):
            response = self.client.post(
                self.url,
                data={
                    "sensor_1": [5.44, 3.22, 6.55, 8.54, 1.24],
                    "sensor_2": [5444.44, 33.22, 622.55, 812.54, 123.24],
                    "sensor_3": [0.44, 0.22, 0.55, 0.54, 0.24]
                },
                content_type='application/json'
            )
            self.assertEqual(
                response.status_code, status.HTTP_401_UNAUTHORIZED, response.data
            )

    def test_normalization(self):
        # Mock validation
        with patch('normalization.standardizer.request_validation') as mock_validation:
            mock_validation.side_effect = [True]
            # Mock calculations
            with patch('normalization.standardizer.standard_deviation') as mock_standard_deviation:
                mock_standard_deviation.side_effect = [{
                    'success': True,
                    'result': {
                        'sensor1': [0.17354382198293136],
                        'sensor2': [0.17354382198293136]
                        }}]
                # Making request
                response = self.client.post(
                    self.url,
                    data=json.dumps('some data'),
                    content_type='application/json',
                    **self.bearer_token
                )
                self.assertEqual(response.status_code, status.HTTP_200_OK)
                result = {
                    "sensor1": [0.17354382198293136]
                }
                self.assertEqual(
                    result['sensor1'],
                    list(response.data['result']['sensor1'])
                )

    def test_400_BED_REQUEST(self):
        with patch('normalization.standardizer.request_validation') as mock_validation:
            mock_validation.side_effect = [False]
            response = self.client.post(
                self.url,
                data=json.dumps('some data'),
                content_type='application/json',
                **self.bearer_token
            )
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
