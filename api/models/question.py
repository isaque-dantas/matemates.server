from django.db import models

from api.models.entry import Entry


class QuestionManager(models.Manager):
    def create(self, questions):
        return self.bulk_create(questions)

class Question(models.Model):
    statement = models.CharField(max_length=256, blank=False)
    answer = models.CharField(max_length=256, blank=False)

    entry = models.ForeignKey(Entry, on_delete=models.CASCADE, related_name="questions")
    objects = QuestionManager()
