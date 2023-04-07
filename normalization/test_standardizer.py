from django.test import TestCase
from .standardizer import request_validation, standard_deviation


class ValidationTestCase(TestCase):

    def test_empty_data(self):
        data = {}
        self.assertTrue(request_validation(data))

    def test_wrong_values(self):
        data = {'sensor_1': {'a': 5}}
        self.assertFalse(request_validation(data))

    def test_different_lenght(self):
        data = {
            'sensor_1': [1, 2, 3],
            'sensor_2': [0, 2]
        }
        self.assertFalse(request_validation(data))


class StandardDeviationTestCase(TestCase):

    def test_correct_result(self):
        data = {
            "sensor_1": [5.44, 3.22, 6.55, 8.54, 1.24],
            "sensor_2": [5444.44, 33.22, 622.55, 812.54, 1233.24],
            "sensor_3": [0.44, 0.22, 0.55, 0.54, 0.24]
        }
        normalized_data = standard_deviation(data)
        self.assertEqual(normalized_data['success'], True)
        self.assertEqual(
            normalized_data['result']["sensor1"][3], 1.3907063743519035)
        self.assertEqual(
            normalized_data['result']["sensor2"][4], -0.20344219611829167)
        self.assertEqual(
            normalized_data['result']["sensor3"][2], 1.0658861555611072)

    def test_zero_vector(self):
        data = {
            "sensor_1": [5.44, 3.22, 6.55, 8.54, 1.24],
	        "sensor_2": [5444.44, 33.22, 622.55, 812.54, 1233.24],
            "sensor_3": [0, 0, 0, 0, 0]
        }
        normalized_data = standard_deviation(data)
        self.assertEqual(normalized_data['success'], True)
        self.assertEqual(
            normalized_data['result']["sensor1"][2], 0.6093665423473053)
        self.assertEqual(
            normalized_data['result']["sensor2"][3], -0.41959676783288097)
        self.assertEqual(
            normalized_data['result']["sensor3"][4], 0.0)

    def test_incorrect_values(self):
        data = 	{
            "sensor_1": ['asd', 3.22, 6.55, 8.54, 1.24],
            "sensor_2": [5444.44, 33.22, 622.55, 812.54, 1233.24],
            "sensor_3": [0.44, 0.22, 0.55, 0.54, 0.24]
        }
        normalized_data = standard_deviation(data)
        self.assertEqual(normalized_data['success'], False)
