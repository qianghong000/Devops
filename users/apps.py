from django.apps import AppConfig


class UsersConfig(AppConfig):
    name = 'users'
    verbose_name = '用户管理'    #这里给APP加中文别名


class UserGroupsConfig(AppConfig):
    name = 'usergroups'
    verbose_name = '用户组管理'    #这里给APP加中文别名
