from django.shortcuts import render,redirect
from django.views.generic import TemplateView
from django.http import HttpResponseRedirect
from django.views import generic
from django.template.context_processors import csrf
from .models import quiz_data,Question_data,option_data
from django.contrib.auth.models import User, auth
from django.contrib.auth import logout
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
import uuid


def createquiz(request):
    return render(request, "createquiz.html")

def quiznext2(request):
    if request.method == 'POST':
        context = {"QuizID" : request.POST.get('QuizID','')}
        return render(request,"quiznext2.html",context)
    else:
         return HttpResponseRedirect('/EasyToQuiz')   

def generate_quizid():
    return uuid.uuid4().hex[:6].upper()

def savingquiz(request):
        if request.method == 'POST':
            quizid=0
            quiz_id=""
            while 1:
                quiz_id=generate_quizid()
                exist = quiz_data.objects.raw("SELECT * from CreateQuiz_quiz_data WHERE quizid=%s", [quiz_id])
                if len(exist)==0:
                    break
            quiztitle=request.POST.get('title','')
            quizdescription=request.POST.get('description','')
            mail=request.POST.get('smail','')
            u_id =int(request.POST.get('u_id',''))
            q = quiz_data(quizid=quiz_id ,quiztitle=quiztitle , description=quizdescription ,username_id=u_id)
            q.save()
            array2=request.POST.get('array2','').split(",")
            array=request.POST.get('array','').split(",")
            for i in range(0,int(request.POST.get('x',''))):
                if array2[i+1]=='1':
                    questiontitle=request.POST.get('QuestionTitle-'+str(i+1),'')
                    questiontype=False
                    quizid=q.id
                    Q = Question_data(qtitle=questiontitle,qtype=questiontype,quizid_id=quizid)
                    Q.save()
                    for j in range(1,int(array[i+1])+1):
                        option = request.POST.get("option-"+str(i+1)+"-"+str(j))
                        if option:
                            questionid=Q.id
                            op = option_data(option=option,questionid_id=questionid,quizid_id=quizid)
                            op.save()
            subject = str(quiztitle)
            message = 'You have successfully created Quiz on EasyToQuiz!\nQuiz information is as follow:\nQuiz Title: '+str(quiztitle)+'\nQuizID: '+str(q.quizid)+'\n\nThank You, for spending your valuable time on EasyToQuiz!'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [mail,]
            send_mail( subject, message, email_from, recipient_list )
            context = {"QuizID" : q.quizid }
            return render(request, "quiznext.html",context)

        else:
            return HttpResponseRedirect('/EasyToQuiz')
# Create your views here.
