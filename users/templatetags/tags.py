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


# 友好的展示组名，见图（过滤器是否加载）
@register.filter(name='group_str2')
def groups_str2(group_list):    # {{ user.groups.all | group_str2 |default:"None" }}: group_list是管道前面(user.groups.all)传值。
    """
    将角色列表转换为str
    """

    # g_list = [group for group in group_list]
    g_list = [group.name for group in group_list]
    print(g_list)
    if len(group_list) < 3:
        return ' '.join([group.name for group in group_list])
    else:
        return '%s ...' % ' '.join([group.name for group in group_list[0:2]])

# 友好的展示是否激活（True -> 是 ;False -> 否）
@register.filter(name='bool2str')
def bool2str(value):
    if value:
        return u'是'
    else:
        return u'否'

# 友好的展示用户名
@register.filter(name='userlist_str2')
def userlist_str2(user_list):
    """
    将角色列表转换为str
    """

    # a = [user for user in user_list]
    # print(a)
    # print(type(user_list),user_list,len(user_list))
    # print(type(len(user_list)),len(user_list))
    # ll = []
    # for user in user_list:
    #     print('user: ',user,'type: ',type(user))
    #     username = str(user)
    #     ll.append(username)
    # print(ll)

    if len(user_list) < 3:
        return ' '.join([str(user) for user in user_list])
    else:
        return '%s ...' % ' '.join([str(user) for user in user_list[0:2]])

# 友好的展示权限
@register.filter(name='perm_str2')
def perm_str2(perm_list):
    ll_perm = []
    for perm in perm_list:
        # 以字符串'|'分割 ;re.M多行匹配，影响 ^ 和 $ ;re.I使匹配对大小写不敏感
        SplitObj = re.split('\s[|+]\s', str(perm), re.M | re.I)
        if SplitObj[2]:
            # 将空格替换为'_'
            SubObj = re.sub(r'\s+', "_", SplitObj[2])
            ll_perm.append(SubObj)

    if len(perm_list) < 3:
        return ' '.join(ll_perm)
    else:
        # return '%s ...' % ' '.join([str(perm) for perm in perm_list[0:2]])
        return '%s ...' % ' '.join(ll_perm[0:2])





