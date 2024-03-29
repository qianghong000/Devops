"""reboot URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include,re_path
from .settings import MEDIA_ROOT
from django.views.static import serve

urlpatterns = [
    #访问根路径走 users.urls 路由规则
    path('', include('users.urls')),
    path("workorder/", include('work_order.urls')),
    path("deploy/", include('deploy.urls')),
    re_path("media/(?P<path>.*)", serve, {"document_root": MEDIA_ROOT}),
    #path('', include('users.urls1')),
    path('admin/', admin.site.urls),
    path('hello/', include('hello.urls'), name="hello"),
    path('users/', include('users.urls_old'), name="users"),
]
