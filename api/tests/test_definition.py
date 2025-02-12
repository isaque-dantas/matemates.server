from rest_framework.test import APITestCase
from django.test import TestCase
from api import log

from api.serializers.definition import DefinitionSerializer
from api.services.definition import DefinitionService
from api.tests.utils.entry_utils import EntryUtils
from api.tests.utils.knowledge_area_utils import KnowledgeAreaUtils
from api.tests.utils.user_utils import UserUtils
from api.tests.utils.definition_utils import DefinitionUtils
from api.tests import BASE_URL
from rest_framework import status


class DefinitionViewTestCase(APITestCase):
    user_utils = UserUtils()
    entry_utils = EntryUtils()
    definition_utils = DefinitionUtils()
    knowledge_area_utils = KnowledgeAreaUtils()

    def test_get__on_happy_path__should_return_OK(self):
        self.knowledge_area_utils.create_all()
        self.entry_utils.set_database_environment({"calculadora": True}, force_operations=True)
        self.user_utils.set_database_environment({"admin-user": True})

        pk = self.definition_utils.get_pk_from_data_identifier("calculadora-0")

        response = self.client.get(
            f"{BASE_URL}/definition/{pk}",
            headers=self.user_utils.admin_credentials
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)


class DefinitionSerializerTestCase(TestCase):
    user_utils = UserUtils()
    entry_utils = EntryUtils()
    knowledge_area_utils = KnowledgeAreaUtils()
    definition_utils = DefinitionUtils()

    def test_to_representation__on_happy_path__should_return_dict(self):
        self.knowledge_area_utils.create_all()
        self.entry_utils.set_database_environment({"calculadora": True}, force_operations=True)
        definition = self.definition_utils.retrieve("calculadora-0")
        serializer = DefinitionSerializer(definition)
        data = serializer.data

        self.assertIn("content", data)
        self.assertIn("knowledge_area", data)

    def test_validate__on_happy_path__should_return_valid(self):
        self.knowledge_area_utils.create_all()

        definition_data = self.entry_utils.get_data("calculadora")["definitions"][0]
        definition_data["content"] = "Outra definição, que está editada, obviamente."

        serializer = DefinitionSerializer(data=definition_data)
        self.assertTrue(serializer.is_valid())

    def test_validate__non_existent_knowledge_area__should_return_invalid(self):
        serializer = DefinitionSerializer(
            data={
                "content": "Esta definição está mentindo.",
                "knowledge_area__content": "inexistente"
            }
        )

        self.assertFalse(serializer.is_valid())


class DefinitionServiceTestCase(TestCase):
    user_utils = UserUtils()
    entry_utils = EntryUtils()
    knowledge_area_utils = KnowledgeAreaUtils()
    definition_utils = DefinitionUtils()

    def test_update__on_happy_path__should_edit_in_database(self):
        self.knowledge_area_utils.create_all()
        self.entry_utils.set_database_environment({"calculadora": True}, force_operations=True)

        serializer = DefinitionSerializer(
            self.definition_utils.retrieve("calculadora-0"),
            data={"content": "Definição editada", "knowledge_area__content": "cinemática"}
        )

        serializer.is_valid()
        DefinitionService.update(serializer)
        content_after_update = self.definition_utils.retrieve("calculadora-0").content

        self.assertEqual("Definição editada", content_after_update)

    def test_delete__on_happy_path__should_delete_in_database(self):
        self.knowledge_area_utils.create_all()
        self.entry_utils.set_database_environment({"calculadora": True}, force_operations=True)

        pk = self.definition_utils.retrieve("calculadora-0").pk
        DefinitionService.delete(pk)

        self.assertFalse(self.definition_utils.exists(pk))
