from rest_framework.test import APITestCase

from api.tests.entry_utils import EntryUtils
from api.tests.knowledge_area_utils import KnowledgeAreaUtils
from api.tests.user_utils import UserTestsUtils


class EntryUtilsTests(APITestCase):
    user_utils = UserTestsUtils()
    entry_utils = EntryUtils()

    def test_exists_on_existent_entity__should_be_equal_to_true(self):
        self.entry_utils.set_database_environment({'calculadora': True})
        self.assertTrue(self.entry_utils.exists('calculadora'))

    def test_exists_on_non_existent_entity__should_be_equal_to_false(self):
        self.user_utils.set_database_environment({'admin-user': True})
        self.entry_utils.set_database_environment({'calculadora': False})

        self.assertFalse(self.entry_utils.exists('calculadora'))
