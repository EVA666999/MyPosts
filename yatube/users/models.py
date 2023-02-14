from django.db import models
from django.contrib.auth.models import AbstractUser


class Contact(models.Model):
    name = models.CharField(max_length=100, verbose_name="Имя")
    email = models.EmailField(verbose_name="Емаил")
    subject = models.CharField(max_length=100, verbose_name="Субьект")
    body = models.TextField(verbose_name="Тело")
    is_answered = models.BooleanField(default=False, verbose_name="Ответ")


class User(AbstractUser):
    image = models.ImageField(upload_to="posts/", null=True, blank=True)
