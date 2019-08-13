from django.views.generic import View
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout,decorators
from django.urls import reverse
# CBV应用装饰器， django的bug，不能直接对类进行装饰，必须使用 method_decorator,把装饰器当作参数传进去。
from django.utils.decorators import method_decorator
from django.views.generic import ListView

# 权限&&认证
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import View, ListView, DetailView


# ## 不需要任何验证
# class IndexView(View):
#     """
#     首页
#     """
#
#     def get(self, request):
#         return render(request, 'list1.html')

# ## is_authenticated最原始的认证
# class IndexView(View):
#     """
#     首页
#     """
#
#     def get(self, request):
#         # 判断用户session 是否在数据库存在
#         if not request.user.is_authenticated:
#             return HttpResponseRedirect(reverse("users:login"))
#         else:
#             return render(request, 'list1.html')

# ## login_required验证用户是否登陆
# class IndexView(View):
#     """
#     首页
#     """
#
#     # login_url 用户没有通过测试时跳转的地址，默认是 settings.LOGIN_URL
#     @method_decorator(decorators.login_required(login_url='/login/'))
#     def get(self, request):
#         return render(request, 'list1.html')


## LoginRequiredMixin验证用户
class IndexView(LoginRequiredMixin, View):
    """
    首页
    """
    # 用户没有通过或者权限不够时跳转的地址，默认是 settings.LOGIN_URL.
    login_url = '/login/'
    # 把没通过检查的用户重定向到没有 "next page" 的非登录页面时，把它设置为 None ，这样它会在 URL 中移除。
    redirect_field_name = 'redirect_to'   # http://127.0.0.1:8000/login/?redirect_to=/

    def get(self, request):
        return render(request, 'index.html')


class LoginView(View):
    """
    登录模块
    """

    def get(self, request):
        return render(request, "login.html")

    class LoginView(View):
        """
        登录模块
        """

    def get(self, request):
        return render(request, "login.html")

    def post(self, request):
        username = request.POST.get("username", None)
        password = request.POST.get("password", None)
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                # 默认为当前登录用户创建session
                login(request, user)
                # 登录成功则跳到首页
                #return HttpResponseRedirect('/userlist/')
                # 命名空间的写法
                return HttpResponseRedirect(reverse("users:user_list"))
            else:
                return render(request, "login.html", {"msg": "用户未激活！"})
        else:
            return render(request, "login.html", {"msg": "用户名或密码错误！"})


class LogoutView(View):
    """
    登出功能
    """

    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse("users:login"))

