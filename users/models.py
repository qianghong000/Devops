from django.db import models
# 此模块 设置自定义用户模型
from django.contrib.auth.models import AbstractUser

# Create your models here.

# UserProfile会被初始化为表名(users_userprofile)
class UserProfile(AbstractUser):
    name_cn = models.CharField('中文名',max_length=30)
    phone = models.CharField('手机',max_length=11,null=True,blank=True)

    class Meta:
        verbose_name = '用户信息'
        verbose_name_plural = verbose_name  # 让后台显示为'用户信息'

        def __str__(self):
            return self.username

# class UserProfile_Groups(models.Model):
    # group_name = models.CharField('用户组',max_length=10)
    #
    #
    # class Meta:   # 页面展示相关类
    #     verbose_name = '用户组信息'
    #     verbose_name_plural = verbose_name  # 让后台显示为'用户信息'








