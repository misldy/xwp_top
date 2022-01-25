# -*- coding:utf-8 -*-
# author: SM0558
# datetime: 2022/1/20 15:30
# software: PyCharm
from django.urls import path
from . import views

app_name = 'message_logs'

urlpatterns = [
    path('post-message_log/', views.post_message_log, name='post_message_log'),
]
