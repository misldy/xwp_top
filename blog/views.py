from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import BlogPost
import markdown
from .forms import BlogPostFrom
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator


# 文章列表视图
def blog_list(reuqest):
    # 取出所有文章
    blogs_list = BlogPost.objects.all()
    # 根据GET请求中查询条件
    # 返回不同排序的对象数组
    if reuqest.GET.get('order') == 'total_views':
        blogs_list = BlogPost.objects.all().order_by('-total_views')
        order = 'total_views'
    else:
        blogs_list = BlogPost.objects.all()
        order = 'normal'
    # 每页显示一篇文章
    paginator = Paginator(blogs_list, 3)
    # 获取url中的页码
    page = reuqest.GET.get('page')
    # 将导航对象相应的页码内容返回给blogs
    # blogs = paginator.get_page(page)
    blogs = paginator.get_page(page)
    # 添加Markdown功能
    for blog in blogs:
        blog.body = markdown.markdown(blog.body,
                                      extensions=['markdown.extensions.extra', 'markdown.extensions.codehilite', ])
    # 取出需要传递的模板对象
    context = {'blogs': blogs, 'order': order}
    # render方式返回context对象
    return render(reuqest, 'blog/list.html', context)


# 文章详情视图
def blog_detail(request, id):
    blog = BlogPost.objects.get(id=id)
    blog.total_views += 1
    blog.save(update_fields=['total_views'])
    md = markdown.Markdown(
        extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            'markdown.extensions.toc',
        ]
    )
    blog.body = md.convert(blog.body)
    context = {'blog': blog, 'toc': md.toc}
    return render(request, 'blog/detail.html', context)


# 增加文章视图
@login_required(login_url='/userprofile/login')
def blog_create(request):
    if request.method == "POST":
        blog_post_form = BlogPostFrom(data=request.POST)
        if blog_post_form.is_valid():
            new_blog = blog_post_form.save(commit=False)
            # new_blog.blogger = User.objects.get(request.user.id)
            new_blog.blogger_id = request.user.id
            new_blog.save()
            return redirect('blog:blog_list')
        else:
            return HttpResponse("表单内容有误,请重新填写")

    else:
        blog_post_form = BlogPostFrom()
        context = {'blog_post_form': blog_post_form}
        return render(request, 'blog/create.html', context)


def blog_delete(request, id):
    blog = BlogPost.objects.get(id=id)
    blog.delete()
    return redirect('blog:blog_list')


def blog_update(request, id):
    blog = BlogPost.objects.get(id=id)
    if request.method == "POST":
        blog_post_form = BlogPostFrom(data=request.POST)
        if blog_post_form.is_valid():
            blog.title = request.POST['title']
            blog.body = request.POST['body']
            blog.save()
            return redirect("blog:blog_detail", id=id)
        else:
            return HttpResponse("表单内容有误,请重新填写")
    else:
        blog_post_form = BlogPostFrom()
        context = {'blog': blog, 'blog_post_form': blog_post_form}
        return render(request, 'blog/update.html', context)
