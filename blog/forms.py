# -*- coding:utf-8 -*-
# author: SM0558
# datetime: 2022/1/17 15:57
# software: PyCharm
from django import forms
from .models import BlogPost


# 写文章表单类
class BlogPostFrom(forms.ModelForm):
    class Meta:
        # 数据来源
        model = BlogPost
        # 表单字段
        fields = ('title', 'body')
