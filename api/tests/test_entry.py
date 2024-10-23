import os

from rest_framework import status
from rest_framework.test import APITestCase

from api import log
from api.models import Definition
from api.serializers.entry import EntrySerializer
from api.tests import BASE_URL
from api.tests.entry_utils import EntryUtils
from api.tests.user_utils import UserTestsUtils
from matemates_server import settings


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

        calculadora = self.entry_utils.retrieve("calculadora")
        files_in_uploads_folder = os.listdir(settings.MEDIA_ROOT)
        self.assertIn(f'entry_{calculadora.pk}__image_0__.jpg', files_in_uploads_folder)
        self.assertIn(f'entry_{calculadora.pk}__image_1__.jpg', files_in_uploads_folder)

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

    def test_get_all__on_happy_path__should_return_OK(self):
        self.user_utils.set_database_environment({"admin-user": True})
        self.entry_utils.set_database_environment({"calculadora": True, "angulo-reto": True})

        response = self.client.get(f'{BASE_URL}/entry')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) == 2)

    def test_get_single__on_happy_path__should_return_OK(self):
        self.entry_utils.set_database_environment({"calculadora": True, "angulo-reto": True})

        calculadora_id = self.entry_utils.retrieve("calculadora").id
        response = self.client.get(f'{BASE_URL}/entry/{calculadora_id}')

        log.debug(f"{response.data=}")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertIn("terms", response.data)
        self.assertIn("syllables", response.data["terms"][0])
        self.assertNotIn("entry", response.data["terms"])

        self.assertIn("definitions", response.data)
        self.assertNotIn("entries", response.data["definitions"][0])

        self.assertIn("knowledge_area", response.data["definitions"][0])
        self.assertIn("questions", response.data)
        self.assertIn("images", response.data)

    def test_get_all_from_specified_knowledge_area__on_happy_path__should_return_OK(self):
        self.entry_utils.set_database_environment({"calculadora": True, "angulo-reto": True})

        response = self.client.get(f'{BASE_URL}/entry?knowledge_area=estatística')

        log.debug(f"{response.data=}")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

        calculadora_id = self.entry_utils.retrieve("calculadora").id
        self.assertEqual(response.data[0]["id"], calculadora_id)

    def test_get_all_from_specified_knowledge_area__non_existent_knowledge_area__should_return_NOT_FOUND(self):
        response = self.client.get(f'{BASE_URL}/entry?knowledge_area=non-existent-knowledge-area')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_put__on_happy_path__should_return_OK(self):
        self.user_utils.set_database_environment({"admin-user": True})
        self.entry_utils.set_database_environment({"calculadora": True, "angulo-reto": True})

        calculadora_id = self.entry_utils.retrieve("calculadora").id

        edited_data = self.entry_utils.get_data("calculadora")
        new_definitions = self.entry_utils.get_data("angulo-reto")["definitions"]
        edited_data["definitions"] = new_definitions

        response = self.client.put(
            f'{BASE_URL}/entry/{calculadora_id}',
            edited_data,
            headers=self.user_utils.admin_credentials,
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        calculadora = self.entry_utils.retrieve("calculadora")
        definitions = calculadora.definitions.all()

        self.assertEqual(definitions[0].content, new_definitions[0]["content"])
        self.assertEqual(definitions[0].knowledge_area.content, new_definitions[0]["knowledge_area__content"])

    def test_delete__on_happy_path__should_return_NO_CONTENT(self):
        self.user_utils.set_database_environment({"admin-user": True})
        self.entry_utils.set_database_environment({"calculadora": True, "angulo-reto": False})

        calculadora_id = self.entry_utils.retrieve("calculadora").id

        response = self.client.delete(
            f'{BASE_URL}/entry/{calculadora_id}',
            headers=self.user_utils.admin_credentials
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(self.entry_utils.exists("calculadora"))
        self.assertFalse(Definition.objects.filter(entry__id=calculadora_id).exists())

    def test_delete__non_existent_entry__should_return_NOT_FOUND(self):
        self.user_utils.set_database_environment({"admin-user": True})
        self.entry_utils.set_database_environment({"calculadora": False})

        response = self.client.delete(
            f'{BASE_URL}/entry/{99999}',
            headers=self.user_utils.admin_credentials
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class EntrySerializerTestCase(APITestCase):
    user_utils = UserTestsUtils()
    entry_utils = EntryUtils()

    def test_is_valid__on_happy_path__should_return_true(self):
        self.user_utils.set_database_environment({"admin-user": True})
        self.entry_utils.set_database_environment({"angulo-reto": False})

        serializer = EntrySerializer(data=self.entry_utils.get_data("angulo-reto"))
        self.assertTrue(serializer.is_valid())

    def test_is_valid__duplicated_entry__should_return_false(self):
        self.user_utils.set_database_environment({"admin-user": True})
        self.entry_utils.set_database_environment({"angulo-reto": True})

        serializer = EntrySerializer(data=self.entry_utils.get_data("angulo-reto"))
        self.assertFalse(serializer.is_valid())

    def test_is_valid__definitions_with_non_existent_knowledge_area__should_return_false(self):
        invalid_data = self.entry_utils.get_data("calculadora")
        invalid_data["definitions"] = [
            {
                'content': definition['content'],
                'knowledge_area__content': 'non-existent-knowledge-area'
            }

            for definition in invalid_data["definitions"]
        ]

        invalid_data["definitions"].append(self.entry_utils.get_data("calculadora")["definitions"][0])

        serializer = EntrySerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())

    def test_is_valid__no_main_term_on_content__should_return_false(self):
        self.user_utils.set_database_environment({"admin-user": True})
        self.entry_utils.set_database_environment({"angulo-reto": False})

        data = self.entry_utils.get_data("angulo-reto")
        data["content"] = "ân.gu.lo re.to"

        serializer = EntrySerializer(data=data)
        self.assertFalse(serializer.is_valid())

    def test_is_valid__space_inside_main_term_on_content__should_return_false(self):
        self.entry_utils.set_database_environment({"angulo-reto": False})

        data = self.entry_utils.get_data("angulo-reto")
        data["content"] = "*ân.gu.lo * re.to"

        serializer = EntrySerializer(data=data)
        self.assertFalse(serializer.is_valid())

    def test_is_valid__dot_on_start_and_end_of_content__should_return_false(self):
        self.entry_utils.set_database_environment({"angulo-reto": False})

        data = self.entry_utils.get_data("angulo-reto")
        data["content"] = ".*ân.gu.lo* re.to."

        serializer = EntrySerializer(data=data)
        self.assertFalse(serializer.is_valid())

        log.debug(f"{serializer.errors=}")
        self.assertIn("content", serializer.errors)
        self.assertEqual(len(serializer.errors["content"]), 3)

    def test_is_valid__dot_in_side_of_star_in_content__should_return_false(self):
        self.entry_utils.set_database_environment({"angulo-reto": False})

        data = self.entry_utils.get_data("angulo-reto")
        data["content"] = "ân.gu.lo re*.to"

        serializer = EntrySerializer(data=data)
        self.assertFalse(serializer.is_valid())
