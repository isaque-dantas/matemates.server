from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, email: str, username: str, password: str, first_name: str, last_name: str,
                    profile_image_path: str):
        user = self.model(email=self.normalize_email(email), username=username, first_name=first_name,
                          last_name=last_name, profile_image_path=profile_image_path)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email: str, username: str, password: str, first_name: str, last_name: str,
                         profile_image_path: str):
        user = self.create_user(email, username, password, first_name, last_name, profile_image_path)
        user.is_staff()
        user.is_superuser = True
        user.save()
        return user


class User(AbstractBaseUser):
    username = models.CharField(max_length=32, unique=True, blank=False)
    first_name = models.CharField(max_length=64, blank=False)
    last_name = models.CharField(max_length=64, blank=False)
    email = models.EmailField(max_length=128, unique=True, blank=False)
    profile_image_path = models.CharField(max_length=128, blank=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()
    USERNAME_FIELD = 'username'


class InvitedEmail(models.Model):
    email = models.EmailField(max_length=128, unique=True, blank=False)
    user_who_invited = models.ForeignKey(User, on_delete=models.CASCADE)


class Entry(models.Model):
    content = models.CharField(max_length=128, blank=False, unique=True)
    is_validated = models.BooleanField(default=False, blank=False)


class Term(models.Model):
    class Gender(models.TextChoices):
        MALE = ('M', "Masculino")
        FEMALE = ('F', "Feminino")

    class GrammaticalCategory(models.TextChoices):
        SUBSTANTIVE = 'substantivo'
        VERB = 'verbo'
        ADJECTIVE = 'adjetivo'
        NUMERAL = 'numeral'

    content = models.CharField(max_length=64, blank=False, unique=True)
    gender = models.CharField(max_length=16, blank=False, choices=Gender)
    grammatical_category = models.CharField(max_length=16, blank=False, choices=GrammaticalCategory,
                                            default=GrammaticalCategory.SUBSTANTIVE)
    is_main_term = models.BooleanField(default=False, blank=False)
    order = models.IntegerField(blank=False)

    entry = models.ForeignKey(Entry, on_delete=models.CASCADE)


class Image(models.Model):
    path = models.CharField(max_length=128, blank=False, unique=True)
    caption = models.CharField(max_length=256, blank=True)
    order = models.IntegerField(blank=False)

    entry = models.ForeignKey(Entry, on_delete=models.CASCADE)


class Question(models.Model):
    statement = models.CharField(max_length=256, blank=False)
    answer = models.CharField(max_length=256, blank=False)
    explanation = models.CharField(max_length=256, blank=True)
    order = models.IntegerField(blank=False)

    entry = models.ForeignKey(Entry, on_delete=models.CASCADE)


class Syllable(models.Model):
    content = models.CharField(max_length=16, blank=False)
    order = models.IntegerField(blank=False)

    entry = models.ForeignKey(Term, on_delete=models.CASCADE)


class KnowledgeArea(models.Model):
    content = models.CharField(max_length=128, blank=False, unique=True)
    subject = models.CharField(max_length=128, blank=False)


class Definition(models.Model):
    content = models.CharField(max_length=256, blank=False)
    order = models.IntegerField(blank=False)

    entry = models.ForeignKey(Entry, on_delete=models.CASCADE)
    knowledge_area = models.ForeignKey(KnowledgeArea, on_delete=models.CASCADE)
