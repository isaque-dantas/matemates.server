from rest_framework.test import APITestCase

from api.tests.entry_utils import EntryUtils
from api.tests.test_user_utils import UserUtils


class DefinitionUtils:
    pass


class TestDefinitionView(APITestCase):
    user_utils = UserUtils()
    entry_utils = EntryUtils()
    definition_utils = DefinitionUtils()