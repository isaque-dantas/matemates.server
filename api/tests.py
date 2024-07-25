from rest_framework import status
from rest_framework.test import APITestCase

BASE_URL = "http://127.0.0.1:8000/api"


class ConnectionTests(APITestCase):
    def test_connection(self):
        response = self.client.get(f'{BASE_URL}/hello-world')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class UserTests(APITestCase):
    def test_post_on_happy_path(self):
        data = {
            "first_name": 'First',
            "last_name": 'Last',
            "email": 'user-1@email.com',
            "password": 'pass',
            "username": 'user-1'
        }

        response = self.client.post(f'{BASE_URL}/users', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertIn('is_admin', response.data)
        self.assertEqual(response.data['is_admin'], False)
        self.assertNotIn('password', response.data)

    def test_post_with_non_existent_field(self):
        data = {
            "first_name": 'First',
            "last_name": 'Last',
            "email": 'user-2@email.com',
            "password": 'pass',
            "username": 'user-2',
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
            "username": 'user-3'
        }

        self.client.post(f'{BASE_URL}/users', data)
        response = self.client.post(f'{BASE_URL}/users', data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_on_happy_path(self):
        data = {
            "first_name": 'First',
            "last_name": 'Last',
            "email": 'user-4@email.com',
            "password": 'pass',
            "username": 'user-4'
        }

        self.client.post(f'{BASE_URL}/users', data)

        data = {"username": data["username"], "password": data["password"]}

        response = self.client.post(f'{BASE_URL}/token', data)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_get(self):
        data = {
            "first_name": 'First',
            "last_name": 'Last',
            "email": 'user-5@email.com',
            "password": 'pass',
            "username": 'user-5'
        }

        self.client.post(f'{BASE_URL}/users', data)
        data = {"username": data["username"], "password": data["password"]}
        response = self.client.post(f'{BASE_URL}/token', data)

        response = self.client.get(f'{BASE_URL}/users')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
