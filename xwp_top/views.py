# -*- coding:utf-8 -*-
# author: SM0558
# datetime: 2022/1/20 13:38
# software: PyCharm
from django.shortcuts import render


def index(request):
    return render(request, 'indexfile/index.html')
