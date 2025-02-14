from rest_framework.test import APITestCase

from api.services.entry import EntryService
from api.tests.entry_utils import EntryUtils


class TestEntryService(APITestCase):
    entry_utils = EntryUtils()

    def test_search_by_content__calc__should_return_one_entry(self):
        self.entry_utils.set_database_environment({"angulo-reto": True, "calculadora": True})

        entries = EntryService.search_by_content("calc", False)

        self.assertEqual(len(entries), 1)
        self.assertEqual(entries[0].content, "calculadora")

    def test_search_by_content__a__should_return_two_entries(self):
        self.entry_utils.set_database_environment({"angulo-reto": True, "calculadora": True})

        entries = EntryService.search_by_content("o", False)

        self.assertEqual(len(entries), 2)
        self.assertEqual(entries[0].content, "ângulo reto")
        self.assertEqual(entries[1].content, "calculadora")
