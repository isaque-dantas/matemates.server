from django.db import models

from api.models.user import User


class InvitedEmail(models.Model):
    email = models.EmailField(max_length=128, unique=True, blank=False)
    user_who_invited = models.ForeignKey(User, on_delete=models.CASCADE)
