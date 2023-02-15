# Generated by Django 2.2.16 on 2023-02-15 12:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('posts', '0007_dislike'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dislike',
            name='post',
        ),
        migrations.AddField(
            model_name='dislike',
            name='post',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='dislikes', to='posts.Post'),
            preserve_default=False,
        ),
        migrations.RemoveField(
            model_name='dislike',
            name='user',
        ),
        migrations.AddField(
            model_name='dislike',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='dislikes', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
