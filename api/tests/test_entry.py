from rest_framework import status
from rest_framework.test import APITestCase

from api import log
from api.tests import BASE_URL
from api.tests.entry_utils import EntryUtils
from api.tests.user_utils import UserTestsUtils


class EntryTests(APITestCase):
    user_utils = UserTestsUtils()
    entry_utils = EntryUtils()

    def test_post__on_happy_path__should_return_CREATED(self):
        self.user_utils.set_database_environment({"admin-user": True})
        self.entry_utils.set_database_environment({"calculadora": False})

        response = self.client.post(
            f'{BASE_URL}/entry',
            self.entry_utils.get_data("calculadora"),
            headers=self.user_utils.admin_credentials,
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(self.entry_utils.exists("calculadora"))

    def test_post__with_duplicated_content__should_return_BAD_REQUEST(self):
        self.user_utils.set_database_environment({"admin-user": True})
        self.entry_utils.set_database_environment({"calculadora": True})

        self.assertTrue(self.entry_utils.exists("calculadora"))

        response = self.client.post(
            f'{BASE_URL}/entry',
            self.entry_utils.get_data("calculadora"),
            headers=self.user_utils.admin_credentials,
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post__with_common_credentials__should_return_FORBIDDEN(self):
        self.user_utils.set_database_environment({"common-user": True})
        self.entry_utils.set_database_environment({"calculadora": False})

        response = self.client.post(
            f'{BASE_URL}/entry',
            self.entry_utils.get_data("calculadora"),
            headers=self.user_utils.common_credentials,
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_post__definitions_with_non_existent_knowledge_areas__should_return_BAD_REQUEST(self):
        self.user_utils.set_database_environment({"admin-user": True})
        self.entry_utils.set_database_environment({"calculadora": False})

        invalid_data = self.entry_utils.get_data("calculadora")
        invalid_data["definitions"] = [
            {
                'content': definition['content'],
                'knowledge_area__content': 'non-existent-knowledge-area'
            }

            for definition in invalid_data["definitions"]
        ]

        invalid_data["definitions"].append(self.entry_utils.get_data("calculadora")["definitions"][0])

        response = self.client.post(
            f'{BASE_URL}/entry',
            invalid_data,
            headers=self.user_utils.admin_credentials,
            format='json'
        )

        log.debug(f'{response.data=}')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # TODO: build test case where definition with non-existent knowledge_area that matches knowledge_area__content
