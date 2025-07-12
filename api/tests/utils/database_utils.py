from api import log
from django.db import models

from api.models import Entry, Definition, Question, Image, User, KnowledgeArea
from api.serializers.definition import DefinitionSerializer
from api.serializers.entry import EntrySerializer
from api.serializers.image import ImageSerializer
from api.serializers.knowledge_area import KnowledgeAreaSerializer
from api.serializers.question import QuestionSerializer
from api.serializers.user import UserSerializer
from api.services.definition import DefinitionService
from api.services.entry import EntryService
from api.services.image import ImageService
from api.services.knowledge_area import KnowledgeAreaService
from api.services.question import QuestionService
from api.services.user import UserService
from api.tests.utils.request_body import RequestBody
from abc import ABC, abstractmethod


class DatabaseUtils(ABC):
    entity_serializer_translator = {
        Entry: EntrySerializer,
        Definition: DefinitionSerializer,
        Question: QuestionSerializer,
        Image: ImageSerializer,
        User: UserSerializer,
        KnowledgeArea: KnowledgeAreaSerializer,
    }

    entity_service_translator = {
        Entry: EntryService,
        Definition: DefinitionService,
        Question: QuestionService,
        Image: ImageService,
        User: UserService,
        KnowledgeArea: KnowledgeAreaService,
    }

    entity_name_translator = {
        Entry: "entry",
        Definition: "definition",
        Question: "question",
        Image: "image",
        User: "user",
        KnowledgeArea: "knowledge_area",
    }

    def __init__(self, entity: models.Model):
        self.__entity = entity
        self.__entity_name = self.entity_name_translator[entity]
        self.__service = self.entity_service_translator[entity]
        self.__serializer = self.entity_serializer_translator[entity]

    def get_data(self, data_identifier: str) -> dict:
        return RequestBody.get_data(self.__entity_name, data_identifier)

    def create_all(self, force_operations: bool = False):
        for key in RequestBody.get_entity_keys(self.__entity_name):
            self.create(key, force_operations)

    def set_database_environment(self, environment: dict[str, bool], force_operations=False):
        actions = {
            True: lambda e: self.create(e, force_operations),
            False: lambda e: self.delete(e, force_operations),
        }

        for data_identifier, must_create in environment.items():
            actions[must_create](data_identifier)

    @abstractmethod
    def get_entity_query_parameters_from_data_identifier(self, data_identifier: str | int) -> dict:
        pass

    def retrieve(self, data_identifier: str):
        query_parameters = self.get_entity_query_parameters_from_data_identifier(data_identifier)
        return self.__entity.objects.get(**query_parameters)

    def exists(self, data_identifier: str) -> bool:
        query_parameters = self.get_entity_query_parameters_from_data_identifier(data_identifier)
        return self.__entity.objects.filter(**query_parameters).exists()

    def create(self, data_identifier: str, force_operations: bool = False):
        if self.exists(data_identifier) and not force_operations:
            return None

        if force_operations:
            self.delete(data_identifier)

        log.debug(f"Creating {self.__entity_name} identified by '{data_identifier}'")

        request_data = RequestBody.get_data(self.__entity_name, data_identifier)
        serializer = self.__serializer(data=request_data)
        log.debug("")
        serializer.is_valid(raise_exception=True)
        self.__service.create(serializer)

    def delete(self, data_identifier: str, force_operations: bool = False):
        if not self.exists(data_identifier) and not force_operations:
            return None

        if force_operations:
            self.create(data_identifier)

        log.debug(f"Deleting {self.__entity_name} identified by '{data_identifier}'")

        query_parameters = self.get_entity_query_parameters_from_data_identifier(data_identifier)
        self.__entity.objects.filter(**query_parameters).delete()
