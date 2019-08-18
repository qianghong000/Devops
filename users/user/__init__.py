#!/usr/bin/python
# author: qsh

from django.http import  HttpResponseRedirect, JsonResponse, QueryDict, Http404
from django.shortcuts import render
from django.urls import reverse

# 权限&&认证
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import View, ListView, DetailView
from django.contrib.auth.models import  Group,User,Permission

# 查询数据库
from django.db.models import Q

### 自定义模块
from django.conf import settings
# models 数据库定义的类
from users.models import UserProfile
# 分页
from pure_pagination.mixins import PaginationMixin

# 导入forms表单验证
from users.forms import UserProfileForm,UserUpdateForm

# 引入密码加密模块
from django.contrib.auth.hashers import make_password

# 第二天：函数的方式
def userlist(request):
    # 从.models 中获取表中所有数据
    users = UserProfile.objects.all()
    #users = UserProfile.objects.all().values('id', 'username', 'name_cn', 'phone')
    print(users,type(users))
    return render(request,'user/list1.html',{'users':users})

# 第三天：类 更简洁的方式
# ListView 主要用在获取某个models的所有数据
class UserListView(LoginRequiredMixin, PaginationMixin, ListView):
    def __init__(self):
        self.model = UserProfile  #(此属性是必须的)指定了数据表。他的功能相当于取出了UserProfile 中所有数据。
        # self.template_name = "user/userlist.html"
        self.template_name = "user/user_list.html"
        self.context_object_name = "userlist"    # 传递的变量
        self.paginate_by = 3    #  分页
        self.keyword = ''
        self.login_url = '/login/' # 用户没有通过或者权限不够时跳转的地址，默认是 settings.LOGIN_URL.
        # 把没通过检查的用户重定向到没有 "next page" 的非登录页面时，把它设置为 None ，这样它会在 URL 中移除。
        self.redirect_field_name = 'redirect_to'

    def get_queryset(self):  # 继承父类
        # 变量属性见图（应用场景：列表页）
        queryset = super(UserListView, self).get_queryset()
        #print(self.request.GET)    #<QueryDict: {'keyword': ['admin']}>
        self.keyword = self.request.GET.get('keyword', '').strip()
        if self.keyword:
            # 查询条件为name_cn|username|phone的查询结果。icontains（大小写不敏感）
            queryset = queryset.filter(Q(name_cn__icontains=self.keyword)|
                                    Q(username__icontains=self.keyword) |
                                       Q(phone__icontains=self.keyword))
        #print(queryset)     # <QuerySet [<UserProfile: admin>]>
        # 后端将 queryset 传递给前端
        return queryset

    # 效果见图1
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(UserListView,self).get_context_data(**kwargs)
        context['keyword'] = self.keyword
        return context

    # 创建用户
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

    """
    删除用户
    """
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

class UserDetailView(LoginRequiredMixin,DetailView):
    """
    用户详情
    """
    model = UserProfile  # object =  UserProfile.objects.filter(pk=pk)
    template_name = "user/user_edit.html"
    context_object_name = "user"  # user = object

    """
    更新用户信息
    """
    def post(self, request, **kwargs):
        print(request.POST)  # <QueryDict: {'id': ['7'], 'username': ['aa'], 'name_cn': ['bb'], 'phone': ['13305779168']}>
        print(kwargs)  # {'pk': '7'}
        print(request.body)  # b'id=7&username=aa&name_cn=bb&phone=13305779168'
        pk = kwargs.get("pk")
        data = QueryDict(request.body).dict()
        print(data)  # {'id': '7', 'username': 'aa', 'name_cn': 'bb', 'phone': '13305779168'}
        _userForm = UserUpdateForm(request.POST)
        if _userForm.is_valid():
            try:
                self.model.objects.filter(pk=pk).update(**data)
                res = {'code': 0, "next_url": reverse("users:user_list"), 'result': '更新用户成功'}
            except:
                res = {'code': 1, "next_url": reverse("users:user_list"), 'errmsg': '更新用户失败'}
                #logger.error("update user  error: %s" % traceback.format_exc())
        else:
            # 获取所有的表单错误
            print(_userForm.errors)
            res = {'code': 1, "next_url": reverse("users:user_list"), 'errmsg': _userForm.errors}
        return render(request, settings.JUMP_PAGE, res)

