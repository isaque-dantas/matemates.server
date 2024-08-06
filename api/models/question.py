from django.db import models

from api.models.entry import Entry


class QuestionManager(models.Manager):
    @staticmethod
    def create(**kwargs):
        question =

    def create_all(self, questions_data: list):
        for question_data in questions_data:
            self.create(**question_data)


class Question(models.Model):
    statement = models.CharField(max_length=256, blank=False)
    answer = models.CharField(max_length=256, blank=False)
    explanation = models.CharField(max_length=256, blank=True)
    order = models.IntegerField(blank=False)

    entry = models.ForeignKey(Entry, on_delete=models.CASCADE)

    objects = QuestionManager()
