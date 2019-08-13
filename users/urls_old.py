#!/usr/bin/python
# author: qsh

from django.urls import path,re_path
from . import views_old,views1

app_name = 'users-old'
urlpatterns = [
    path("", views1.LoginView.as_view(), name='index'),
    path("login/", views_old.login, name='login'),
    #path("login/", views1.LoginView.as_view(), name='login'),
    path('userlist/',views_old.userlist, name='user_list'),
    path('logout/',views_old.logout, name='logout'),
]



