# Generated by Django 2.2.16 on 2023-02-15 08:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0004_auto_20230215_1102'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='title',
            field=models.CharField(default=1, max_length=224),
            preserve_default=False,
        ),
    ]
