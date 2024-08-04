from django.db import models


class KnowledgeAreaManager(models.Model):
    @staticmethod
    def create(**kwargs):
        knowledge_area = KnowledgeArea(content=kwargs['content'], subject=kwargs['subject'])
        knowledge_area.save()


class KnowledgeArea(models.Model):
    content = models.CharField(max_length=128, blank=False, unique=True)
    subject = models.CharField(max_length=128, blank=False)
