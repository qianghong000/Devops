#!/usr/bin/python
# author: qsh
"""
过滤器

创建 templatetags 包名,下面创建tags py文件；
注意目录结构；
"""

from django import template
register = template.Library()


# 友好的展示组名，见图（过滤器是否加载）
@register.filter(name='group_str2')
def groups_str2(group_list):
    """
    将角色列表转换为str
    """
    if len(group_list) < 3:
        return ' '.join([user.name for user in group_list])
    else:
        return '%s ...' % ' '.join([user.name for user in group_list[0:2]])

# 友好的展示是否激活（True -> 是 ;False -> 否）
@register.filter(name='bool2str')
def bool2str(value):
    if value:
        return u'是'
    else:
        return u'否'