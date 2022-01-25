# -*- coding:utf-8 -*-
# author: SM0558
# datetime: 2022/1/12 16:21
# software: PyCharm

from django.urls import path

from . import views

# 正在部署的应用的名称
app_name = 'blog'
urlpatterns = [
    path('list/', views.blog_list, name='blog_list'),
    path('blog-detail/<int:id>/', views.blog_detail, name='blog_detail'),
    path('blog-create/', views.blog_create, name='blog_create'),
    path('blog-delete/<int:id>/', views.blog_delete, name='blog_delete'),
    path('blog-update/<int:id>/', views.blog_update, name="blog_update"),
]
