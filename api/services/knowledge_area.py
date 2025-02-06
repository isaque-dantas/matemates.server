from api.models import KnowledgeArea
from api import log

class KnowledgeAreaService:
    @staticmethod
    def get_by_content(content: str) -> KnowledgeArea:
        return KnowledgeArea.objects.filter(content=content).first()

    @staticmethod
    def exists_content(content: str):
        return KnowledgeArea.objects.filter(content=content).exists()

    @staticmethod
    def create(serializer):
        data = serializer.validated_data
        return KnowledgeArea.objects.create(content=data["content"], subject=data["subject"])

    @staticmethod
    def get_validation_errors_in_content(content: str, instance: KnowledgeArea | None = None):
        knowledge_area = KnowledgeArea.objects.filter(content=content).first()

        if knowledge_area is None:
            return []

        if not instance or instance.pk != knowledge_area.pk:
            return [f'a área do conhecimento \'{content}\' já existe.']

        return []

    @staticmethod
    def exists(pk: int) -> bool:
        return KnowledgeArea.objects.filter(pk=pk).exists()

    @staticmethod
    def get(pk: int) -> KnowledgeArea:
        return KnowledgeArea.objects.get(pk=pk)

    @staticmethod
    def delete(pk: int):
        KnowledgeArea.objects.filter(pk=pk).delete()

    @staticmethod
    def update(serializer):
        instance = serializer.instance
        data = serializer.validated_data

        instance.content = data["content"]
        instance.subject = data["subject"]
        instance.save()
