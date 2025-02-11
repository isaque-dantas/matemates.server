from rest_framework.test import APITestCase
from django.test import TestCase

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
        self.user_utils.set_database_environment({"admin-user": True})

        pk = self.question_utils.get_pk_from_data_identifier("calculadora-0")
        response = self.client.get(
            f"{BASE_URL}/question/{pk}",
            headers=self.user_utils.admin_credentials
        )

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

        self.assertIn("statement", data)
        self.assertIn("answer", data)

    def test_to_representation__from_instance__should_return_dict(self):
        self.knowledge_area_utils.create_all()
        self.entry_utils.set_database_environment({"calculadora": True}, force_operations=True)
        question = self.question_utils.retrieve("calculadora-0")

        serializer = QuestionSerializer(question)
        data = serializer.data

        self.assertIn("id", data)
        self.assertIn("statement", data)
        self.assertIn("answer", data)

    def test_validate__on_happy_path__should_return_valid(self):
        self.knowledge_area_utils.create_all()

        question_data = self.entry_utils.get_data("calculadora")["questions"][0]
        question_data["statement"] = "Pergunta maravilhosa?"

        serializer = QuestionSerializer(data=question_data)
        self.assertTrue(serializer.is_valid())

    def test_validate__missing_attributes__should_return_invalid(self):
        serializer = QuestionSerializer(
            data={"statement": "Por que você não escreve a resposta, também?"}
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
            data={"statement": "Pergunta maravilhosa?", "answer": "Com certeza."}
        )

        serializer.is_valid()
        QuestionService.update(serializer)
        statement_after_update = self.question_utils.retrieve("calculadora-0").statement

        self.assertEqual("Pergunta maravilhosa?", statement_after_update)

    def test_delete__on_happy_path__should_delete_in_database(self):
        self.knowledge_area_utils.create_all()
        self.entry_utils.set_database_environment({"calculadora": True}, force_operations=True)

        pk = self.question_utils.retrieve("calculadora-0").pk
        QuestionService.delete(pk)

        self.assertFalse(self.question_utils.exists(pk))
