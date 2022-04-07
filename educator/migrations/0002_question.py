# Generated by Django 3.2 on 2021-05-11 09:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('educator', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quizid', models.PositiveIntegerField()),
                ('question', models.CharField(max_length=500)),
                ('numofques', models.PositiveIntegerField()),
                ('correctoption', models.PositiveIntegerField()),
                ('option1', models.CharField(max_length=150)),
                ('option2', models.CharField(max_length=150)),
                ('option3', models.CharField(blank=True, max_length=150)),
                ('option4', models.CharField(blank=True, max_length=150)),
                ('option5', models.CharField(blank=True, max_length=150)),
            ],
        ),
    ]
