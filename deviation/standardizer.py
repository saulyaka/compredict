import itertools
import re
import numpy as np
from django.core.exceptions import ValidationError
from sklearn.preprocessing import StandardScaler

def standard_deviation(data):
    inputs = {int(m.group(1)): v for k, v in data.items()
    if (m := re.match(r"sensor_(\d*)", k))}
    # create a numpy array from the data
    try:
         array = np.fromiter(
            itertools.chain.from_iterable(inputs.values()),
            dtype=float).reshape(len(data), -1)
    except ValueError as err:
        return {
            'success': False,
            'result': {'error': str(err)}
            }

    array = StandardScaler().fit_transform(array.transpose()).transpose()

    # prepare data for serializer
    result = {f"sensor{i}": v for i, v in zip(inputs, array)}
    return {
        'success': True,
        'result': result
    }


def request_validation(data):
    """
    Each value is a list.
    All lists are the same length.
    """
    if data:
        # Check if value is a list
        try:
            if not isinstance(next(iter(data.values())), list):
                return False
        except AttributeError:
            return False
        # Check if all lists have the same lenght
        length = len(next(iter(data.values())))
        if not all(len(v) == length for v in data.values()):
            return False
    return True
