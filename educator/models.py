from django.db import models

# Create your models here.
class quiz(models.Model):
    uid=models.PositiveIntegerField()
    quizname=models.CharField(max_length=250)
    quizdesc=models.CharField(max_length=500)
    quizstatus=models.BooleanField(default=False, editable=False)
    creationdate=models.DateField()
    creationtime=models.TimeField()
    attempts=models.PositiveIntegerField(default=0)
class question(models.Model):
    quizid=models.PositiveIntegerField()
    question=models.CharField(max_length=500)
    numofques=models.PositiveIntegerField()
    correctoption=models.PositiveIntegerField()
    option1=models.CharField(max_length=150)
    option2=models.CharField(max_length=150)
    option3=models.CharField(max_length=150, null=True)
    option4=models.CharField(max_length=150, null=True )
    option5=models.CharField(max_length=150, null=True)
class responser(models.Model):
    quizid=models.PositiveIntegerField()
    name=models.CharField(max_length=250)
    email=models.CharField(max_length=250)
    clientip=models.CharField(max_length=250,null=True)
    substatus=models.BooleanField(default=False, editable=False)
    subdate=models.DateField()
    subtime=models.TimeField()
    score=models.PositiveIntegerField(default=0)
class answers(models.Model):
    uid=models.PositiveIntegerField()
    quesid=models.PositiveIntegerField()
    option=models.PositiveIntegerField()


