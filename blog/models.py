import django.utils.timezone
from django.db import models

# 导入内建的User模型
from django.contrib.auth.models import User


# 博客数据模型
class BlogPost(models.Model):
    # 博主
    blogger = models.ForeignKey(User, on_delete=models.CASCADE)

    # 博客标题
    title = models.CharField(max_length=200)

    # 博客内容
    body = models.TextField()

    # 创建时间
    created = models.DateTimeField(default=django.utils.timezone.now)

    # 更新时间
    updated = models.DateTimeField(auto_now=True)

    # 浏览次数
    total_views = models.PositiveIntegerField(default=0)

    # 内部类，给model定义元数据
    class Meta:
        # ordering 指定模型返回的数据的排列顺序
        # ’-created‘ 表明数据应该以倒叙排列
        ordering = ('-created',)

    def __str__(self):
        return self.title
