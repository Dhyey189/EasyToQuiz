from django.shortcuts import render,redirect
from django.views.generic import TemplateView
from django.http import HttpResponseRedirect
from django.views import generic
from django.template.context_processors import csrf
from .models import user_signup
from GiveQuiz.models import response_data
from django.contrib.auth.models import User, auth
from django.contrib.auth import logout
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
import uuid
from CreateQuiz.models import quiz_data,Question_data,option_data

def login(request):
    if request.method == 'POST':
        sname = request.POST.get('username', '')
        spass = request.POST.get('password', '')
        user = auth.authenticate(username=sname,password=spass)
        if user is not None:
            auth.login(request,user)
            return HttpResponseRedirect('/EasyToQuiz')
        else:
            messages.error(request,"Username or password invalid")
            return render(request,'login.html')
    else:
        return render(request, "login.html")

def userregistration(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/EasyToQuiz/')
    if request.method == 'POST':
        sname = request.POST.get('username', '')
        semail = request.POST.get('email', '')
        spass = request.POST.get('pass', '')
        spass1 = request.POST.get('cpass','')
        if spass==spass1:
            if User.objects.filter(username=sname).exists():
                messages.error(request,"username already exist.")
                return render(request, "userregistration.html")
            elif User.objects.filter(email=semail).exists():
                messages.error(request,"This email is already connected to an account.")
                return render(request, "userregistration.html")
            else:
                messages.success(request,"Register Successfull, please Login again for confirmation.")
                s = User.objects.create_user(username = sname, email=semail, password=spass)
                subject = 'Welcome to EasyToQuiz'
                message = 'Thank you '+sname+',\nHave a nice journey on EasyToQuiz!'
                email_from = settings.EMAIL_HOST_USER
                recipient_list = [semail,]
                send_mail( subject, message, email_from, recipient_list )
                s.save()
                return HttpResponseRedirect('/EasyToQuiz/login')
        else:
            messages.error(request,"confirm password is not same as password! please check!")
            return render(request, "userregistration.html")
    else:
        return render(request, "userregistration.html")


def welcome(request):
    return render(request, "welcome.html")
    
def signout(request):
    logout(request)
    return redirect("EasyToQuiz")

def responses(request):
    return render(request,"responses.html")

def responses_data(request):
    quizid=request.POST.get("quizcode","")
    userid=request.POST.get("user_id","")
    quiz=quiz_data.objects.raw("SELECT * from CreateQuiz_quiz_data WHERE quizid=%s and username_id=%s", [quizid,userid])
    if len(quiz)==1:
        responses=response_data.objects.raw("SELECT * from userlogin_response_data WHERE quizid_id=%s",[quiz[0].id])
        unique_username_list=[]
        for response in responses:
            user1=User.objects.raw("SELECT DISTINCT * from auth_user WHERE id=%s",[response.userid_id])
            for x in user1:
                if x.id!=int(userid):
                    if x not in unique_username_list:
                        unique_username_list.append(x)
        context = {"responses":responses , "username_list":unique_username_list , "quizid":quiz[0].id,"rs":quiz[0].response_status}
        return render(request, "responses_data.html",context)
    else:
        context = {"mymessage":"Please enter valid Quiz id or this Quiz does not belong to you" }
        return render(request, "responses.html",context)
        
def view_response(request):
    username=request.POST.get("username","")
    user1=User.objects.raw("SELECT * from auth_user WHERE username=%s",[username])
    quizid=(request.POST.get("quizid",""))
    quiz=quiz_data.objects.raw("SELECT * from CreateQuiz_quiz_data WHERE id=%s", [quizid])
    correct_answer_list=[]
    userid=quiz[0].username_id
    correct_response=response_data.objects.raw("SELECT * from userlogin_response_data WHERE quizid_id=%s and userid_id=%s",[quizid,userid])
    for cr in correct_response:
        correct_option=option_data.objects.raw("SELECT * from CreateQuiz_option_data Where id=%s",[cr.answer_id])
        correct_answer_list.append(correct_option[0].option)
    responses=response_data.objects.raw("SELECT * from userlogin_response_data WHERE quizid_id=%s and userid_id=%s",[quizid,user1[0].id])
    
    question_list=[]
    answer_list=[]
    
    for response in responses:
        ques=Question_data.objects.raw("SELECT * from CreateQuiz_question_data WHERE id=%s",[response.questionid_id])
        question_list.append(ques[0])
        answer=option_data.objects.raw("SELECT * from CreateQuiz_option_data WHERE id=%s",[response.answer_id])    
        answer_list.append(answer[0])
    is_answerd=True
    i=0
    if len(correct_response)!=0:
        is_answerd=True
        response_list=zip(question_list,answer_list,correct_answer_list)
        for question,answer,correct_answer in response_list:
            if answer.option==correct_answer:
                i+=1
        response_list=zip(question_list,answer_list,correct_answer_list)
    else:
        is_answerd=False
        response_list=zip(question_list,answer_list)
    x=len(question_list)
    context={"response_list":response_list , "quiz":quiz[0], "total":x , "correct":i,"name":username,"email":user1[0].email, "answered":is_answerd}
    return render(request,"view_response.html",context)

def change_data(request):
    # python.post(/url/responses_data)
    if request.method == 'POST':
        quizid=request.POST.get("quizid","")
        userid=request.POST.get('user_id','')
        
        quiz=quiz_data.objects.raw("SELECT * from CreateQuiz_quiz_data WHERE id=%s", [quizid])
        print(quiz[0].response_status)
        if quiz[0].response_status:
            a=quiz_data.objects.get(pk=quiz[0].id)
            a.response_status=False
            a.save()
        else:
            a=quiz_data.objects.get(pk=quiz[0].id)
            a.response_status=True
            a.save()
        # print(checked)
        context = {"quizcode":quiz[0].quizid, "userid":quiz[0].username_id}
        print(context)
        return render(request,"change_data.html",context)
    