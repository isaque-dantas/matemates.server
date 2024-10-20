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

        # log.debug(f'{response.data=}')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_all__on_happy_path__should_return_OK(self):
        self.user_utils.set_database_environment({"common-user": True})
        self.entry_utils.set_database_environment({"calculadora": True, "angulo-reto": True})

        response = self.client.get(
            f'{BASE_URL}/entry',
            headers=self.user_utils.common_credentials,
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) == 2)

    def test_get_single__on_happy_path__should_return_OK(self):
        self.entry_utils.set_database_environment({"calculadora": True, "angulo-reto": True})

        calculadora_id = self.entry_utils.retrieve("calculadora").id
        response = self.client.get(f'{BASE_URL}/entry/{calculadora_id}')

        log.debug(f"{response.data=}")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertIn("terms", response.data)
        self.assertIn("definitions", response.data)
        self.assertIn("knowledge_area", response.data["definitions"][0])
        self.assertIn("questions", response.data)
        self.assertIn("images", response.data)

    def test_get_all__from_specified_knowledge_area__should_return_OK(self):
        self.entry_utils.set_database_environment({"calculadora": True, "angulo-reto": True})

        calculadora_id = self.entry_utils.retrieve("calculadora").id
        response = self.client.get(
            f'{BASE_URL}/entry?knowledge_area=estatística',
        )

        log.debug(f"{response.data=}")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["id"], calculadora_id)
