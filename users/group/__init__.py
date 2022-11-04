#!/usr/bin/python
# author: qsh
# 角色管理页面

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
from django.shortcuts import render,reverse, redirect

# 导入forms表单验证
from users.forms import UserProfileForm,UserUpdateForm


def grouplist(request):
    # 从.models 中获取表中所有数据
    groups = Group.objects.all()
    # users = UserProfile.objects.all().values('id', 'username', 'name_cn', 'phone')
    print(groups, type(groups))
    return render(request, 'users/group/usergroup_list.html', {'grouplist': groups})

# 角色管理列表
class GroupListView(LoginRequiredMixin, PaginationMixin, ListView):
    model = Group  #(此属性是必须的)指定了数据表。他的功能相当于取出了Group 中所有数据。
    # template_name = "user/userlist.html"
    template_name = "users/group/group_list.html"
    context_object_name = "grouplist"    # 往前端传递的变量
    paginate_by = 5
    keyword = ''
    login_url = '/login/'  # 用户没有通过或者权限不够时跳转的地址，默认是 settings.LOGIN_URL.

    def get_queryset(self):  # 继承父类 ListView(BaseListView)，查询字段
        # 变量属性见图（应用场景：列表页）
        queryset = super(GroupListView, self).get_queryset()
        self.keyword = self.request.GET.get('keyword', '')
        if self.keyword:
            queryset = queryset.filter(name__icontains = self.keyword)
        # 后端将 queryset 传递给前端
        return queryset
    '''
    # 第一种方式通过后端获取权限和用户数据
    def get_context_data(self, **kwargs):
        context = super(RoleListView, self).get_context_data(**kwargs)
        context['keyword'] = self.keyword
        rolelist = []
        for role in context["object_list"]:
            role_info = {}
            role_info['id'] = role.id
            role_info['name'] = role.name
            role_info['member'] = role.user_set.all()
            role_info['permissions'] = role.permissions.all()
            rolelist.append(role_info)
        context['rolelist'] = rolelist
        return context
    '''

    # 第二种方式：交给前端获取数据去处理
    def get_context_data(self, **kwargs):   # 继承父类 ListView(BaseListView)，把数据返回给上下文
        context = super(GroupListView,self).get_context_data(**kwargs)
        context['keyword'] = self.keyword
        # print(context)  #{'paginator': <pure_pagination.paginator.Paginator object at 0x10f377f60>, 'page_obj': <Page 1 of 3>, 'is_paginated': True, 'object_list': <QuerySet [<Group: admin>, <Group: test1>, <Group: test2>]>, 'grouplist': <QuerySet [<Group: admin>, <Group: test1>, <Group: test2>]>, 'view': <users.group.GroupListView object at 0x10f2a0e80>, 'keyword': ''}
        #print(self.model)
        return context

    # 添加角色
    def post(self, request):
        _userForm = UserProfileForm(request.POST)
        if _userForm.is_valid():
            try:
                _userForm.cleaned_data['password'] = make_password("12345678")
                _userForm.cleaned_data['is_active'] = True
                data = _userForm.cleaned_data
                self.model.objects.create(**data)
                res = {'code': 0, 'result': '添加用户成功。'}
            except:
                #logger.error("create user  error: %s" % traceback.format_exc())
                res = {'code': 1, 'errmsg': '添加用户失败。'}
        else:
            # 获取自定义的表单错误的两种常用方式
            print(_userForm.errors)
            # <ul class="errorlist">
            #   <li>phone<ul class="errorlist"><li>手机号码非法</li></ul></li>
            #   <li>username<ul class="errorlist"><li>已存在一位使用该名字的用户。</li></ul></li>
            # </ul>
            print(_userForm.errors.as_json())
            # {"phone": [{"message": "\u624b\u673a\u53f7\u7801\u975e\u6cd5", "code": "invalid"}],
            # "username": [{"message": "\u5df2\u5b4f7f\u7528\u8be5\u540d\u5b57\u7684\u7528\u6237\u3002",
            # "code": "unique"}]}
            if _userForm.errors.get('phone'):
                print(_userForm.errors['phone'][0])      # 手机号码非法
            if _userForm.errors.get('username'):
                print(_userForm.errors['username'][0])   # 已存在一位使用该名字的用户
            res = {'code': 1, 'errmsg': _userForm.errors.as_json()}
        return JsonResponse(res, safe=True)

    #删除用户
    def delete(self, request):
        data = QueryDict(request.body).dict()
        print(data)
        pk = data.get('id')
        try:
            user = self.model.objects.filter(pk=pk)
            user.delete()
            res = {'code': 0, 'result': '删除用户成功'}
        except:
            # logger.error("delete user  error: %s" % traceback.format_exc())
            res = {'code': 1, 'errmsg': '删除用户失败'}
        return JsonResponse(res, safe=True)

class GroupDetailView(LoginRequiredMixin, DetailView):
    """
    角色更新
    """
    model = Group  # object =  UserProfile.objects.filter(pk=pk)
    template_name = "users/group/group_edit.html"
    context_object_name = "grouplist"  # user = object

    """
    更新用户信息
    """

    def post(self, request, **kwargs):
        pk = kwargs.get("pk")
        print(pk)
        data = QueryDict(request.body).dict()
        print(data)  # {'id': '7', 'username': 'aa', 'name_cn': 'bb', 'phone': '13305779168'}
        _userForm = UserUpdateForm(request.POST)
        if _userForm.is_valid():
            try:
                self.model.objects.filter(pk=pk).update(**data)
                res = {'code': 0, "next_url": reverse("users:user_list"), 'result': '更新用户成功'}
            except:
                res = {'code': 1, "next_url": reverse("users:user_list"), 'errmsg': '更新用户失败'}
                # logger.error("update user  error: %s" % traceback.format_exc())
        else:
            # 获取所有的表单错误
            print(_userForm.errors)
            res = {'code': 1, "next_url": reverse("users:user_list"), 'errmsg': _userForm.errors}
        return render(request, settings.JUMP_PAGE, res)


