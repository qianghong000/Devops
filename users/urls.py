#!/usr/bin/python
# author: qsh

from django.urls import path, re_path
from . import views_old,views1,views
from . import views,user,roles

app_name = 'users'
urlpatterns = [
    # http://ip:8000/
    path("", views.IndexView.as_view(), name='index'),
    # http://ip:8000/login/
    path("login/", views.LoginView.as_view(), name='login'),
    path("logout/", views.LogoutView.as_view(), name='logout'),
    path("list/", user.userlist, name='user_list'),
    path('userlist/', user.UserListView.as_view(), name = 'user_list'),
    path('grouplist/',roles.GroupListView.as_view(), name='group_list'),
    path('powerlist/', roles.PowerListView.as_view(), name='power_list'),
    # <pk> 既英语单词主键 <Primary key> --> 搜索索引(userid)
    re_path('userdetail/(?P<pk>[0-9]+)?/$', user.UserDetailView.as_view(), name='user_detail'),
    path('modifypasswd/', user.ModifyPwdView.as_view(), name='modify_pwd'),
    re_path('usergrouppower/(?P<pk>[0-9]+)?/$', user.UserGroupPowerView.as_view(), name='user_group_power'),
    # http://ip:8000/logout/
    #path("logout/", views2.LogoutView.as_view(), name='logout'),
]



