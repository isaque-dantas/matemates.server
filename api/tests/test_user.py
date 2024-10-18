from rest_framework import status
from rest_framework.test import APITestCase

from api import log
from api.tests import BASE_URL
from api.tests.user_utils import UserTestsUtils
from matemates_server import settings


# TODO: add Invited Email instance to database when a user is invited to be admin

class UserTests(APITestCase):
    utils = UserTestsUtils()

    def test_post_on_happy_path__should_return_OK(self):
        self.utils.set_database_environment({'common-user': False})

        response = self.client.post(f'{BASE_URL}/users', data=self.utils.common_user_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertNotIn('password', response.data)
        self.assertFalse(response.data['is_admin'])

        self.utils.refresh_tokens()

    def test_post_with_non_existent_field__should_return_CREATED(self):
        self.utils.set_database_environment({'common-user': False})

        data = self.utils.common_user_data.copy()
        data.update({'non_existent_field': 'any'})

        response = self.client.post(f'{BASE_URL}/users', data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertNotIn('non_existent_field', response.data)

        self.utils.refresh_tokens()

    def test_post_with_repeated_unique_attributes__should_return_BAD_REQUEST(self):
        self.utils.set_database_environment({'common-user': True})

        response = self.client.post(f'{BASE_URL}/users', data=self.utils.common_user_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.utils.refresh_tokens()

    def test_post_with_admin_email__should_return_CREATED(self):
        self.utils.set_database_environment({'admin-user': False})

        admin_data = self.utils.common_user_data.copy()
        admin_data['username'] = self.utils.admin_user_data['username']
        admin_data['email'] = settings.ADMIN_EMAIL

        response = self.client.post(f'{BASE_URL}/users', admin_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('is_admin', response.data)
        self.assertTrue(response.data['is_admin'])

        self.utils.refresh_tokens()

    def test_login_on_happy_path__should_return_OK(self):
        self.utils.set_database_environment({'common-user': True})

        response = self.client.post(f'{BASE_URL}/token', self.utils.common_user_login_data)
        log.debug(response.data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_login_with_wrong_credentials__should_return_UNAUTHORIZED(self):
        data = {"username": 'non-existent-user', "password": 'wrong-password'}
        response = self.client.post(f'{BASE_URL}/token', data)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_on_happy_path__should_return_OK(self):
        self.utils.set_database_environment({'common-user': True})
        response = self.client.get(f'{BASE_URL}/users', headers=self.utils.common_credentials)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('email', response.data)
        self.assertIn('username', response.data)
        self.assertIn('is_admin', response.data)
        self.assertNotIn('password', response.data)

        self.assertEqual(response.data['username'], self.utils.common_user_data['username'])
        self.assertEqual(response.data['email'], self.utils.common_user_data['email'])

    def test_put_on_happy_path__should_return_NO_CONTENT(self):
        self.utils.set_database_environment({'common-user': True})

        edited_data = self.utils.common_user_data.copy()
        edited_data['name'] = 'Edited User'

        response = self.client.put(f'{BASE_URL}/users', edited_data, headers=self.utils.common_credentials)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        edited_user = self.utils.retrieve_user('common-user')
        self.assertEqual(edited_user.name, edited_data['name'])

        self.utils.refresh_tokens()

    def test_put_with_username_from_another_user__should_return_BAD_REQUEST(self):
        self.utils.set_database_environment({'admin-user': True, 'common-user': True})

        response = self.client.put(
            f'{BASE_URL}/users', self.utils.admin_user_data, headers=self.utils.common_credentials)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        user = self.utils.retrieve_user(self.utils.common_user_data['username'])
        self.assertNotEqual(user.username, self.utils.admin_user_data['username'])

    def test_delete_on_happy_path__should_return_NO_CONTENT(self):
        self.utils.set_database_environment({'common-user': True})

        response = self.client.delete(f'{BASE_URL}/users', headers=self.utils.common_credentials)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.utils.refresh_tokens()

    def test_delete_without_credentials__should_return_UNAUTHORIZED(self):
        response = self.client.delete(f'{BASE_URL}/users')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.utils.refresh_tokens()

    def test_turn_other_user_admin__should_return_OK(self):
        self.utils.set_database_environment({'admin-user': True, 'common-user': True})

        response = self.client.post(
            f"{BASE_URL}/users/turn-admin",
            data={"email": self.utils.common_user_data['email']},
            headers=self.utils.admin_credentials)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        admin = self.utils.retrieve_user('admin-user')
        self.assertTrue(admin.is_admin)
