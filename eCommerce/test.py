import json
from rest_framework.test import APIRequestFactory
from api.models import *
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from rest_framework import status
from api.serializers import *

factory = APIRequestFactory()


class RegistrationTestCase(APITestCase):
    def test_registration(self):
        data = {"username":"amr98", "email":"amr@gmail.com", "password":"password", 
                "confirm_password":"password", "first_name":"Amr", "last_name": "Ehab"}
        response = self.client.post("/api/v1/register/", data)
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)

class UserViewTestCase(APITestCase):

    def setUp(self):
        data = {"username":"amr98", "email":"amr@gmail.com", "password":"password", 
                "confirm_password":"password", "first_name":"Amr", "last_name": "Ehab"}
        response = self.client.post("/api/v1/register/", data)
        print(response)
        # self.token = response['token']
        self.api_authentication()

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION= "Token "+ self.token.key)

    def test_user_info_authenticated(self):
        response = self.client.get("api/v1/user/info")
        self.assertEquals(response.status_code, 200)