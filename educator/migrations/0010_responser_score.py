# Generated by Django 3.2 on 2021-05-23 11:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('educator', '0009_quiz_attempts'),
    ]

    operations = [
        migrations.AddField(
            model_name='responser',
            name='score',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
