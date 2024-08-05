from django.db import models


class KnowledgeAreaManager(models.Manager):
    @staticmethod
    def create(**kwargs):
        print(f'trying to create knowledge area: <{kwargs["content"]} | {kwargs["subject"]}>')

        knowledge_area = KnowledgeArea(content=kwargs['content'], subject=kwargs['subject'])
        knowledge_area.save()


class KnowledgeArea(models.Model):
    content = models.CharField(max_length=128, blank=False, unique=True)
    subject = models.CharField(max_length=128, blank=False)

    objects = KnowledgeAreaManager()

    def __repr__(self):
        return f'<KnowledgeArea {self.content} | {self.subject}>'
