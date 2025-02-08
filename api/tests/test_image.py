from rest_framework import status
from rest_framework.test import APITestCase

from api.models import Entry, Image, KnowledgeArea
from api.tests import BASE_URL
from api.tests.entry_utils import EntryUtils
from api.tests.knowledge_area_utils import KnowledgeAreaUtils
from api.tests.test_user_utils import UserUtils
from api import log

class ImageTestCase(APITestCase):
    entry_utils = EntryUtils()
    user_utils = UserUtils()
    knowledge_area_utils = KnowledgeAreaUtils()

    def test_get__on_happy_path__should_return_200(self):
        self.knowledge_area_utils.create_all()
        self.entry_utils.set_database_environment({"calculadora": True})

        calculadora: Entry = self.entry_utils.retrieve("calculadora")
        image_pk = Image.objects.filter(entry__pk=calculadora.pk).first().pk

        response = self.client.get(f"{BASE_URL}/entry_image/{image_pk}")

        log.debug(f"{response=}")

        self.assertTrue(response.status_code, status.HTTP_200_OK)
