from django.db import models

from api.models import Entry, User


class EntryAccessHistory(models.Model):
    entry = models.ForeignKey(Entry, on_delete=models.CASCADE, related_name='access_history')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='access_history')
    access_moment = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()
