#!/usr/bin/python
# author: qsh

from django.urls import path, re_path
from .views import *

app_name = 'workorder'
urlpatterns = [
    path('apply/', WorkOrderApplyView.as_view(), name='apply'),
    path('list/', WorkOrderListView.as_view(), name='list'),
    path('history/', WorkOrderHistoryView.as_view(), name='history'),
    re_path('detail/(?P<pk>[0-9]+)?/$', WorkOrderDetailView.as_view(), name='detail'),

]