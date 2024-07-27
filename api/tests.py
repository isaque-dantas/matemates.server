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

    @property
    def credentials(self):
        if self._credentials is not None:
            return self._credentials

        self.post_fake_user()
        response = self.client.post(f'{BASE_URL}/token', self.fake_user_login_data)
        self._credentials = response.data['access']
        return self._credentials

    @property
    def fake_user_login_data(self):
        return {
            "username": self.fake_user_data["username"],
            "password": self.fake_user_data["password"]
        }

    def get_fake_user(self) -> Response:
        return self.client.get(f'{BASE_URL}/users', headers={"Authorization": f"Bearer {self.credentials}"})

    def post_fake_user(self) -> Response:
        response = self.client.post(f'{BASE_URL}/users', self.fake_user_data.copy())
        # print(f'\n\t> post_fake_user with {self.fake_user_data} returned {response}')
        return response

    def delete_fake_user(self):
        return self.client.delete(f'{BASE_URL}/users', headers={"Authorization": f"Bearer {self.credentials}"})

    def test_post_on_happy_path__should_return_OK(self):
        response = self.post_fake_user()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertNotIn('password', response.data)

        self.delete_fake_user()

    def test_post_with_non_existent_field__should_return_CREATED(self):
        response = self.post_fake_user()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertNotIn('non_existent_field', response.data)
        self.delete_fake_user()

    def test_post_with_repeated_unique_attributes__should_return_BAD_REQUEST(self):
        self.post_fake_user()
        response = self.post_fake_user()

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.delete_fake_user()

    def test_login_on_happy_path__should_return_OK(self):
        self.post_fake_user()

        response = self.client.post(f'{BASE_URL}/token', self.fake_user_login_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

        self.delete_fake_user()

    def test_login_with_wrong_credentials__should_return_UNAUTHORIZED(self):
        data = {"username": 'non-existent-user', "password": 'wrong-password'}
        response = self.client.post(f'{BASE_URL}/token', data)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_on_happy_path__should_return_OK(self):
        self.post_fake_user()

        response = self.client.get(
            f'{BASE_URL}/users',
            headers={"Authorization": f"Bearer {self.credentials}"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('id', response.data)
        self.assertIn('email', response.data)
        self.assertIn('username', response.data)
        self.assertNotIn('password', response.data)

        self.assertEqual(response.data['username'], self.fake_user_data['username'])
        self.assertEqual(response.data['email'], self.fake_user_data['email'])

        self.delete_fake_user()

    def test_put_on_happy_path__should_return_NO_CONTENT(self):
        response = self.post_fake_user()

        edited_data = self.fake_user_data.copy()
        edited_data.update({'id': response.data['id']})
        edited_data['username'] = 'another-fake-user'

        response = self.client.put(
            f'{BASE_URL}/users', edited_data, headers={"Authorization": f"Bearer {self.credentials}"})

        print(edited_data, type(edited_data))
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        response = self.client.get(f'{BASE_URL}/users', headers={"Authorization": f"Bearer {self.credentials}"})
        self.assertEqual(response.data['username'], edited_data['username'])

        self.delete_fake_user()

    def test_delete_on_happy_path__should_return_NO_CONTENT(self):
        self.post_fake_user()

        response = self.delete_fake_user()
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_without_credentials__should_return_FORBIDDEN(self):
        response = self.client.delete(f'{BASE_URL}/users')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
