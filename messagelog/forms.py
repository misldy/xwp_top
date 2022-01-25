# -*- coding:utf-8 -*-
# author: SM0558
# datetime: 2022/1/20 15:11
# software: PyCharm
from django import forms
from messagelog.models import MessageLog


class MessageLogForm(forms.ModelForm):
    class Meta:
        model = MessageLog
        fields = ['body']
