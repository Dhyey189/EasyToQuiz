from django.contrib import admin
from django.urls import path,include
from . import views
from django.conf.urls import url
from .views import response_data,responses,view_response,change_data
urlpatterns=[
    path('responses',views.responses,name='responses'),
    path('responses_data',views.responses_data,name='responses_data'),
    path('view_response',views.view_response,name='view_response'),
    path('change_data', views.change_data, name='change_data'),
]