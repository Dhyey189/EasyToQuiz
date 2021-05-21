from django.db import models
from django.contrib.auth.models import User, auth
from userlogin.models import *
class quiz_data(models.Model):
    quiztitle = models.CharField(max_length=40)
    quizid = models.CharField(max_length=6)
    username = models.ForeignKey(User,on_delete=models.CASCADE)
    description = models.CharField(max_length=1000)
    response_status = models.BooleanField(default=True)

class Question_data(models.Model):
    quizid = models.ForeignKey("quiz_data",on_delete=models.CASCADE)
    qtitle = models.CharField(max_length=500)
    qtype = models.BooleanField(default=False)

class option_data(models.Model):
    questionid = models.ForeignKey("Question_data",on_delete=models.CASCADE)
    option = models.CharField(max_length=500)
    quizid = models.ForeignKey("quiz_data",on_delete=models.CASCADE)
# Create your models here.
