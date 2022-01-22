import random
import string

import allure
import pytest
import requests
from bs4 import BeautifulSoup
from hamcrest import assert_that, empty, has_entries, is_not

DUMMY_URL = "http://dummy.restapiexample.com"
PREFIX = "/api"
VERSION = "/v1"
DEFAULT_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/97.0.4692.71 Safari/537.36"
}


def random_string(length=8):
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in
                   range(length))


def random_digits(length=8):
    return ''.join(random.choice(string.digits) for _ in range(length))


def allure_repr(response):
    allure.attach(
        repr(response.request.body),
        name=f"{response.request.method} {response.request.url} request body",
        attachment_type=allure.attachment_type.JSON,
    )
    allure.attach(
        repr(response.headers),
        name=f"{response.request.method} {response.url} raw response headers",
        attachment_type=allure.attachment_type.JSON,
    )
    allure.attach(
        repr(response.text),
        name=f"{response.request.method} {response.url} raw response body",
        attachment_type=allure.attachment_type.JSON,
    )


@pytest.mark.dummy
class TestApiEmployeeCreate:

    @allure.step("[POST] Get /create")
    def test_create_employee(self):
        """Create employee"""
        data = {
            "name": "Yury",
            "surname": "Pavlov",
            "phone": "375291117788"
        }
        response = requests.post(DUMMY_URL + PREFIX + VERSION + "/create",
                                 data=data,
                                 headers=DEFAULT_HEADERS)
        allure_repr(response)
        assert response.status_code == 200, response.text
        assert_that(response.json(), has_entries(**{
            "status": 'success',
            "data": has_entries(**{
                'id': is_not(empty()),
                'name': data['name'],
                'surname': data['surname'],
                'phone': data['phone']
            }),
            "message": 'Successfully! Record has been added.'
        }))
        # There should be DB info check

    @pytest.mark.xfail(reason='Returns a successful result with new user_id')
    @allure.step("[POST] Get /create")
    def test_double_create(self):
        """Double request with the added user"""
        data = {
            "name": "Yury",
            "surname": "Pavlov",
            "phone": "375291117788"
        }
        response = requests.post(DUMMY_URL + PREFIX + VERSION + "/create",
                                 data=data,
                                 headers=DEFAULT_HEADERS)
        allure_repr(response)
        assert response.status_code == 400, response.text
        assert_that(response.json(), has_entries(**{
            "message": "User already added",
            "code": 400,
        }))
        # There should be check, that user hasn't been added to the DB again

    @pytest.mark.xfail(reason='Returns a successful result with new user_id')
    @allure.step("[POST] Get /create")
    def test_create_employee_without_body_request(self):
        """Create employee without body request"""
        response = requests.post(DUMMY_URL + PREFIX + VERSION + "/create",
                                 headers=DEFAULT_HEADERS)

        assert response.status_code == 400, response.text
        assert_that(response.json(), has_entries(**{
            "message": "Missing required parameters!",
            "code": 400,
        }))

    @allure.step("[POST] Get /create")
    def test_multiple_request(self):
        """/create multiple request in a row"""
        data = {
            "name": random_string().title(),
            "surname": random_string().title(),
            "phone": random_digits(length=11)
        }
        i = 0
        while i <= 3:
            i += 1
            requests.post(DUMMY_URL + PREFIX + VERSION + "/create",
                          data=data,
                          headers=DEFAULT_HEADERS)
        response = requests.post(DUMMY_URL + PREFIX + VERSION + "/create",
                                 data=data,
                                 headers=DEFAULT_HEADERS)
        allure_repr(response)
        assert response.status_code == 429
        title = BeautifulSoup(response.text, 'html.parser').find(
            'title').getText()
        assert title == 'Too Many Requests'

    @allure.step("[POST] Get /create")
    def test_incorrect_http_method(self):
        """Test /create with incorrect http method"""
        data = {
            "name": "Yury",
            "surname": "Pavlov",
            "phone": "375291117788"
        }
        response = requests.post(DUMMY_URL + PREFIX + VERSION + "/create",
                                 data=data,
                                 headers=DEFAULT_HEADERS)
        allure_repr(response)
        title = BeautifulSoup(response.text, 'html.parser').find(
            'title').getText()

        assert response.status_code == 405
        assert title == 'An Error Occurred: Method Not Allowed'
