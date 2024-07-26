from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APITestCase

BASE_URL = "http://127.0.0.1:8000/api"


class ConnectionTests(APITestCase):
    def test_connection__should_return_OK(self):
        response = self.client.get(f'{BASE_URL}/hello-world')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class UserTests(APITestCase):
    _credentials = None

    fake_user_data = {
        "first_name": 'Fake',
        "last_name": 'User',
        "email": 'fake-user@email.com',
        "password": 'pass',
        "username": 'fake-user'
    }

    def get_fake_user(self) -> Response:
        return self.client.get(f'{BASE_URL}/users', headers={"Authorization": f"Bearer {self.credentials}"})

    def post_fake_user(self) -> dict:
        self.client.post(f'{BASE_URL}/users', self.fake_user_data)
        return self.fake_user_data

    def delete_fake_user(self):
        return self.client.delete(f'{BASE_URL}/users', headers={"Authorization": f"Bearer {self.credentials}"})

    @property
    def credentials(self):
        if self._credentials is not None:
            return self._credentials

        data = self.post_fake_user()
        response = self.client.post(f'{BASE_URL}/token', {"username": data['username'], "password": data['password']})
        self._credentials = response.data['access']
        return self._credentials

    def test_post_on_happy_path__should_return_OK(self):
        data = {
            "first_name": 'First',
            "last_name": 'Last',
            "email": 'user-1@email.com',
            "password": 'pass',
            "username": 'user-1'
        }

        response = self.client.post(f'{BASE_URL}/users', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertNotIn('password', response.data)

    def test_post_with_non_existent_field__should_return_CREATED(self):
        data = {
            "first_name": 'First',
            "last_name": 'Last',
            "email": 'user-2@email.com',
            "password": 'pass',
            "username": 'user-2',
            "non_existent_field": 'foo'
        }

        response = self.client.post(f'{BASE_URL}/users', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertNotIn('non_existent_field', response.data)

    def test_post_with_repeated_unique_attributes__should_return_BAD_REQUEST(self):
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

    def test_login_on_happy_path__should_return_OK(self):
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
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_login_with_wrong_credentials__should_return_UNAUTHORIZED(self):
        data = {"username": 'non-existent-user', "password": 'wrong-password'}
        response = self.client.post(f'{BASE_URL}/token', data)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_on_happy_path__should_return_OK(self):
        data = {
            "first_name": 'First',
            "last_name": 'Last',
            "email": 'user-5@email.com',
            "password": 'pass',
            "username": 'user-5'
        }

        self.client.post(f'{BASE_URL}/users', data)
        credentials = {"username": data["username"], "password": data["password"]}
        response = self.client.post(f'{BASE_URL}/token', credentials)

        response = self.client.get(
            f'{BASE_URL}/users',
            headers={"Authorization": f"Bearer {response.data['access']}"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('email', response.data)
        self.assertIn('username', response.data)
        self.assertNotIn('password', response.data)

        self.assertEqual(response.data['username'], data["username"])
        self.assertEqual(response.data['email'], data["email"])

    # def test_put_on_happy_path__should_return_NO_CONTENT(self):
    #     data = {
    #         "first_name": 'First',
    #         "last_name": 'Last',
    #         "email": 'user-5@email.com',
    #         "password": 'pass',
    #         "username": 'user-5'
    #     }
    #
    #     self.client.post(f'{BASE_URL}/users', data)
    #     credentials = {"username": data["username"], "password": data["password"]}
    #     response = self.client.post(f'{BASE_URL}/token', credentials)
    #
    #     response = self.client.get(
    #         f'{BASE_URL}/users',
    #         headers={"Authorization": f"Bearer {response.data['access']}"})
    #
    #     self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    #     self.assertIn('email', response.data)
    #     self.assertIn('username', response.data)
    #     self.assertNotIn('password', response.data)

        self.assertEqual(response.data['username'], data["username"])
        self.assertEqual(response.data['email'], data["email"])

    def test_delete_on_happy_path__should_return_NO_CONTENT(self):
        self.post_fake_user()

        response = self.delete_fake_user()
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
