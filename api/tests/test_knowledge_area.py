from rest_framework import status
from rest_framework.test import APITestCase

from api.tests import BASE_URL
from api.tests.entry_utils import EntryUtils
from api.tests.knowledge_area_utils import KnowledgeAreaUtils
from api.tests.user_utils import UserTestsUtils


class KnowledgeAreaTests(APITestCase):
    user_utils = UserTestsUtils()
    entry_utils = EntryUtils()
    knowledge_area_utils = KnowledgeAreaUtils()

    def test_get__on_happy_path__should_return_OK(self):
        self.knowledge_area_utils.create_all()
        self.entry_utils.set_database_environment({"calculadora": True, "angulo-reto": True})

        response = self.client.get(
            f"{BASE_URL}/knowledge_area"
        )

        print(response.data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), len(self.knowledge_area_utils.knowledge_areas))
        self.assertIn("entries", response.data[0])
        self.assertNotEqual(len(response.data[0]["entries"]), 0)

