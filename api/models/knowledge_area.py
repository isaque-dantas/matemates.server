from django.db import models


class KnowledgeAreaManager(models.Manager):
    @staticmethod
    def create(content: str, subject: str):
        print(f'trying to create knowledge area: <{content} | {subject}>')

        knowledge_area = KnowledgeArea(content=content, subject=subject)
        knowledge_area.save()

        return knowledge_area


class KnowledgeArea(models.Model):
    content = models.CharField(max_length=128, blank=False, unique=True)
    subject = models.CharField(max_length=128, blank=False)

    objects = KnowledgeAreaManager()

    def __repr__(self):
        return f'<KnowledgeArea {self.content} | {self.subject}>'
