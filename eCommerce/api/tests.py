from django.test import TestCase

# Create your tests here.
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
        self.token = response.data['token']
        self.api_authentication()

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION= "Token "+ self.token)

    def test_user_info_authenticated(self):
        response = self.client.get("http://127.0.0.1:8000/api/v1/user/info/")
        self.assertEquals(response.data['data']['username'], "amr98")
        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_user_info_un_authenticated(self):
        self.client.force_authenticate(user=None)
        response = self.client.get("http://127.0.0.1:8000/api/v1/user/info/")
        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_add_product_correctly(self):
        data = {"name":"shirt", "price":"10.5","category":"clothes","description":"beautiful shirt"}
            
        response = self.client.post("http://127.0.0.1:8000/api/v1/store/", data)
        
        self.assertEquals(response.data['data']['name'],'shirt')
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
