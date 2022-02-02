import random
import string

import pytest


def random_string(length=8):
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in
                   range(length))


def random_digits(length=8):
    return ''.join(random.choice(string.digits) for _ in range(length))


@pytest.fixture(scope="module")
def data():
    return {
        "name": random_string().title(),
        "surname": random_string().title(),
        "phone": random_digits(length=11)
    }
