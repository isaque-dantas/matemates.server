from rest_framework.test import APITestCase

from api.tests.utils.entry_utils import EntryUtils
from api.tests.utils.knowledge_area_utils import KnowledgeAreaUtils
from api.tests.utils.user_utils import UserUtils


class EntryUtilsTests(APITestCase):
    user_utils = UserUtils()
    entry_utils = EntryUtils()
    knowledge_area_utils = KnowledgeAreaUtils()

    def test_exists_on_existent_entity__should_be_equal_to_true(self):
        self.knowledge_area_utils.create_all()
        self.entry_utils.set_database_environment({'calculadora': True})
        self.assertTrue(self.entry_utils.exists('calculadora'))

    def test_exists_on_non_existent_entity__should_be_equal_to_false(self):
        self.knowledge_area_utils.create_all()
        self.user_utils.set_database_environment({'admin-user': True})
        self.entry_utils.set_database_environment({'calculadora': False})

        self.assertFalse(self.entry_utils.exists('calculadora'))
