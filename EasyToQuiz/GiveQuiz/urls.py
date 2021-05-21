from django.contrib import admin
from django.urls import path,include
from . import views
from django.conf.urls import url
from .views import submit,btw_submit,quiz_data,quiz
urlpatterns=[

    path('quizdata', views.quizdata, name='quizdata'),
    path('quiz', views.quiz, name='quiz'),
    path('submit', views.submit, name='submit'),
    path('btw_submit',views.btw_submit,name='btw_submit'),
]