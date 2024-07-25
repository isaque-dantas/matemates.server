from django.db import models


class User(models.Model):
    first_name = models.CharField(max_length=64, blank=False)
    last_name = models.CharField(max_length=64, blank=False)
    email = models.EmailField(max_length=128, unique=True, blank=False)
    password = models.CharField(max_length=256, blank=False)
    username = models.CharField(max_length=32, unique=True, blank=False)
    phone_number = models.CharField(max_length=32)
    role = models.CharField(max_length=8, blank=False, default="normal")

    profile_image_path = models.CharField(max_length=128)
    invitation_is_pending = models.BooleanField(blank=False, default=False)


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
