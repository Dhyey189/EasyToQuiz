from django.contrib import admin
from django.urls import path,include
from . import views
from django.conf.urls import url
from .views import login, userregistration,welcome,logout
urlpatterns=[

    url(r'^login/$', login),
    path('login', views.login, name= 'login'),
    path('signout', views.signout, name= 'signout'),
    url(r'^userregistration/$', userregistration),
    path('userregistration', views.userregistration, name= 'userregistration'),
    path('', views.welcome, name='EasyToQuiz'),

]
