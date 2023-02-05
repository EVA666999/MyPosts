from django.db import models


class Contact(models.Model):
    name = models.CharField(max_length=100, verbose_name="Имя")
    email = models.EmailField(verbose_name="Емаил")
    subject = models.CharField(max_length=100, verbose_name="Субьект")
    body = models.TextField(verbose_name="Тело")
    is_answered = models.BooleanField(default=False, verbose_name="Ответ")