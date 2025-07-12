from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase

from api import log
from api.models import InvitedEmail
from api.serializers.user import UserSerializer
from api.services.user import UserService
from api.tests import BASE_URL
from api.tests.utils.user_utils import UserUtils
from matemates_server import settings
from api.tests.utils.base64_encoded_files import DOG, CALCULADORA
from matemates_server.settings import BASE_DIR


class UserTests(APITestCase):
    utils = UserUtils()

    def test_post__on_happy_path__should_return_OK(self):
        self.utils.set_database_environment({'common-user': False})

        response = self.client.post(f'{BASE_URL}/users', data=self.utils.common_user_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertNotIn('password', response.data)
        self.assertFalse(response.data['is_staff'])

    def test_post__with_non_existent_field__should_return_CREATED(self):
        self.utils.set_database_environment({'common-user': False})

        data = self.utils.common_user_data.copy()
        data.update({'non_existent_field': 'any'})

        response = self.client.post(f'{BASE_URL}/users', data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertNotIn('non_existent_field', response.data)

    def test_post__with_repeated_unique_attributes__should_return_BAD_REQUEST(self):
        self.utils.set_database_environment({'common-user': True})

        response = self.client.post(f'{BASE_URL}/users', data=self.utils.common_user_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post__with_admin_email__should_return_CREATED(self):
        self.utils.set_database_environment({'admin-user': False})

        admin_data = self.utils.common_user_data.copy()
        admin_data['username'] = self.utils.admin_user_data['username']
        admin_data['email'] = settings.ADMIN_EMAIL

        response = self.client.post(f'{BASE_URL}/users', admin_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('is_staff', response.data)
        self.assertTrue(response.data['is_staff'])

    def test_post__without_image__should_return_CREATED(self):
        self.utils.set_database_environment({'admin-user': False})

        admin_data = self.utils.admin_user_data.copy()
        admin_data.pop("profile_image_base64_encoded_string", None)

        response = self.client.post(f'{BASE_URL}/users', admin_data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('is_staff', response.data)
        self.assertTrue(response.data['is_staff'])

    def test_login_on_happy_path__should_return_OK(self):
        self.utils.set_database_environment({'common-user': True})

        response = self.client.post(f'{BASE_URL}/token', self.utils.common_user_login_data)
        log.debug(response.data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_login_with_wrong_credentials__should_return_UNAUTHORIZED(self):
        data = {"email": 'wrong_email@email.com', "password": 'wrong-password'}
        response = self.client.post(f'{BASE_URL}/token', data)

        log.debug(response)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_on_happy_path__should_return_OK(self):
        self.utils.set_database_environment({'common-user': True})
        response = self.client.get(f'{BASE_URL}/users', headers=self.utils.common_credentials)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('email', response.data)
        self.assertIn('username', response.data)
        self.assertIn('is_staff', response.data)
        self.assertNotIn('password', response.data)

        self.assertEqual(response.data['username'], self.utils.common_user_data['username'])
        self.assertEqual(response.data['email'], self.utils.common_user_data['email'])

    def test_put_on_happy_path__should_return_NO_CONTENT(self):
        self.utils.set_database_environment({'common-user': True})

        edited_data = self.utils.common_user_data.copy()
        edited_data['name'] = 'Edited User'

        response = self.client.put(f'{BASE_URL}/users', edited_data, headers=self.utils.common_credentials)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        edited_user = self.utils.retrieve('common-user')
        self.assertEqual(edited_user.name, edited_data['name'])

    def test_put_with_username_from_another_user__should_return_BAD_REQUEST(self):
        self.utils.set_database_environment({'admin-user': True, 'common-user': True})

        response = self.client.put(
            f'{BASE_URL}/users', self.utils.admin_user_data, headers=self.utils.common_credentials)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        user = self.utils.retrieve(self.utils.common_user_data['username'])
        self.assertNotEqual(user.username, self.utils.admin_user_data['username'])

    def test_delete_on_happy_path__should_return_NO_CONTENT(self):
        self.utils.set_database_environment({'common-user': True})

        response = self.client.delete(f'{BASE_URL}/users', headers=self.utils.common_credentials)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_without_credentials__should_return_UNAUTHORIZED(self):
        response = self.client.delete(f'{BASE_URL}/users')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_turn_other_existent_user_admin__should_return_OK(self):
        self.utils.set_database_environment({'admin-user': True, 'common-user': True})

        response = self.client.post(
            f"{BASE_URL}/users/turn-admin",
            data={"email": self.utils.common_user_data['email']},
            headers=self.utils.admin_credentials
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        common = self.utils.retrieve('common-user')
        self.assertTrue(common.is_staff)

        self.utils.set_database_environment({'common-user': False})

    def test_turn_other_non_existent_user_admin__should_return_OK(self):
        self.utils.set_database_environment({'admin-user': True, 'common-user': False})

        response = self.client.post(
            f"{BASE_URL}/users/turn-admin",
            data={"email": self.utils.common_user_data['email']},
            headers=self.utils.admin_credentials
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertTrue(InvitedEmail.objects.filter(email=self.utils.common_user_data['email']).exists())


class UserSerializerTestCase(TestCase):
    user_utils = UserUtils()

    def test_is_valid__on_happy_path__should_return_VALID(self):
        serializer = UserSerializer(
            data={
                "name": "New User",
                "username": "new-user",
                "password": "password",
                "email": "email@email.com",
            }
        )

        serializer.is_valid(raise_exception=True)
        self.assertTrue(serializer.is_valid())

    def test_is_valid__without_data__should_return_INVALID(self):
        serializer = UserSerializer(data={})
        log.debug(serializer.initial_data)
        self.assertFalse(serializer.is_valid())

    def test_is_valid__on_edit_profile_image__should_return_VALID(self):
        serializer = UserSerializer(
            data={"profile_image_base64": DOG},
            context={'is_profile_image_update': True}
        )

        serializer.is_valid(raise_exception=True)
        self.assertTrue(serializer.is_valid())

    def test_is_valid__email_in_wrong_format__should_return_INVALID(self):
        data = self.user_utils.get_data("common-user")
        data["email"] = "invalid email"

        serializer = UserSerializer(data=data)

        self.assertFalse(serializer.is_valid())


class UserServiceTestCase(TestCase):
    user_utils = UserUtils()

    def test_update_profile_image__on_happy_path__should_do_it(self):
        self.user_utils.set_database_environment({"common-user": True})
        user = self.user_utils.retrieve('common-user')

        serializer = UserSerializer(
            user,
            data={"profile_image_base64": CALCULADORA},
            context={"is_profile_image_update": True}
        )

        serializer.is_valid(raise_exception=True)

        UserService.update_profile_image(serializer)
        user_after_update = self.user_utils.retrieve('common-user')

        self.assertEqual(user_after_update.profile_image.open().read(), open(f"{BASE_DIR}/api/tests/utils/calculadora.png", mode='rb').read())
