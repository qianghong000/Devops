# Generated by Django 2.2 on 2019-08-26 08:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Deploy',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=40, verbose_name='项目名称')),
                ('version', models.CharField(max_length=40, verbose_name='上线版本')),
                ('version_desc', models.CharField(max_length=100, verbose_name='版本描述')),
                ('update_detail', models.TextField(verbose_name='更新详情')),
                ('status', models.IntegerField(choices=[(0, '申请'), (1, '审核'), (2, '上线'), (3, '取消上线')], default=0, verbose_name='上线状态')),
                ('apply_time', models.DateTimeField(auto_now_add=True, verbose_name='申请时间')),
                ('deploy_time', models.DateTimeField(auto_now=True, verbose_name='上线完成时间')),
                ('applicant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='applicant', to=settings.AUTH_USER_MODEL, verbose_name='申请人')),
                ('handler', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='handler', to=settings.AUTH_USER_MODEL, verbose_name='最终处理人')),
                ('reviewer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reviewer', to=settings.AUTH_USER_MODEL, verbose_name='审核人')),
            ],
        ),
    ]
