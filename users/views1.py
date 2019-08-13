from django.views.generic import View
from django.shortcuts import render
from django.http import  HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse


class IndexView(View):
    """
    首页
    """
    def get(self, request):
        return render(request, 'list1.html')

###### 第一个登录版本
class LoginView(View):

    def get(self,request):
        return render(request,"login.html")

    def post(self, request):
        username = request.POST.get("username", None)
        password = request.POST.get("password", None)
        user = authenticate(username=username, password=password)  # 数据库中密码须为密文
        if user:
            if user.is_active:
                login(request, user)
                #return HttpResponseRedirect('/userlist/')
                return HttpResponseRedirect(reverse("users:userlist"))   # 命名空间的写法
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

