from django.db import models

from api.models.entry import Entry
from api.models.knowledge_area import KnowledgeArea

class DefinitionManager(models.Manager):
    def create(self, definitions):
        return self.bulk_create(definitions)

class Definition(models.Model):
    content = models.CharField(max_length=256, blank=False)

    entry = models.ForeignKey(Entry, on_delete=models.CASCADE)
    knowledge_area = models.ForeignKey(KnowledgeArea, on_delete=models.CASCADE)

    objects = DefinitionManager()
