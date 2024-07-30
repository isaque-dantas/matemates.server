from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APITestCase

from api.models.user import User
from api.serializers.serializers import UserSerializer
from matemates_server import settings

BASE_URL = "http://127.0.0.1:8000/api"


class ConnectionTests(APITestCase):
    def test_connection__should_return_OK(self):
        response = self.client.get(f'{BASE_URL}/hello-world')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


# self\.client\.get|self\.client\.put|self\.client\.post

class UserTests(APITestCase):
    fake_user_data = {
        "first_name": "Fake",
        "last_name": "User",
        "email": "fake-user@email.com",
        "password": "pass",
        "username": "fake-user"
    }

    _credentials_header = None

    @property
    def credentials(self):
        if self._credentials_header:
            return self._credentials_header

        if not self.does_fake_user_exist():
            self.post_fake_user()

        response = self.client.post(f'{BASE_URL}/token', self.fake_user_login_data)

        # if response.status_code != status.HTTP_200_OK:
        #     print()
        #     print('*** set_credentials ***')
        #     print(response.data)
        #     print()

        self._credentials_header = {"Authorization": f'Bearer {response.data["access"]}'}
        # print(f'*** set credentials to {self._credentials_header} ***')
        return self._credentials_header

    @property
    def fake_user_login_data(self):
        return {
            "username": self.fake_user_data["username"],
            "password": self.fake_user_data["password"]
        }

    def get_fake_user(self) -> Response:
        return self.client.get(f'{BASE_URL}/users', headers=self.credentials)

    def does_fake_user_exist(self):
        return User.objects.filter(username=self.fake_user_data['username']).exists()

    def post_fake_user(self, data: dict = None):
        data = data or self.fake_user_data

        serializer = UserSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.create(serializer.validated_data)

        self._credentials_header = None

    def delete_fake_user(self, username_to_delete: str = None):
        username_to_delete = username_to_delete or self.fake_user_data['username']
        user = User.objects.get(username=username_to_delete)
        user.delete()

    def test_post_on_happy_path__should_return_OK(self):
        response = self.client.post(f'{BASE_URL}/users', data=self.fake_user_data)

        if response.status_code == status.HTTP_400_BAD_REQUEST:
            print()
            print('test_post_on_happy_path__should_return_OK; ', response.data)
            print()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertNotIn('password', response.data)
        self.assertFalse(response.data['is_admin'])

        self.delete_fake_user()

    def test_post_with_non_existent_field__should_return_CREATED(self):
        response = self.client.post(f'{BASE_URL}/users', data=self.fake_user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertNotIn('non_existent_field', response.data)
        self.delete_fake_user()

    def test_post_with_repeated_unique_attributes__should_return_BAD_REQUEST(self):
        self.post_fake_user()

        response = self.client.post(f'{BASE_URL}/users', data=self.fake_user_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.delete_fake_user()

    def test_post_with_admin_email__should_return_CREATED(self):
        admin_data = self.fake_user_data.copy()
        admin_data['username'] = 'admin-user'
        admin_data['email'] = settings.ADMIN_EMAIL

        response = self.client.post(f'{BASE_URL}/users', admin_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('is_admin', response.data)
        self.assertTrue(response.data['is_admin'])
        self.delete_fake_user('admin-user')

    def test_login_on_happy_path__should_return_OK(self):
        if not self.does_fake_user_exist():
            self.post_fake_user()

        response = self.client.post(f'{BASE_URL}/token', self.fake_user_login_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_login_with_wrong_credentials__should_return_UNAUTHORIZED(self):
        data = {"username": 'non-existent-user', "password": 'wrong-password'}
        response = self.client.post(f'{BASE_URL}/token', data)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_on_happy_path__should_return_OK(self):
        response = self.client.get(f'{BASE_URL}/users', headers=self.credentials)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('email', response.data)
        self.assertIn('username', response.data)
        self.assertIn('is_admin', response.data)
        self.assertNotIn('password', response.data)

        self.assertEqual(response.data['username'], self.fake_user_data['username'])
        self.assertEqual(response.data['email'], self.fake_user_data['email'])

    def test_put_on_happy_path__should_return_NO_CONTENT(self):
        edited_data = self.fake_user_data.copy()
        edited_data['first_name'] = 'Edited'

        response = self.client.put(f'{BASE_URL}/users', edited_data, headers=self.credentials)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        response = self.client.get(f'{BASE_URL}/users', headers=self.credentials)
        self.assertEqual(response.data['username'], edited_data['username'])

    def test_put_with_username_from_another_entity__should_return_BAD_REQUEST(self):
        self.post_fake_user({
            'first_name': "Another",
            'last_name': "User",
            'username': "another-user",
            'password': "password",
            'email': "another.user@email.com",
        })

        edited_data = self.fake_user_data.copy()
        edited_data['username'] = 'another-user'

        response = self.client.put(f'{BASE_URL}/users', edited_data, headers=self.credentials)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = self.client.get(f'{BASE_URL}/users', headers=self.credentials)
        self.assertNotEqual(response.data['username'], edited_data['username'])

        self.delete_fake_user("another-user")

    def test_delete_on_happy_path__should_return_NO_CONTENT(self):
        response = self.client.delete(f'{BASE_URL}/users', headers=self.credentials)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_without_credentials__should_return_UNAUTHORIZED(self):
        response = self.client.delete(f'{BASE_URL}/users')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
