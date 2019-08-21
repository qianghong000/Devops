#!/usr/bin/python
# author: qsh
"""
过滤器

创建 templatetags 包名,下面创建tags py文件；
注意目录结构；
"""

import re
from django import template
register = template.Library()


@register.filter(name='orderfile_name')
def orderfile_name(file_path):
    '''
    截取上传文件的文件名
    上传文件数据库中存放的格式：orderfiles/2019/08/aa.txt
    最终需要的格式：aa.txt
    '''
    # print(file_path)
    file_name = str(file_path).split('/')[-1]
    return file_name
