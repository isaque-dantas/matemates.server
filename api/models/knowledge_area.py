from django.db import models


class KnowledgeAreaManager(models.Manager):
    @staticmethod
    def create(content: str):
        print(f'trying to create knowledge area: <{content}>')

        knowledge_area = KnowledgeArea(content=content)
        knowledge_area.save()

        return knowledge_area


class KnowledgeArea(models.Model):
    content = models.CharField(max_length=128, blank=False, unique=True)

    objects = KnowledgeAreaManager()

    def __repr__(self):
        return f'<KnowledgeArea {self.content}>'
