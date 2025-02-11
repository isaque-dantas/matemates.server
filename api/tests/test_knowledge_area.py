from rest_framework import status
from rest_framework.test import APITestCase

from api.services.knowledge_area import KnowledgeAreaService
from api.tests import BASE_URL
from api.tests.utils.entry_utils import EntryUtils
from api.tests.utils.knowledge_area_utils import KnowledgeAreaUtils
from api.tests.utils.request_body import RequestBody
from api.tests.utils.user_utils import UserUtils


class KnowledgeAreaTests(APITestCase):
    user_utils = UserUtils()
    entry_utils = EntryUtils()
    knowledge_area_utils = KnowledgeAreaUtils()

    def test_get__on_happy_path__should_return_OK(self):
        self.knowledge_area_utils.create_all()
        self.entry_utils.set_database_environment({"calculadora": True, "angulo-reto": True})

        response = self.client.get(
            f"{BASE_URL}/knowledge_area"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), len(RequestBody.get_entity_keys("knowledge_area")))
        self.assertIn("entries", response.data[0])
        self.assertNotEqual(len(response.data[0]["entries"]), 0)

    def test_post__on_happy_path__should_return_CREATED(self):
        self.user_utils.set_database_environment({"admin-user": True})
        self.knowledge_area_utils.set_database_environment({"estatistica": False})

        response = self.client.post(
            f'{BASE_URL}/knowledge_area',
            data=self.knowledge_area_utils.get_data("estatistica"),
            format='json',
            headers=self.user_utils.admin_credentials
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('id', response.data)
        self.assertIn('content', response.data)
        self.assertIn('subject', response.data)

        self.assertTrue(self.knowledge_area_utils.exists("estatistica"))

    def test_put__on_happy_path__should_return_NO_CONTENT(self):
        self.user_utils.set_database_environment({"admin-user": True})
        self.knowledge_area_utils.set_database_environment({"estatistica": True, "algebra": False})

        pk = self.knowledge_area_utils.retrieve("estatistica").pk

        data = self.knowledge_area_utils.get_data("estatistica")
        data["content"] = "biociências"

        response = self.client.put(
            f'{BASE_URL}/knowledge_area/{pk}',
            data=data,
            format='json',
            headers=self.user_utils.admin_credentials
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertIsNotNone(self.knowledge_area_utils.exists("estatistica"))

    def test_delete__on_happy_path__should_return_NO_CONTENT(self):
        self.user_utils.set_database_environment({"admin-user": True})
        self.knowledge_area_utils.set_database_environment({"estatistica": True})

        pk = self.knowledge_area_utils.retrieve("estatistica").pk

        response = self.client.delete(
            f'{BASE_URL}/knowledge_area/{pk}',
            format='json',
            headers=self.user_utils.admin_credentials
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(self.knowledge_area_utils.exists("estatistica"))


class KnowledgeAreaServiceTests(APITestCase):
    user_utils = UserUtils()
    entry_utils = EntryUtils()
    knowledge_area_utils = KnowledgeAreaUtils()

    def test_validate_content__with_valid_content__should_return_empty_list(self):
        self.knowledge_area_utils.set_database_environment({'estatistica': False})
        errors = KnowledgeAreaService.get_validation_errors_in_content('estatística')
        self.assertEqual(errors, [])

    def test_validate_content__with_already_existent_content__should_return_uniqueness_error(self):
        self.knowledge_area_utils.set_database_environment({'estatistica': True})
        errors = KnowledgeAreaService.get_validation_errors_in_content('estatística')
        self.assertEqual(errors, ['a área do conhecimento \'estatística\' já existe.'])

    def test_validate_content__with_already_existent_content_and_instance__should_return_empty_list(self):
        self.knowledge_area_utils.set_database_environment({'estatistica': True})

        errors = KnowledgeAreaService.get_validation_errors_in_content(
            'estatística',
            self.knowledge_area_utils.retrieve("estatistica")
        )

        self.assertEqual(errors, [])

    def test_validate_content__with_already_existent_content_and_instance_with_different_content__should_return_uniqueness_error(
            self):
        self.knowledge_area_utils.set_database_environment({'estatistica': True, 'algebra': True})

        errors = KnowledgeAreaService.get_validation_errors_in_content(
            'álgebra',
            self.knowledge_area_utils.retrieve("estatistica")
        )

        self.assertEqual(errors, ['a área do conhecimento \'álgebra\' já existe.'])
