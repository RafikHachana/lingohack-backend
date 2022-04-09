from random import choices
from unicodedata import category
from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
# from .managers import CustomUserManager

class Category(models.Model):
    Id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True, editable=False)
    name = models.TextField()


class Text(models.Model):
    Id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True, editable=False)
    content = models.TextField()

    RUS = 'russian'
    ENG = 'english'

    AVAILABLE_LANGUAGES = [
        (RUS, 'Russian'),
        (ENG, 'English')
    ]

    language = models.CharField(max_length=8, choices=AVAILABLE_LANGUAGES)

    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.content

class Translation(models.Model):
    Id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True, editable=False)
    englishText = models.ForeignKey(Text, on_delete=models.PROTECT, related_name="englishText")
    russianText = models.ForeignKey(Text, on_delete=models.PROTECT, related_name="russianText")

    # class Meta:
    #     constraints = [
    #         models.CheckConstraint(check=models.Q(englishText__language="english"), name="english_text"),
    #         models.CheckConstraint(check=models.Q(russianText__language="russian"), name="russian_text")
    #     ]