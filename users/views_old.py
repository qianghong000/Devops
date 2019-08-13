
# Create your views here.
from django.http import HttpResponse, QueryDict, HttpResponseRedirect
from django.shortcuts import render
from django.shortcuts import render
from .models import UserProfile
# 引入密码加密模块
from django.contrib.auth.hashers import make_password
from django.urls import reverse

# 练习一
# def index(request):
#     return HttpResponse("<p>Hello World,Hello, Django</p>")
# 练习二
def index(request):
    # 普通参数的接受方法
    # 方法一、设置默认值的方式获取数据更优雅
    year = request.GET.get("year","2019")
    # 方法二、直接获取数据，没有传值会报错，不建议使用
    month = request.GET["month"]
    return HttpResponse("year is %s,month is %s" %(year,month))

# 推荐写法
def index2(request,**kwargs):
    if request.method == "POST":
        #print(request.method)    #POST
        print(request.body)    #b'year=2019&month=11'
        #print(type(request.body))
        print(QueryDict(request.body).dict())   #{'year': '2019', 'month': '11'}
        #print(type(QueryDict(request.body).dict()))
        print(request.POST)    #<QueryDict: {'year': ['2019'], 'month': ['11']}>
        print(type(request.POST))    #<class 'django.http.request.QueryDict'>

        data = request.POST
        year = data.get('year',2019)
        month = data.get('month',8)
    else:
        print(request)
        print(request.method)
        print(request.META)
        print(request.body)
        print(kwargs)
        year = kwargs.get('year',2019)
        month = kwargs.get('month',8)
    return HttpResponse("year is %s,month is %s" %(year,month))

def user(request,**kwargs):
    if request.method == "POST":
        pass
    else:
        user = {'name':'qsh','age':'18'}

        title = "devops"
        books = ['python','java','php','web']
        people = {'name':'qsh','age':18,'sex':'male'}
        products = [{'pid': 1, 'name': 'iphone'}, {'pid': 2, 'name': 'computer'}, {'pid': 3, 'name': 'TV'}]

    return render(request,'index.html',{'title':title,'books':books,'people':people,'user':user,'products':products})

# 此方法已被封装好,抛弃掉（from django.contrib.auth import authenticate）
def login(request, **kwargs):
    data = ""
    if request.method == "POST":
        username = request.POST.get('username', 'reboot')
        passwd = request.POST.get('password', '123456')
        user = UserProfile.objects.filter(username=username).first()
        print('user:', user,user.password)
        print('make_password',make_password(passwd))
        if user:
            if user.password == make_password(passwd):
                return HttpResponseRedirect("/userlist/")
            else:
                data = "your passwd is wrong"
        else:
            data = "user is not exist"
        return render(request, 'login-old.html', {'data': data})
    if request.method == "GET":
        return render(request, 'login-old.html', {'data': data})


def logout(request,**kwargs):
    return render(request,'login.html')

def list(request,*args,**kwargs):
   users = [
       {'username':'wd','name_cn':'wd','age':18},
       {'username':'ll','name_cn':'ll','age':11},
       {'username':'yy','name_cn':'yy','age':21}
        ]
   return render(request, 'list.html',{'users':users})


def userlist(request):
    # 从.models 中获取表中所有数据
    users = UserProfile.objects.all()
    #users = UserProfile.objects.all().values('id', 'username', 'name_cn', 'phone')
    print(users,type(users))
    return render(request,'list1.html',{'users':users})