class ModifyPwdView(LoginRequiredMixin,View):
    """
    重置密码
    """
    def get(self,request):
        uid = request.GET.get('uid',None)
        return render(request,'user/change_passwd.html',{'uid':uid})

    def post(self,request):
        uid = request.POST.get('uid',None)
        pwd1 = request.POST.get('password1','')
        pwd2 = request.POST.get('password2','')
        if pwd1 != pwd2:
            return render(request,"user/change_passwd.html",{"msg":"两次密码输入不一致！"})
        try:
            user = UserProfile.objects.get(pk=uid)
            user.password = make_password(pwd1)
            user.save()
            return HttpResponseRedirect(reverse("users:index"))
        except:
            return render(request,"user/change_passwd.html",{"msg":"密码修改失败！"})

class UserGroupPowerView(LoginRequiredMixin, DetailView):
    """
    更新用户角色及权限
    """
    template_name = 'user/user_group_power.html'
    model = UserProfile
    context_object_name = 'user'

    # 返回所有组、权限，并将当前用户所拥有的组、权限显示
    def get_context_data(self, **kwargs):
        context = super(UserGroupPowerView, self).get_context_data(**kwargs)
        context['user_has_groups'], context['user_has_permissions'] = self._get_user_group_power()
        context['user_not_groups'], context['user_not_permissions'] = self._get_user_not_group_power()
        return context   #{'object': <UserProfile: admin>, 'user': <UserProfile: admin>, 'view': <users.user.UserGroupPowerView object at 0x1097a3a20>, 'user_has_groups': <QuerySet [<Group: admin>]>, 'user_has_permissions': <QuerySet []>, 'user_not_groups': [<Group: test1>, <Group: test2>, <Group: test3>, <Group: test4>, <Group: test5>, <Group: test6>], 'user_not_permissions': [<Permission: admin | 日志记录 | Can add log entry>, <Permission: admin | 日志记录 | Can change log entry>, <Permission: admin | 日志记录 | Can delete log entry>, <Permission: admin | 日志记录 | Can view log entry>, <Permission: auth | 组 | Can add group>, <Permission: auth | 组 | Can change group>, <Permission: auth | 组 | Can delete group>, <Permission: auth | 组 | Can view group>, <Permission: auth | 权限 | Can add permission>, <Permission: auth | 权限 | Can change permission>, <Permission: auth | 权限 | Can delete permission>, <Permission: auth | 权限 | Can view permission>, <Permission: contenttypes | 内容类型 | Can add content type>, <Permission: contenttypes | 内容类型 | Can change content type>, <Permission: contenttypes | 内容类型 | Can delete content type>, <Permission: contenttypes | 内容类型 | Can view content type>, <Permission: sessions | 会话 | Can add session>, <Permission: sessions | 会话 | Can change session>, <Permission: sessions | 会话 | Can delete session>, <Permission: sessions | 会话 | Can view session>, <Permission: users | 用户信息 | Can add 用户信息>, <Permission: users | 用户信息 | Can change 用户信息>, <Permission: users | 用户信息 | Can delete 用户信息>, <Permission: users | 用户信息 | Can view 用户信息>]}

    # 获取当前用户所有组、权限以列表形式返回
    def _get_user_group_power(self):
        pk = self.kwargs.get(self.pk_url_kwarg)
        try:
            user = self.model.objects.get(pk=pk)
            return user.groups.all(), user.user_permissions.all()
        except self.model.DoesNotExist:
            raise Http404

    # 获取当前用户没有的组、权限，以列表形式返回
    def _get_user_not_group_power(self):
        pk = self.kwargs.get(self.pk_url_kwarg)
        try:
            user = self.model.objects.get(pk=pk)
            all_group = Group.objects.all()
            groups = [group for group in all_group if group not in user.groups.all()]
            all_perms = Permission.objects.all()
            perms = [perm for perm in all_perms if perm not in user.user_permissions.all()]
            return groups, perms
        except:
            return JsonResponse([], safe=False)

    def post(self, request, **kwargs):
        group_id_list = request.POST.getlist('groups_selected', [])
        permission_id_list = request.POST.getlist('perms_selected', [])
        pk = kwargs.get("pk")
        try:
            user = self.model.objects.get(pk=pk)
            user.groups.set(group_id_list)
            user.user_permissions.set(permission_id_list)
            res = {'code': 0, 'next_url': reverse("users:user_list"), 'result': '用户角色权限更新成功'}
        except:
            res = {'code': 1, 'next_url': reverse("users:user_list"), 'errmsg': '用户角色权限更新失败'}
            #logger.error("edit  user group pwoer error: %s" % traceback.format_exc())
        return render(request, settings.JUMP_PAGE, res)





