from django.db import models
from django.contrib.auth.models import User, auth
from CreateQuiz.models import *
from userlogin.models import *

class response_data(models.Model):
    questionid = models.ForeignKey("CreateQuiz.Question_data",on_delete=models.CASCADE)
    answer = models.ForeignKey("CreateQuiz.option_data",on_delete=models.CASCADE)
    quizid = models.ForeignKey("CreateQuiz.quiz_data",on_delete=models.CASCADE)
    userid = models.ForeignKey(User,on_delete=models.CASCADE)
# Create your models here.
