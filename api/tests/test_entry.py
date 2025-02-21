import os

from rest_framework import status
from rest_framework.test import APITestCase

from api import log
from api.models import Definition, Entry, EntryAccessHistory
from api.serializers.entry import EntrySerializer
from api.services.entry import EntryService
from api.tests import BASE_URL
from api.tests.utils.entry_utils import EntryUtils
from api.tests.utils.image_utils import ImageUtils
from api.tests.utils.knowledge_area_utils import KnowledgeAreaUtils
from api.tests.utils.user_utils import UserUtils
from matemates_server import settings


class EntryViewTestCase(APITestCase):
    user_utils = UserUtils()
    entry_utils = EntryUtils()
    knowledge_area_utils = KnowledgeAreaUtils()

    def test_post__with_common_credentials__should_return_FORBIDDEN(self):
        self.knowledge_area_utils.create_all()
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
        self.knowledge_area_utils.create_all()
        self.user_utils.set_database_environment({"admin-user": True})
        self.entry_utils.set_database_environment({"calculadora": True, "angulo-reto": True})

        response = self.client.get(
            f'{BASE_URL}/entry',
            headers=self.user_utils.admin_credentials
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) == 2)

    def test_get_single__on_happy_path__should_return_OK(self):
        self.knowledge_area_utils.create_all()
        self.entry_utils.set_database_environment({"calculadora": True, "angulo-reto": True})
        self.user_utils.set_database_environment({"admin-user": True})

        calculadora_id = self.entry_utils.retrieve("calculadora").id
        admin_user_id = self.user_utils.retrieve("admin-user").id

        EntryAccessHistory.objects.all().delete()

        response = self.client.get(
            f'{BASE_URL}/entry/{calculadora_id}',
            headers=self.user_utils.admin_credentials
        )

        self.assertEqual(EntryAccessHistory.objects.filter(user__id=admin_user_id).count(), 1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_all_from_specified_knowledge_area__on_happy_path__should_return_OK(self):
        self.knowledge_area_utils.create_all()
        self.user_utils.set_database_environment({"admin-user": True})
        self.entry_utils.set_database_environment({"calculadora": True, "angulo-reto": True})

        response = self.client.get(
            f'{BASE_URL}/entry?knowledge_area=estatística',
            headers=self.user_utils.admin_credentials
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_all_from_specified_knowledge_area__non_existent_knowledge_area__should_return_NOT_FOUND(self):
        self.knowledge_area_utils.create_all()
        self.user_utils.set_database_environment({"admin-user": True})
        response = self.client.get(
            f'{BASE_URL}/entry?knowledge_area=non-existent-knowledge-area',
            headers=self.user_utils.admin_credentials
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_all__non_logged_user__should_not_return_non_validated_entries(self):
        self.knowledge_area_utils.create_all()
        self.entry_utils.set_database_environment({"calculadora": True, "angulo-reto": True})
        response = self.client.get(f'{BASE_URL}/entry')

        print(
            [
                {
                    key: value
                    for key, value in entry.items() if key in ["content", "is_validated"]
                } for entry in response.data
            ]
        )

        are_all_validated = all([entry['is_validated'] for entry in response.data])
        self.assertTrue(are_all_validated)

    def test_get_with_search__calc_parameter__should_return_OK(self):
        self.knowledge_area_utils.create_all()
        self.user_utils.set_database_environment({"admin-user": True})
        self.entry_utils.set_database_environment({"calculadora": True, "angulo-reto": True})

        response = self.client.get(
            f'{BASE_URL}/entry?search_query=calc',
            headers=self.user_utils.admin_credentials,
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_put__on_happy_path__should_return_METHOD_NOT_ALLOWED(self):
        self.knowledge_area_utils.create_all()
        self.user_utils.set_database_environment({"admin-user": True})
        self.entry_utils.set_database_environment({"calculadora": True, "angulo-reto": True})

        calculadora_id = self.entry_utils.retrieve("calculadora").id
        response = self.client.put(
            f'{BASE_URL}/entry/{calculadora_id}',
            data={},
            headers=self.user_utils.admin_credentials,
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_delete__on_happy_path__should_return_NO_CONTENT(self):
        self.knowledge_area_utils.create_all()
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
        self.knowledge_area_utils.create_all()
        self.user_utils.set_database_environment({"admin-user": True})

        response = self.client.delete(
            f'{BASE_URL}/entry/{99999}',
            headers=self.user_utils.admin_credentials
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_patch__on_happy_path__should_return_NO_CONTENT(self):
        self.knowledge_area_utils.create_all()
        self.user_utils.set_database_environment({"admin-user": True})
        self.entry_utils.set_database_environment({"calculadora": True})

        calculadora_id = self.entry_utils.retrieve("calculadora").id

        response = self.client.patch(
            f'{BASE_URL}/entry/{calculadora_id}',
            headers=self.user_utils.admin_credentials,
            format='json',
            data={"content": "*cal.cu.la.do.ra* ma.nu.al"}
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_patch__without_data__should_return_BAD_REQUEST(self):
        self.knowledge_area_utils.create_all()
        self.user_utils.set_database_environment({"admin-user": True})
        self.entry_utils.set_database_environment({"calculadora": True})

        calculadora_id = self.entry_utils.retrieve("calculadora").id

        response = self.client.patch(
            f'{BASE_URL}/entry/{calculadora_id}',
            headers=self.user_utils.admin_credentials,
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("content", response.data)


class EntrySerializerTestCase(APITestCase):
    user_utils = UserUtils()
    entry_utils = EntryUtils()
    knowledge_area_utils = KnowledgeAreaUtils()

    def test_to_representation__on_happy_path__should_return_dict(self):
        self.knowledge_area_utils.create_all()
        self.entry_utils.set_database_environment({"calculadora": True})
        entry = self.entry_utils.retrieve("calculadora")
        serializer = EntrySerializer(entry)

        serialized_data = serializer.data

        self.assertIn("is_validated", serialized_data)

        self.assertIn("terms", serialized_data)
        self.assertIn("syllables", serialized_data["terms"][0])
        self.assertNotIn("entry", serialized_data["terms"])

        self.assertIn("definitions", serialized_data)
        self.assertNotIn("entries", serialized_data["definitions"][0])

        self.assertIn("knowledge_area", serialized_data["definitions"][0])
        self.assertIn("questions", serialized_data)
        self.assertIn("images", serialized_data)

    def test_is_valid__on_happy_path__should_return_true(self):
        self.knowledge_area_utils.create_all()
        self.user_utils.set_database_environment({"admin-user": True})
        self.entry_utils.set_database_environment({"angulo-reto": False})

        serializer = EntrySerializer(data=self.entry_utils.get_data("angulo-reto"))
        self.assertTrue(serializer.is_valid())

    def test_is_valid__duplicated_entry__should_return_false(self):
        self.knowledge_area_utils.create_all()
        self.user_utils.set_database_environment({"admin-user": True})
        self.entry_utils.set_database_environment({"angulo-reto": True})

        serializer = EntrySerializer(data=self.entry_utils.get_data("angulo-reto"))
        self.assertFalse(serializer.is_valid())

    def test_is_valid__definitions_with_non_existent_knowledge_area__should_return_false(self):
        self.knowledge_area_utils.create_all()
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
        self.knowledge_area_utils.create_all()
        self.user_utils.set_database_environment({"admin-user": True})
        self.entry_utils.set_database_environment({"angulo-reto": False})

        data = self.entry_utils.get_data("angulo-reto")
        data["content"] = "ân.gu.lo re.to"

        serializer = EntrySerializer(data=data)
        self.assertFalse(serializer.is_valid())

    def test_is_valid__space_inside_main_term_on_content__should_return_false(self):
        self.knowledge_area_utils.create_all()
        self.entry_utils.set_database_environment({"angulo-reto": False})

        data = self.entry_utils.get_data("angulo-reto")
        data["content"] = "*ân.gu.lo * re.to"

        serializer = EntrySerializer(data=data)
        self.assertFalse(serializer.is_valid())

    def test_is_valid__dot_on_start_and_end_of_content__should_return_false(self):
        self.knowledge_area_utils.create_all()
        self.entry_utils.set_database_environment({"angulo-reto": False})

        data = self.entry_utils.get_data("angulo-reto")
        data["content"] = ".*ân.gu.lo* re.to."

        serializer = EntrySerializer(data=data)
        self.assertFalse(serializer.is_valid())

        log.debug(f"{serializer.errors=}")
        self.assertIn("content", serializer.errors)
        self.assertEqual(len(serializer.errors["content"]), 3)

    def test_is_valid__dot_in_side_of_star_in_content__should_return_false(self):
        self.knowledge_area_utils.create_all()
        self.entry_utils.set_database_environment({"angulo-reto": False})

        data = self.entry_utils.get_data("angulo-reto")
        data["content"] = "ân.gu.lo re*.to"

        serializer = EntrySerializer(data=data)
        self.assertFalse(serializer.is_valid())

    def test_post__with_missing_stars_in_content__should_return_BAD_REQUEST(self):
        self.knowledge_area_utils.create_all()
        self.user_utils.set_database_environment({"admin-user": True})
        self.entry_utils.set_database_environment({"angulo-reto": False})

        data = self.entry_utils.get_data("angulo-reto")
        data["content"] = "an.gu.lo re.to"

        response = self.client.post(
            f'{BASE_URL}/entry',
            data,
            headers=self.user_utils.admin_credentials,
            format='json'
        )

        log.debug(f"{self.user_utils.admin_credentials=}")
        log.debug(f"{response}")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_validate__missing_data__should_return_invalid(self):
        serializer = EntrySerializer(data={})
        self.assertFalse(serializer.is_valid())
        log.debug(serializer.errors)

    def test_validate__missing_content_in_patch__should_return_valid(self):
        serializer = EntrySerializer(data={"main_term_grammatical_category": "numeral"}, context={"is_patch": True})

        is_valid = serializer.is_valid()
        # log.debug(serializer.errors)

        self.assertTrue(is_valid)


class EntryServiceTestCase(APITestCase):
    user_utils = UserUtils()
    entry_utils = EntryUtils()
    knowledge_area_utils = KnowledgeAreaUtils()
    image_utils = ImageUtils()

    def test_get_all_related_to_knowledge_area__on_happy_path__should_not_return_duplicates(self):
        self.knowledge_area_utils.create_all()
        self.entry_utils.set_database_environment({"calculadora": True, "angulo-reto": True})
        entries = EntryService.get_all_related_to_knowledge_area("álgebra", False)

        entries_ids = [entry.pk for entry in entries]
        are_there_any_duplicates = any([entries_ids.count(entry_id) >= 2 for entry_id in entries_ids])
        self.assertFalse(are_there_any_duplicates)

    def test_search_by_content__calc__should_return_one_entry(self):
        self.knowledge_area_utils.create_all()
        self.entry_utils.set_database_environment({"angulo-reto": True, "calculadora": True})

        entries = EntryService.search_by_content("calc", False)

        self.assertEqual(len(entries), 1)
        self.assertEqual(entries[0].content, "calculadora")

    def test_search_by_content__a__should_return_two_entries(self):
        self.knowledge_area_utils.create_all()
        self.entry_utils.set_database_environment({"angulo-reto": True, "calculadora": True})

        entries = EntryService.search_by_content("o", False)

        self.assertEqual(len(entries), 2)
        self.assertEqual(entries[0].content, "ângulo reto")
        self.assertEqual(entries[1].content, "calculadora")

    def test_post__on_happy_path__should_return_CREATED(self):
        self.knowledge_area_utils.create_all()
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

        img_0 = self.image_utils.retrieve("calculadora-0")
        img_1 = self.image_utils.retrieve("calculadora-0")
        files_in_uploads_folder = os.listdir(settings.MEDIA_ROOT)

        self.assertIn(img_0.content.name, files_in_uploads_folder)
        self.assertIn(img_1.content.name, files_in_uploads_folder)

    def test_search_by_content__should_return_two_entries(self):
        self.knowledge_area_utils.create_all()
        self.entry_utils.create_all()

        entries = EntryService.search_by_content(
            "calc",
            should_get_only_validated=False
        )

        self.assertEqual(len(entries), 1)

    def test_make_entry_validated__on_happy_path__should_do_it(self):
        self.knowledge_area_utils.create_all()
        self.entry_utils.set_database_environment({"calculadora": True}, force_operations=True)
        pk = self.entry_utils.retrieve("calculadora").pk

        EntryService.make_entry_validated(pk)

        self.assertTrue(self.entry_utils.retrieve("calculadora").is_validated)

    def test_patch__on_happy_path__should_patch(self):
        self.knowledge_area_utils.create_all()
        self.entry_utils.set_database_environment({"calculadora": True})

        entry = self.entry_utils.retrieve("calculadora")

        serializer = EntrySerializer(entry, data={"content": "po.ta.to.es"}, context={"is_patch": True})
        serializer.is_valid(raise_exception=True)
        EntryService.patch(serializer)

        new_entry = Entry.objects.get(pk=entry.pk)
        log.debug(new_entry)
        self.assertEqual(new_entry.content, "potatoes")
