from django.conf.urls import url,include
from django.contrib import admin


from django.contrib.auth import views as auth_views
from .views import register,home,detail,attempt,submit, UserLogin,UserAttempts,Quizes,QuizQuestionsView,QuizAttempts,StudentProfileView
from .views import StudentResponsesSerializerView
urlpatterns = [
    url(r'^register/$', register,name='register'),
    #url(r'^login/$',user_login,   name='login'),
    #url(r'^$',user_login,  name='login'),
    url(r'^login/$',UserLogin.as_view(),   name='login'),

    url(r'^home/',home ,name='home'),
    url(r'^logout/$',auth_views.logout,  {'next_page':'/quiz/'}, name='logout'),
    url(r'^detail/(?P<test_id>[0-9]+)/$', detail, name='detail'),
    url(r'^attempt/(?P<test_id>[0-9]+)/$', attempt, name='attempt'),
    url(r'^attempt/(?P<test_id>[0-9]+)/submit$', submit, name='submit'),
    url(r'^userattempts/(?P<pk>[A-Za-z0-9]+)/$',UserAttempts.as_view()),
    url(r'^quizes/',Quizes.as_view()),
    url(r'^quizquestions/(?P<test_id>[A-Za-z0-9]+)/$',QuizQuestionsView.as_view()),
    url(r'^quizattempts/(?P<student_id>[A-Za-z0-9]+)/$',QuizAttempts.as_view()),
    url(r'^profile/$',StudentProfileView.as_view()),
    url(r'^responses/$',StudentResponsesSerializerView.as_view())
]

