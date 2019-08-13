#!/usr/bin/python
# author: qsh

from django.urls import path,re_path
from . import views

app_name = 'hello'
urlpatterns = [
    # 请求方式 http://127.0.0.1:8000/hello/hello/?year=2019&month=10
    path('index/', views.index, name='index'),
    # get不带参数；get通过？加参数；post请求的url格式如下
    path('hello/',views.index2, name='hello'),
    path('login/',views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('index2/',views.user, name='user'),
    path('list/',views.list, name='list'),
    # 关键字传参数 （?<参数名>参数类型）--视图中直接通过参数名获取值(最常用)
    # 请求方式 http://127.0.0.1:8000/hello/hello/2019/08/
    re_path('hello/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/', views.index2, name='index2'),
    re_path('user/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/', views.user, name='user'),
]


