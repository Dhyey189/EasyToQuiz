from django.shortcuts import render,redirect
from django.views.generic import TemplateView
from django.http import HttpResponseRedirect
from django.views import generic
from django.template.context_processors import csrf
from .models import response_data
from userlogin.models import user_signup
from django.contrib.auth.models import User, auth
from django.contrib.auth import logout
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
import uuid
from CreateQuiz.models import quiz_data,Question_data,option_data


def quizdata(request):
    return render(request, "quizdata.html")

def quiz(request):
    if request.method == 'POST':
        user_id=request.POST.get('user_id','')
        quizid=request.POST.get('quizcode','')
        x = quiz_data.objects.raw("SELECT * from CreateQuiz_quiz_data WHERE quizid=%s", [quizid])
        if len(x)==1:
            
                exist = response_data.objects.raw("SELECT * from GiveQuiz_response_data WHERE userid_id=%s and quizid_id=%s", [user_id, x[0].id])
                if len(exist)!=0:
                    return render(request, "submitquiz.html")
                elif x[0].response_status:
                    Q_data=Question_data()
                    for y in x:
                        title=y.quiztitle
                        discription=y.description
                    questions = Question_data.objects.raw("SELECT * from CreateQuiz_question_data WHERE quizid_id=%s", [x[0].id])
                    option = option_data.objects.raw("SELECT * from CreateQuiz_option_data WHERE quizid_id=%s", [x[0].id])
                    context = {"questions":questions , "options":option, "title":title, "description": discription}
                    return render(request, "quiz.html",context)
                else:
                    context = {"mymessage":"This quiz is no longer accepting response, try to contact owner of the Quiz!!" }
                    return render(request, "quizdata.html",context)    
        else:
            context = {"mymessage":"No Quiz available for this ID" }
            return render(request, "quizdata.html",context)
    else:
        return HttpResponseRedirect('/EasyToQuiz')

def submit(request):
    if request.method == 'POST':
        quizid=request.POST.get('quiz_id','')
        questions = Question_data.objects.raw("SELECT * from CreateQuiz_question_data WHERE quizid_id=%s", [quizid])
        userid = int(request.POST.get('u_id',''))
        for question in questions:
            selected_option=request.POST.get('answer'+str(question.id),'1')
            qid=question.id
            response = response_data( answer_id=selected_option, questionid_id=qid, quizid_id=quizid, userid_id=userid)
            response.save()
        return render(request, "submitquiz.html")
    else:
        return HttpResponseRedirect('/EasyToQuiz')

def btw_submit(request):
    if request.method == 'POST':
        return render(request,"submit.html")
    else:
         return HttpResponseRedirect('/EasyToQuiz') 
# Create your views here.
