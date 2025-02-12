from rest_framework import status
from rest_framework.test import APITestCase

from api.serializers.image import ImageSerializer
from api.services.image import ImageService
from api.tests import BASE_URL
from api.tests.utils.entry_utils import EntryUtils
from api.tests.utils.image_utils import ImageUtils
from api.tests.utils.knowledge_area_utils import KnowledgeAreaUtils
from api.tests.utils.user_utils import UserUtils
from api import log
from django.test import TestCase


class TestImageView(APITestCase):
    entry_utils = EntryUtils()
    user_utils = UserUtils()
    knowledge_area_utils = KnowledgeAreaUtils()
    image_utils = ImageUtils()

    def test_get__on_happy_path__should_return_200(self):
        self.knowledge_area_utils.create_all()
        self.entry_utils.set_database_environment({"calculadora": True})
        self.user_utils.set_database_environment({"admin-user": True})

        image_pk = self.image_utils.get_pk_from_data_identifier("calculadora-0")

        response = self.client.get(
            f"{BASE_URL}/image/{image_pk}",
            headers=self.user_utils.admin_credentials
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get__non_admin_user_and_non_validated_data__should_return_FORBIDDEN(self):
        self.knowledge_area_utils.create_all()
        self.entry_utils.set_database_environment({"calculadora": True})

        image_pk = self.image_utils.get_pk_from_data_identifier("calculadora-0")
        response = self.client.get(f"{BASE_URL}/image/{image_pk}")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class TestImageSerializer(TestCase):
    entry_utils = EntryUtils()
    user_utils = UserUtils()
    knowledge_area_utils = KnowledgeAreaUtils()
    image_utils = ImageUtils()

    def test_validate__valid_data__should_return_valid(self):
        data = self.entry_utils.get_data("calculadora")["images"][0]
        serializer = ImageSerializer(data=data)

        is_valid = serializer.is_valid()
        # log.debug(f"{serializer.errors=}")

        self.assertTrue(is_valid)

    def test_validate__missing_attributes__should_return_invalid(self):
        serializer = ImageSerializer(data={"caption": "Onde foi parar o content?"})
        self.assertFalse(serializer.is_valid())

    def test_validate__on_update_and_missing_base64_image__should_return_valid(self):
        serializer = ImageSerializer(
            data={"caption": "Onde foi parar o content?"},
            context={"is_update": True}
        )

        is_valid = serializer.is_valid()
        self.assertTrue(is_valid)


class TestImageService(TestCase):
    entry_utils = EntryUtils()
    user_utils = UserUtils()
    knowledge_area_utils = KnowledgeAreaUtils()
    image_utils = ImageUtils()

    def test_update__on_happy_path__should_update_in_database(self):
        self.knowledge_area_utils.create_all()
        self.entry_utils.set_database_environment({"calculadora": True})

        instance = self.image_utils.retrieve("calculadora-0")
        data = self.entry_utils.get_data("calculadora")["images"][1]

        serializer = ImageSerializer(instance, data=data)
        serializer.is_valid()
        ImageService.update(serializer)

        image_from_db = self.image_utils.retrieve(instance.pk)
        self.assertEqual(image_from_db.caption, data["caption"])
