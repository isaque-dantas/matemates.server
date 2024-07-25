from rest_framework import status
from rest_framework.test import APITestCase

from api.serializers import UserCreateSerializer
from api.models import User

BASE_URL = "http://127.0.0.1:8000/api"


class ConnectionTests(APITestCase):
    def test_connection(self):
        response = self.client.get(f'{BASE_URL}/hello-world')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class UserTests(APITestCase):
    def test_get_all(self):
        response = self.client.get(f'{BASE_URL}/users')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_by_id(self):
        response = self.client.get(f'{BASE_URL}/users')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post(self):
        data = {
            "first_name": 'First',
            "last_name": 'Last',
            "email": 'user-1@email.com',
            "password": 'pass',
            "username": 'user-1',
            "phone_number": '999999999'
        }

        response = self.client.post(f'{BASE_URL}/users', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_post_with_non_existent_field(self):
        data = {
            "first_name": 'First',
            "last_name": 'Last',
            "email": 'user-2@email.com',
            "password": 'pass',
            "username": 'user-2',
            "phone_number": '999999999',
            "non_existent_field": 'foo'
        }

        response = self.client.post(f'{BASE_URL}/users', data)
        self.assertNotIn('non_existent_field', response.data)

    def test_post_with_repeated_unique_attributes(self):
        data = {
            "first_name": 'First',
            "last_name": 'Last',
            "email": 'user-3@email.com',
            "password": 'pass',
            "username": 'user-3',
            "phone_number": '999999999'
        }

        self.client.post(f'{BASE_URL}/users', data)
        response = self.client.post(f'{BASE_URL}/users', data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
