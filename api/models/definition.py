from django.db import models

from .entry import Entry
from .knowledge_area import KnowledgeArea


class Definition(models.Model):
    content = models.CharField(max_length=256, blank=False)
    order = models.IntegerField(blank=False)

    entry = models.ForeignKey(Entry, on_delete=models.CASCADE)
    knowledge_area = models.ForeignKey(KnowledgeArea, on_delete=models.CASCADE)
