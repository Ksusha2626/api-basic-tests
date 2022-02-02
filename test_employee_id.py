import random

import allure
import pytest
import requests
from bs4 import BeautifulSoup
from hamcrest import assert_that, empty, has_entries, instance_of, is_not

DUMMY_URL = "http://dummy.restapiexample.com"
PREFIX = "/api"
VERSION = "/v1"
DEFAULT_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/97.0.4692.71 Safari/537.36"
}


@pytest.mark.dummy
class TestApiEmployee:

    @allure.step("[GET] /employee/id")
    def test_get_random_employee(self):
        """GET /employee/id with random existing, valid id"""
        employee_id = random.randint(1, 20)
        response = requests.get(
            DUMMY_URL + PREFIX + VERSION + f"/employee/{employee_id}",
            headers=DEFAULT_HEADERS)

        assert response.status_code == 200, response.text
        assert_that(response.json(), has_entries(**{
            "status": 'success',
            "data": has_entries(**{
                'id': is_not(empty()),
                'employee_name': is_not(empty()),
                'employee_salary': is_not(empty()),
                'employee_age': is_not(empty()),
                'profile_image': instance_of(str)
            }),
            "message": 'Successfully! Record has been fetched.'
        }))
        assert response.elapsed.total_seconds() < 4
        # There should be DB info check

    @allure.step("[GET] /employee/id")
    def test_incorrect_http_method(self):
        """Test /employee/id with incorrect http method"""
        response = requests.post(
            DUMMY_URL + PREFIX + VERSION + "/employee/1",
            headers=DEFAULT_HEADERS)
        title = BeautifulSoup(response.text, 'html.parser').find('title').getText()

        assert response.status_code == 405
        assert title == 'An Error Occurred: Method Not Allowed'

    @allure.step("[GET] /employee/id")
    def test_get_non_existent_employee(self):
        """GET /employee/{id} non-existent employee"""
        response = requests.get(
            DUMMY_URL + PREFIX + VERSION + "/employee/0",
            headers=DEFAULT_HEADERS)

        assert response.status_code == 400, response.text
        assert_that(response.json(), has_entries(**{
            "status": 'error',
            "message": "Not found record",
            "code": 400,
            "errors": "id is empty"
        }))

    @pytest.mark.xfail(reason='No validation. Returns a successful result.')
    @pytest.mark.parametrize('data', [
        '-1',
        'abc',
        '$',
    ])
    @allure.step("[GET] /employee/id")
    def test_get_invalid_id(self, data):
        """GET /employee/{id} with invalid id"""
        response = requests.get(
            DUMMY_URL + PREFIX + VERSION + f"/employee/{data}",
            headers=DEFAULT_HEADERS)

        assert response.status_code == 400, response.text
        assert_that(response.json(), has_entries(**{
            "message": "Bad Request",
            "code": 400,
        }))

    @pytest.mark.xfail(reason='X-Ratelimit-Limit set 1 minute')
    @allure.step("[GET] /employee/id")
    def test_multiple_request(self):
        """GET /employee/{id} multiple request in a row"""
        for i in range(5):
            employee_id = random.randint(1, 20)
            response = requests.get(
                DUMMY_URL + PREFIX + VERSION + f"/employee/{employee_id}",
                headers=DEFAULT_HEADERS)

            assert response.status_code == 200, "Request went bad"
