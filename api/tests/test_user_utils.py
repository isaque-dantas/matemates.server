from rest_framework import status
from rest_framework.test import APITestCase

from . import BASE_URL
from .user_utils import UserTestsUtils


class UserUtilsTests(APITestCase):
    utils = UserTestsUtils()

    def test_retrieve_user__should_be_equal_to_data_dictionary(self):
        self.utils.set_database_environment({'admin-user': False, 'common-user': True})

        user = self.utils.retrieve_user()
        self.assertEqual(user.username, self.utils.common_user_data['username'])

    def test_get_credentials__should_return_access_token(self):
        self.utils.set_database_environment({'admin-user': False, 'common-user': True})

        header_token = self.utils.get_credentials('common-user')
        self.assertIn('Authorization', header_token)

    def test_get_credentials_after_delete_and_create_user__should_return_access_token(self):
        self.utils.set_database_environment({'admin-user': True, 'common-user': False})
        self.utils.set_database_environment({'admin-user': True, 'common-user': True})
        header_token = self.utils.common_credentials
        self.assertIn('Authorization', header_token)

        header_token = self.utils.common_credentials
        self.assertIn('Authorization', header_token)

        # response = self.client.get(f"{BASE_URL}/users", headers=self.utils.common_credentials)
        # self.assertEqual(response.status_code, status.HTTP_200_OK)
