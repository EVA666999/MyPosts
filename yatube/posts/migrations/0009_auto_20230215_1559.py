# Generated by Django 2.2.16 on 2023-02-15 12:59

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('posts', '0008_auto_20230215_1550'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='dislike',
            field=models.ManyToManyField(related_name='disliked_posts', to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='Dislike',
        ),
    ]