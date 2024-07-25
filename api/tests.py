from rest_framework import status
from rest_framework.test import APITestCase

# Create your tests here.

BASE_URL = "http://127.0.0.1:8000/api"


class ConnectionTests(APITestCase):
    def test_connection(self):
        response = self.client.get(f'{BASE_URL}/hello-world')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class UserTests(APITestCase):
    def test_get_all(self):
        response = self.client.get(f'{BASE_URL}/users')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post(self):
        data = {
            "first_name": 'First',
            "last_name": 'Last',
            "email": 'user@email.com',
            "username": 'first.last',
            "phone_number": '999999999',
            "role": 'admin',
            "invitation_is_pending": False
        }

        response = self.client.post(f'{BASE_URL}/users', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


