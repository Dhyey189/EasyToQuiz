from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url


urlpatterns = [
    path('admin/', admin.site.urls),
    path('EasyToQuiz/', include('userlogin.urls'), name='EasyToQuiz'),
    path('EasyToQuiz/', include('CreateQuiz.urls'), name='EasyToQuiz-create-quiz'),
    path('EasyToQuiz/', include('GiveQuiz.urls'), name='EasyToQuiz-give-quiz'),
    path('EasyToQuiz/', include('ShowResponses.urls'), name='EasyToQuiz-show-responses')
]
