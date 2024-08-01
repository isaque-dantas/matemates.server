from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APITestCase, APIClient

from api.models.user import User
from api.serializers.user import UserSerializer
from matemates_server import settings

BASE_URL = "http://127.0.0.1:8000/api"


class ConnectionTests(APITestCase):
    def test_connection__should_return_OK(self):
        response = self.client.get(f'{BASE_URL}/hello-world')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class UserTestsUtils:
    def __init__(self):
        self.client = APIClient()

    common_user_data = {
        "first_name": "Common",
        "last_name": "User",
        "email": "common-user@email.com",
        "password": "pass",
        "username": "common-user"
    }

    admin_user_data = {
        "first_name": "Admin",
        "last_name": "User",
        "email": settings.ADMIN_EMAIL,
        "password": "pass",
        "username": "admin"
    }

    _credentials_headers = {
        admin_user_data['username']: None,
        common_user_data['username']: None
    }

    _users_data = {
        admin_user_data['username']: admin_user_data,
        common_user_data['username']: common_user_data
    }

    @property
    def common_credentials(self):
        return self.get_credentials(self.common_user_data['username'])

    @property
    def admin_credentials(self):
        return self.get_credentials(self.admin_user_data['username'])

    def get_credentials(self, username: str):
        user_data = self._users_data[username]

        print("*" * 8, self._credentials_headers[username], "*" * 8)
        if self._credentials_headers[username]:
            return self._credentials_headers[username]

        if not self.does_user_exist(username):
            self.create_user(user_data)

        response = self.client.post(f'{BASE_URL}/token', user_data)

        self._credentials_headers[username] = {"Authorization": f'Bearer {response.data["access"]}'}
        print("*" * 8, self._credentials_headers[username], "*" * 8)
        print()
        return self._credentials_headers[username]

    @property
    def common_user_login_data(self):
        return {
            "username": self.common_user_data["username"],
            "password": self.common_user_data["password"]
        }

    def retrieve_user(self, username: str = None) -> User:
        username = username or self.common_user_data["username"]
        return User.objects.get(username=username)

    def does_user_exist(self, username: str = None) -> bool:
        username = username or self.common_user_data["username"]
        return User.objects.filter(username=username).exists()

    def create_user(self, data: dict = None):
        data = data or self.common_user_data

        serializer = UserSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.create(serializer.validated_data)

        print()
        print(self._credentials_headers)
        self._credentials_headers[data['username']] = None
        print(self._credentials_headers)
        print()

    def delete_user(self, username: str = None):
        user = self.retrieve_user()
        user.delete()

        self._credentials_headers[username] = None


class UserUtilsTests(APITestCase):
    utils = UserTestsUtils()

    def test_retrieve_user__should_be_equal_to_data_dictionary(self):
        user = self.utils.retrieve_user()
        self.assertIs(user, User)
        self.assertEqual(user.username, self.utils.common_user_data["username"])

    def test_get_credentials__should_return_access_token(self):
        header_token = self.utils.get_credentials(self.utils.common_user_data['username'])
        self.assertIs(header_token, str)


class UserTests(APITestCase):
    utils = UserTestsUtils()

    def test_post_on_happy_path__should_return_OK(self):
        response = self.client.post(f'{BASE_URL}/users', data=self.utils.common_user_data)

        if response.status_code == status.HTTP_400_BAD_REQUEST:
            print()
            print('test_post_on_happy_path__should_return_OK; ', response.data)
            print()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertNotIn('password', response.data)
        self.assertFalse(response.data['is_admin'])

        self.utils.delete_user()

    def test_post_with_non_existent_field__should_return_CREATED(self):
        response = self.client.post(f'{BASE_URL}/users', data=self.utils.common_user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertNotIn('non_existent_field', response.data)
        self.utils.delete_user()

    def test_post_with_repeated_unique_attributes__should_return_BAD_REQUEST(self):
        self.utils.create_user()

        response = self.client.post(f'{BASE_URL}/users', data=self.utils.common_user_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.utils.delete_user()

    def test_post_with_admin_email__should_return_CREATED(self):
        admin_data = self.utils.common_user_data.copy()
        admin_data['username'] = 'admin-user'
        admin_data['email'] = settings.ADMIN_EMAIL

        response = self.client.post(f'{BASE_URL}/users', admin_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('is_admin', response.data)
        self.assertTrue(response.data['is_admin'])
        self.utils.delete_user('admin-user')

    def test_login_on_happy_path__should_return_OK(self):
        if not self.utils.does_user_exist():
            self.utils.create_user()

        response = self.client.post(f'{BASE_URL}/token', self.utils.common_user_login_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_login_with_wrong_credentials__should_return_UNAUTHORIZED(self):
        data = {"username": 'non-existent-user', "password": 'wrong-password'}
        response = self.client.post(f'{BASE_URL}/token', data)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_on_happy_path__should_return_OK(self):
        response = self.client.get(f'{BASE_URL}/users', headers=self.utils.common_credentials)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('email', response.data)
        self.assertIn('username', response.data)
        self.assertIn('is_admin', response.data)
        self.assertNotIn('password', response.data)

        self.assertEqual(response.data['username'], self.utils.common_user_data['username'])
        self.assertEqual(response.data['email'], self.utils.common_user_data['email'])

    def test_put_on_happy_path__should_return_NO_CONTENT(self):
        edited_data = self.utils.common_user_data.copy()
        edited_data['first_name'] = 'Edited'

        response = self.client.put(f'{BASE_URL}/users', edited_data, headers=self.utils.common_credentials)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        response = self.client.get(f'{BASE_URL}/users', headers=self.utils.common_credentials)
        self.assertEqual(response.data['username'], edited_data['username'])

    def test_put_with_username_from_another_entity__should_return_BAD_REQUEST(self):
        self.utils.create_user({
            'first_name': "Another",
            'last_name': "User",
            'username': "another-user",
            'password': "password",
            'email': "another.user@email.com",
        })

        edited_data = self.utils.common_user_data.copy()
        edited_data['username'] = 'another-user'

        response = self.client.put(f'{BASE_URL}/users', edited_data, headers=self.utils.common_credentials)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = self.client.get(f'{BASE_URL}/users', headers=self.utils.common_credentials)
        self.assertNotEqual(response.data['username'], edited_data['username'])

        self.utils.delete_user("another-user")

    def test_delete_on_happy_path__should_return_NO_CONTENT(self):
        response = self.client.delete(f'{BASE_URL}/users', headers=self.utils.common_credentials)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_without_credentials__should_return_UNAUTHORIZED(self):
        response = self.client.delete(f'{BASE_URL}/users')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_turn_other_user_admin__should_return_OK(self):
        self.utils.create_user(self.utils.admin_user_data)
        response = self.client.post(
            f"{BASE_URL}/users/turn-admin",
            data={"email": self.utils.admin_user_data['email']},
            headers=self.utils.admin_credentials)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        admin_user_data_from_database = User.objects.get(email=self.utils.admin_user_data['email'])
        self.assertTrue(admin_user_data_from_database.is_admin)

        self.utils.delete_user("admin-user")
