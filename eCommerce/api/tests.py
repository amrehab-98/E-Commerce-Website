from django.test import TestCase

# Create your tests here.
import json
from rest_framework.test import APIRequestFactory
from api.models import *
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from rest_framework import status
from api.serializers import *


class RegistrationTestCase(APITestCase):
    def test_registration(self):
        data = {"username":"amr98", "email":"amr@gmail.com", "password":"password", 
                "confirm_password":"password", "first_name":"Amr", "last_name": "Ehab"}
        response = self.client.post("/api/v1/register/", data)
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)

class UserViewTestCase(APITestCase):
    product_id = 0
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
        data = {"name":"shirt", "price":10.5,"category":"clothes","description":"beautiful shirt"}
            
        response = self.client.post("http://127.0.0.1:8000/api/v1/store/", data)
        self.product_id = response.data['data']['id']
        self.assertEquals(response.data['data']['name'],'shirt')
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)

class ProductCRUDTestCase(APITestCase):
    def setUp(self):
        data = {"username":"amr98", "email":"amr@gmail.com", "password":"password", 
                "confirm_password":"password", "first_name":"Amr", "last_name": "Ehab"}
        response = self.client.post("/api/v1/register/", data)
        self.token = response.data['token']
        self.api_authentication()
        # add product
        data = {"name":"shirt", "price":10.5,"category":"clothes","description":"beautiful shirt"}    
        response = self.client.post("http://127.0.0.1:8000/api/v1/store/", data)
        self.product_id = response.data['data']['id']

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION= "Token "+ self.token)

    def test_edit_product_correctly(self):
        data = {"id": str(self.product_id), "name":"jacket", "price":"10.5","category":"clothes","description":"beautiful shirt"}    
        response = self.client.put("http://127.0.0.1:8000/api/v1/store/", data)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data['data']['name'],'jacket')
        self.assertEquals(response.data['data']['price'],'10.5')

        response = self.client.get("http://127.0.0.1:8000/api/v1/amr98/products/"+str(self.product_id)+"/")
        # print(response.data)
        self.assertEquals(response.data['product']['name'],'jacket')
        self.assertEquals(response.status_code, status.HTTP_200_OK)
    
    def test_get_product_specs_correctly(self):
        response = self.client.get("http://127.0.0.1:8000/api/v1/amr98/products/"+str(self.product_id)+"/")
        # print(response.data)
        self.assertEquals(response.data['product']['name'],'shirt')
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        

    def test_delete_product_correctly(self):
        response = self.client.get("http://127.0.0.1:8000/api/v1/amr98/products/"+str(self.product_id)+"/")
        self.assertEquals(response.data['product']['name'],'shirt')
        self.assertEquals(response.status_code, status.HTTP_200_OK)

        response = self.client.delete("http://127.0.0.1:8000/api/v1/product/"+str(self.product_id)+'/')
        self.assertEquals(response.status_code, status.HTTP_200_OK)

        response = self.client.get("http://127.0.0.1:8000/api/v1/amr98/products/"+str(self.product_id)+"/")
        self.assertEquals(response.status_code, status.HTTP_404_NOT_FOUND)
