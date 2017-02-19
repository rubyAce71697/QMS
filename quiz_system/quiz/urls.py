from django.conf.urls import url,include
from django.contrib import admin

from django.contrib.auth import views as auth_views
from .views import register,home,detail,attempt,submit,user_login

urlpatterns = [
    url(r'^register/$', register,name='register'),
    url(r'^login/$',user_login,   name='login'),
    url(r'^$',user_login,  name='login'),

    url(r'^home/',home ,name='home'),
    url(r'^logout/$',auth_views.logout,  {'next_page':'/quiz/'}, name='logout'),
    url(r'^detail/(?P<test_id>[0-9]+)/$', detail, name='detail'),
    url(r'^attempt/(?P<test_id>[0-9]+)/$', attempt, name='attempt'),
    url(r'^attempt/(?P<test_id>[0-9]+)/submit$', submit, name='submit'),
]

