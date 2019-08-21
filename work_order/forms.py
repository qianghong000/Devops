#!/usr/bin/python
# author: qsh

from django import forms
from users.models import UserProfile

class WorkOrderApplyForm(forms.Form):
    # 定义sa组成员（筛选ops组下成员）
    assign_sa = UserProfile.objects.filter(groups__name='ops').values_list('id', 'name_cn')
    # 标题
    title = forms.CharField(required=True,
                           max_length=10, error_messages={'required':'标题不能为空', 'max_length':'最多10个字符'},
                           widget=forms.TextInput(attrs={'class': 'form-control','placeholder': '工单标题'}))
    # 工单内容
    order_contents = forms.CharField(required=True,
                                    error_messages={'required': '工单内容不能为空',},
                                    widget=forms.Textarea(attrs={'class': 'form-control',
                                                                  'rows': 8, 'placeholder': '工单详细内容'}))
    # 选择指派人
    assign = forms.ChoiceField(widget=forms.Select(attrs={'class': 'assign-to form-control'}, choices=assign_sa))
    orderfiles = forms.FileField(required=False)

    # 知识点： 指派给用户的时候，如果用户更新了 指派的下拉列表也得更新
    def __init__(self, *args, **kwargs):
        super(WorkOrderApplyForm, self).__init__(*args, **kwargs)
        # 指派人下拉框（ops组下成员）
        self.fields['assign'].choices = UserProfile.objects.filter(groups__name='ops').values_list('id', 'name_cn')

class WorkOrderResultForm(forms.Form):
    result_desc = forms.CharField(widget=forms.Textarea(), required=True)