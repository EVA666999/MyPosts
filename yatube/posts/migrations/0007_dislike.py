# Generated by Django 2.2.16 on 2023-02-15 12:34

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('posts', '0006_remove_post_title'),
    ]

    operations = [
        migrations.CreateModel(
            name='Dislike',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('post', models.ManyToManyField(related_name='dislikes', to='posts.Post')),
                ('user', models.ManyToManyField(related_name='dislikes', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Дизлайк',
                'verbose_name_plural': 'Дизлайки',
            },
        ),
    ]