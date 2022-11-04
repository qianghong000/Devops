from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.views.generic import View, TemplateView, ListView, DetailView
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin

# 分页
from pure_pagination import Paginator, PageNotAnInteger
from pure_pagination.mixins import PaginationMixin

# 自定义模块
# from deploy.forms import ApplyForm, DeployForm
from deploy.models import Deploy
from users.models import UserProfile
# from utils.gitlab_api import get_user_projects, get_project_versions
import json, logging, traceback

from .utils.gitlab_api import get_user_projects, get_project_versions

class ApplyView(LoginRequiredMixin, TemplateView):
    """
    申请发布
    """

    template_name = 'deploy/apply.html'

    def get_context_data(self, **kwargs):
        context = super(ApplyView, self).get_context_data(**kwargs)
        context['user_projects'] = get_user_projects(self.request)
        return context

class GetProjectVersionsView(LoginRequiredMixin,View):
    """
    获取指定项目的所有版本
    """

    def get(self,request):
        project_id = request.GET.get('project_id', '').split('/')[0]
        print(project_id) # {'title': 'wf', 'order_contents': 'df', 'assign': '1', 'orderfiles': None}
        tags = get_project_versions(int(project_id))
        tags = [[tag.name,tag.message] for tag in tags]
        return HttpResponse(json.dumps(tags),content_type='application/json')

class ProjectListView(LoginRequiredMixin, View):
    """
    当前登陆用户的项目列表
    """

    def get(self,request):
        my_projects = get_user_projects(request)
        print(my_projects)

