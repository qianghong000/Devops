#!/usr/bin/python
# author: qsh
# 权限管理页面

from django.http import  HttpResponseRedirect, JsonResponse, QueryDict, Http404
# 权限&&认证
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import View, ListView, DetailView
from django.contrib.auth.models import  Group,Permission

# 查询数据库
from django.db.models import Q

# models 数据库定义的类
from users.models import UserProfile
# 分页
from pure_pagination.mixins import PaginationMixin
from django.shortcuts import render

# 导入forms表单验证
from users.forms import UserProfileForm,UserUpdateForm

# 权限管理列表
class PowerListView(LoginRequiredMixin, PaginationMixin, ListView):
    model = Permission  #(此属性是必须的)指定了数据表。他的功能相当于取出了Group 中所有数据。
    template_name = "users/power/power_list.html"
    context_object_name = "powerlist"    # 往前端传递的变量
    paginate_by = 10
    keyword = ''
    login_url = '/login/'

    def get_queryset(self):  # 继承父类 ListView(BaseListView)，查询字段
        # 变量属性见图（应用场景：列表页）
        queryset = super(PowerListView, self).get_queryset()
        self.keyword = self.request.GET.get('keyword', '')
        if self.keyword:
            queryset = queryset.filter(name__icontains = self.keyword)
        # 后端将 queryset 传递给前端
        return queryset

    # 效果见图1
    def get_context_data(self, **kwargs):   # 继承父类 ListView(BaseListView)，把数据返回给上下文
        context = super(PowerListView,self).get_context_data(**kwargs)
        context['keyword'] = self.keyword
        # print(context)  #{'paginator': <pure_pagination.paginator.Paginator object at 0x10f377f60>, 'page_obj': <Page 1 of 3>, 'is_paginated': True, 'object_list': <QuerySet [<Group: admin>, <Group: test1>, <Group: test2>]>, 'grouplist': <QuerySet [<Group: admin>, <Group: test1>, <Group: test2>]>, 'view': <users.roles.GroupListView object at 0x10f2a0e80>, 'keyword': ''}
        #print(self.model)
        return context

