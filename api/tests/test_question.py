from rest_framework.test import APITestCase
from django.test import TestCase
from api import log

from api.serializers.question import QuestionSerializer
from api.services.question import QuestionService
from api.tests.utils.entry_utils import EntryUtils
from api.tests.utils.knowledge_area_utils import KnowledgeAreaUtils
from api.tests.utils.user_utils import UserUtils
from api.tests.utils.question_utils import QuestionUtils
from api.tests import BASE_URL
from rest_framework import status


class TestQuestionView(APITestCase):
    user_utils = UserUtils()
    entry_utils = EntryUtils()
    question_utils = QuestionUtils()
    knowledge_area_utils = KnowledgeAreaUtils()

    def test_get__on_happy_path__should_return_OK(self):
        self.knowledge_area_utils.create_all()
        self.entry_utils.set_database_environment({"calculadora": True}, force_operations=True)

        pk = self.question_utils.get_pk_from_data_identifier("calculadora-0")
        response = self.client.get(f"{BASE_URL}/question/{pk}")

        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestQuestionSerializer(TestCase):
    user_utils = UserUtils()
    entry_utils = EntryUtils()
    knowledge_area_utils = KnowledgeAreaUtils()
    question_utils = QuestionUtils()

    def test_to_representation__on_happy_path__should_return_dict(self):
        serializer = QuestionSerializer(data=self.entry_utils.get_data("calculadora")["questions"][0])
        serializer.is_valid()
        data = serializer.data

        self.assertIn("id", data)
        self.assertIn("statement", data)
        self.assertIn("answer", data)

    def test_validate__on_happy_path__should_return_valid(self):
        self.knowledge_area_utils.create_all()

        question_data = self.entry_utils.get_data("calculadora")["questions"][0]
        question_data["content"] = "Outra definição, que está editada, obviamente."

        serializer = QuestionSerializer(data=question_data)
        self.assertTrue(serializer.is_valid())

    def test_validate__non_existent_knowledge_area__should_return_invalid(self):
        serializer = QuestionSerializer(
            data={
                "content": "Esta definição está mentindo.",
                "knowledge_area__content": "inexistente"
            }
        )

        self.assertFalse(serializer.is_valid())


class TestQuestionService(TestCase):
    user_utils = UserUtils()
    entry_utils = EntryUtils()
    knowledge_area_utils = KnowledgeAreaUtils()
    question_utils = QuestionUtils()

    def test_update__on_happy_path__should_edit_in_database(self):
        self.knowledge_area_utils.create_all()
        self.entry_utils.set_database_environment({"calculadora": True}, force_operations=True)

        serializer = QuestionSerializer(
            self.question_utils.retrieve("calculadora-0"),
            data={"content": "Definição editada", "knowledge_area__content": "cinemática"}
        )

        serializer.is_valid()
        QuestionService.update(serializer)
        content_after_update = self.question_utils.retrieve("calculadora-0").content

        self.assertEqual("Definição editada", content_after_update)

    def test_delete__on_happy_path__should_delete_in_database(self):
        self.knowledge_area_utils.create_all()
        self.entry_utils.set_database_environment({"calculadora": True}, force_operations=True)

        pk = self.question_utils.retrieve("calculadora-0").pk
        QuestionService.delete(pk)

        self.assertFalse(self.question_utils.exists(pk))
