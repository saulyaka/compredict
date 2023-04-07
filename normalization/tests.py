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
    url = reverse('normalization')

    def test_standard_deviation_no_auth(self):
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

    def test_standard_deviation(self):
        response = self.client.post(
            self.url,
            data=json.dumps({
                "sensor_1": [5.44, 3.22, 6.55, 8.54, 1.24],
                "sensor_2": [5444.44, 33.22, 622.55, 812.54, 1233.24],
                "sensor_3": [0.44, 0.22, 0.55, 0.54, 0.24]
            }),
            content_type='application/json',
            **self.bearer_token
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        result = {
            "sensor1": [
                0.17354382198293136,
                -0.6981016187458169,
                0.6093665423473053,
                1.3907063743519035,
                -1.475515119936322
            ],
            "sensor2": [
                1.9602614701628547,
                -0.8200093678533557,
                -0.5172131383583263,
                -0.41959676783288097,
                -0.20344219611829167
            ],
            "sensor3": [
                0.29452117456293736,
                -1.248208787433402,
                1.0658861555611072,
                0.9957620663794554,
                -1.1079606090700984
            ]
        }
        self.assertEqual(
            result['sensor1'],
            list(response.data['result']['sensor1'])
        )
        self.assertEqual(
            result['sensor2'],
            list(response.data['result']['sensor2'])
            )
        self.assertEqual(
            result['sensor3'],
            list(response.data['result']['sensor3'])
            )

    def test_wrong_vector_lenght(self):
        response = self.client.post(
            self.url,
            data=json.dumps({
                "sensor_1": [3.22, 6.55, 8.54, 1.24],
                "sensor_2": [5444.44, 33.22, 622.55, 812.54, 1233.24],
                "sensor_3": [0.44, 0.22, 0.55, 0.54, 0.24]
            }),
            content_type='application/json',
            **self.bearer_token
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_bad_request(self):
        response = self.client.post(
            self.url,
            data=json.dumps([2, 4, 1, 6]),
            content_type='application/json',
            **self.bearer_token
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UnsaccessTestCase(TestCaseBase):
    url = reverse('normalization')

    def test_empty_request(self):
        response = self.client.post(
            self.url,
            data={},
            content_type='application/json',
            **self.bearer_token
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['success'], False)

    def test_zero_vector(self):
        response = self.client.post(
            self.url,
            data=json.dumps({
                "sensor_1": [5.44, 3.22, 6.55, 8.54, 1.24],
                "sensor_2": [0, 0, 0, 0, 0],
                "sensor_3": [0.44, 0.22, 0.55, 0.54, 0.24]
            }),
            content_type='application/json',
            **self.bearer_token
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data['success'], True)
