from django.test import TestCase

from api.models.entry_access_history import EntryAccessHistory
from api.services.entry_access_history import EntryAccessHistoryService
from api.tests.utils.entry_utils import EntryUtils
from api.tests.utils.knowledge_area_utils import KnowledgeAreaUtils
from api.tests.utils.user_utils import UserUtils


class EahServiceTestCase(TestCase):
    knowledge_area_utils = KnowledgeAreaUtils()
    user_utils = UserUtils()
    entry_utils = EntryUtils()

    def test_register__on_happy_path_should_create(self):
        self.knowledge_area_utils.create_all()
        self.entry_utils.set_database_environment({"calculadora": True})
        self.user_utils.set_database_environment({"admin-user": True})

        entry_id = self.entry_utils.retrieve("calculadora").pk
        user_id = self.user_utils.retrieve("admin-user").pk

        EntryAccessHistoryService.register(user_id=user_id, entry_id=entry_id)

        self.assertTrue(
            EntryAccessHistory.objects.filter(entry__pk=entry_id, user__pk=user_id).exists()
        )


    def test_get_from_user__on_happy_path__should_return_entities(self):
        self.knowledge_area_utils.create_all()
        self.entry_utils.set_database_environment({"calculadora": True})
        self.user_utils.set_database_environment({"admin-user": True})

        entry_id = self.entry_utils.retrieve("calculadora").pk
        user_id = self.user_utils.retrieve("admin-user").pk

        EntryAccessHistory.objects.create(entry_id=entry_id, user_id=user_id)
        eah_list = EntryAccessHistoryService.get_from_user(user_id=user_id)

        self.assertTrue(eah_list)
