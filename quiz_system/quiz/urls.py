from django.conf.urls import url,include
from django.contrib import admin


from django.contrib.auth import views as auth_views
from .views import register,home,detail,attempt,submit, UserLogin,UserAttempts,Quizes,QuizQuestionsView,QuizAttempts,StudentProfileView
from .views import StudentResponsesSerializerView,UserLogout,LoginTemplateView,HomeTemplateView,ProfileTemplateView
from .views import QuizDetailTemplateView


urlpatterns = [
    
    url(r'^register-rest/$', register,name='register'),
    url(r'^$',LoginTemplateView.as_view(),   name='login_template'),
    
    url(r'^login/$',UserLogin.as_view(),   name='login'),

    #url(r'^home/',home ,name='home'),
    url(r'^logout-rest/$',UserLogout.as_view()),
    url(r'^detail-rest/(?P<test_id>[0-9]+)/$', detail, name='detail'),
    url(r'^detail/(?P<test_id>[0-9]+)/$', QuizDetailTemplateView.as_view(), name='detailtemplate'),
    url(r'^attempt/(?P<test_id>[0-9]+)/$', attempt, name='attempt'),
    url(r'^attempt/(?P<test_id>[0-9]+)/submit$', submit, name='submit'),
    url(r'^userattempts/(?P<pk>[A-Za-z0-9]+)/$',UserAttempts.as_view()),
    #url(r'^userattempts/(?P<pk>[A-Za-z0-9]+)/$',UserAttemptsTemplateView.as_view()),
    url(r'^quizes/',Quizes.as_view(),name='quizes'),
    url(r'^quizquestions/(?P<test_id>[A-Za-z0-9]+)/$',QuizQuestionsView.as_view()),
    url(r'^quizattempts/(?P<student_id>[A-Za-z0-9]+)/$',QuizAttempts.as_view()),
    url(r'^profile-data/$',StudentProfileView.as_view()),
    url(r'^responses/$',StudentResponsesSerializerView.as_view()),
    url(r'^home/',HomeTemplateView.as_view(),name='home'),
    url(r'^profile/',ProfileTemplateView.as_view(),name='profile')
]

