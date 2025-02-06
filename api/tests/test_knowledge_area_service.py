from rest_framework.test import APITestCase

from api.services.knowledge_area import KnowledgeAreaService
from api.tests.entry_utils import EntryUtils
from api.tests.knowledge_area_utils import KnowledgeAreaUtils
from api.tests.user_utils import UserTestsUtils


class KnowledgeAreaTests(APITestCase):
    user_utils = UserTestsUtils()
    entry_utils = EntryUtils()
    knowledge_area_utils = KnowledgeAreaUtils()

    def test_validate_content__with_valid_content__should_return_empty_list(self):
        self.knowledge_area_utils.set_database_environment({'estatistica': False})
        errors = KnowledgeAreaService.get_validation_errors_in_content('estatística')
        self.assertEqual(errors, [])

    def test_validate_content__with_already_existent_content__should_return_uniqueness_error(self):
        self.knowledge_area_utils.set_database_environment({'estatistica': True})
        errors = KnowledgeAreaService.get_validation_errors_in_content('estatística')
        self.assertEqual(errors, ['a área do conhecimento \'estatística\' já existe.'])

    def test_validate_content__with_already_existent_content_and_instance__should_return_empty_list(self):
        self.knowledge_area_utils.set_database_environment({'estatistica': True})

        errors = KnowledgeAreaService.get_validation_errors_in_content(
            'estatística',
            self.knowledge_area_utils.retrieve("estatística")
        )

        self.assertEqual(errors, [])

    def test_validate_content__with_already_existent_content_and_instance_with_different_content__should_return_uniqueness_error(self):
        self.knowledge_area_utils.set_database_environment({'estatistica': True, 'algebra': True})

        errors = KnowledgeAreaService.get_validation_errors_in_content(
            'álgebra',
            self.knowledge_area_utils.retrieve("estatística")
        )

        self.assertEqual(errors, ['a área do conhecimento \'álgebra\' já existe.'])
