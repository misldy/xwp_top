from django.contrib import admin

from .models import MessageLog

# 注册ArticlePost到admin中
admin.site.register(MessageLog)
