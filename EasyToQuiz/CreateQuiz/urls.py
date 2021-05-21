from django.contrib import admin
from django.urls import path,include
from . import views
from django.conf.urls import url
from .views import createquiz,savingquiz,quiznext2
urlpatterns=[

    # url(r'^login/$', login),
    # path('login', views.login, name= 'login'),
    # path('signout', views.signout, name= 'signout'),
    # url(r'^userregistration/$', userregistration),
    # path('userregistration', views.userregistration, name= 'userregistration'),
    # path('', views.welcome, name='EasyToQuiz'),
    path('createquiz', views.createquiz, name='createnewquiz'),
    path('savingquiz', views.savingquiz, name='savingquiz'),
    # path('quizdata', views.quizdata, name='quizdata'),
    # path('quiz', views.quiz, name='quiz'),
    # path('submit', views.submit, name='submit'),
    path('quiznext2',views.quiznext2,name='quiznext2'),
    # path('btw_submit',views.btw_submit,name='btw_submit'),
    # path('responses',views.responses,name='responses'),
    # path('responses_data',views.responses_data,name='responses_data'),
    # path('view_response',views.view_response,name='view_response'),
    # path('change_data', views.change_data, name='change_data'),

]
