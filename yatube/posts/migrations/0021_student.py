# Generated by Django 2.2.16 on 2023-02-06 14:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0020_delete_employee'),
    ]

    operations = [
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('avatar', models.ImageField(upload_to='uploads/')),
            ],
        ),
    ]
