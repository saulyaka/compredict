from rest_framework.test import APITestCase
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
    url = reverse('standard_deviation')

    def test_standard_deviation_no_auth(self):
        response = self.client.post(
            self.url,
            data={
                "sensor1": [5.44, 3.22, 6.55, 8.54, 1.24],
                "sensor_2": [5444.44, 33.22, 622.55, 812.54, 123.24],
                "sensor3": [0.44, 0.22, 0.55, 0.54, 0.24]
            },
            content_type='application/json'
        )
        self.assertEqual(
            response.status_code, status.HTTP_401_UNAUTHORIZED, response.data
        )

    def test_standard_deviation(self):
        response = self.client.post(
            self.url,
            data=json.dumps({
                "sensor1": [5.44, 3.22, 6.55, 8.54, 1.24],
                "sensor_2": [5444.44, 33.22, 622.55, 812.54, 123.24],
                "sensor3": [0.44, 0.22, 0.55, 0.54, 0.24]
            }),
            content_type='application/json',
            **self.bearer_token
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_bad_request(self):
        response = self.client.post(
            self.url,
            data={},
            content_type='application/json',
            **self.bearer_token
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response = self.client.post(
            self.url,
            data=json.dumps({
                "sensor1": [5.44, 3.22, 6.55, 1.24],
                "sensor_2": [5444.44, 33.22, 622.55, 812.54, 123.24],
                "sensor3": [0.44, 0.22, 0.55, 0.54, 0.24]
            }),
            content_type='application/json',
            **self.bearer_token
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UnsaccessTestCase(TestCaseBase):
    url = reverse('standard_deviation')

    def test_unsaccess_request(self):
        response = self.client.post(
            self.url,
            data={},
            content_type='application/json',
            **self.bearer_token
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response = self.client.post(
            self.url,
            data=json.dumps({
                "sensor1": [5.44, 3.22, 6.55, 8.54, 1.24],
                "sensor_2": [0, 0, 0, 0],
                "sensor3": [0.44, 0.22, 0.55, 0.54, 0.24]
            }),
            content_type='application/json',
            **self.bearer_token
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data['success'], False)
