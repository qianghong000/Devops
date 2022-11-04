from django.db import models
from users.models import UserProfile

class Deploy(models.Model):
    STATUS = (
        (0, '申请'),
        (1, '审核'),
        (2, '上线'),
        (3, '取消上线'),
    )

    name = models.CharField(max_length=40,verbose_name='项目名称')
    version = models.CharField(max_length=40, verbose_name='上线版本')
    version_desc = models.CharField(max_length=100, verbose_name='版本描述')
    applicant = models.ForeignKey(UserProfile,verbose_name='申请人',on_delete=models.CASCADE,related_name='applicant')
    reviewer = models.ForeignKey(UserProfile, verbose_name='审核人', on_delete=models.CASCADE, blank=True, null=True,related_name="reviewer")
    handler = models.ForeignKey(UserProfile, verbose_name='最终处理人', blank=True, null=True,on_delete=models.CASCADE, related_name='handler')
    update_detail = models.TextField(verbose_name='更新详情')
    status = models.IntegerField(default=0, choices=STATUS, verbose_name='上线状态')
    apply_time = models.DateTimeField(auto_now_add=True, verbose_name='申请时间')
    deploy_time = models.DateTimeField(auto_now=True, verbose_name='上线完成时间')

