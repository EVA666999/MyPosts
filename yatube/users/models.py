from django.contrib.auth.models import User
from django.db import models


class Contact(models.Model):
    name = models.CharField(max_length=100, verbose_name="Имя")
    email = models.EmailField(verbose_name="Емаил")
    subject = models.CharField(max_length=100, verbose_name="Субьект")
    body = models.TextField(verbose_name="Тело")
    is_answered = models.BooleanField(default=False, verbose_name="Ответ")


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    profile_picture = models.ImageField(blank=True)
