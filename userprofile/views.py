# Create your views here.
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import generic
import hashlib

from userprofile.forms import UserLoginForm, UserRegisterForm, ProfileForm
from userprofile.models import Profile
from .models import User


def user_login(request):
    if request.method == "POST":
        user_login_form = UserLoginForm(data=request.POST)
        if user_login_form.is_valid():
            # .cleaned_data洗出合法数据
            data = user_login_form.cleaned_data
            # 检验账号、密码是否正确匹配数据库中的某个用户
            # 如果均匹配则返回这个user对象
            user = authenticate(username=data['username'], password=data['password'])
            if user:
                login(request, user)
                return redirect("blog:blog_list")
            else:
                return HttpResponse("账号或密码输入有误,请重新输入")
        else:
            return HttpResponse("账号或密码输入不合法")
    elif request.method == "GET":
        user_login_form = UserLoginForm()
        context = {'from': user_login_form}
        return render(request, 'userprofile/login.html', context)
    else:
        return HttpResponse("请使用GET或POST请求数据")


def user_register(request):
    if request.method == 'POST':
        user_register_form = UserRegisterForm(data=request.POST)
        if user_register_form.is_valid():
            new_user = user_register_form.save(commit=False)
            # 设置密码
            new_user.set_password(user_register_form.cleaned_data['password'])
            new_user.save()
            # 保存好数据后立即登录并返回博客列表页面
            login(request, new_user)
            return redirect("blog:blog_list")
        else:
            return HttpResponse("注册表单输入有误。请重新输入~")
    elif request.method == 'GET':
        user_register_form = UserRegisterForm()
        context = {'form': user_register_form}
        return render(request, 'userprofile/register.html', context)
    else:
        return HttpResponse("请使用GET或POST请求数据")


@login_required(login_url='/userprofile/login/')
def user_delete(request, id):
    user = User.objects.get(id=id)
    if request.user == user:
        logout(request)
        user.delete()
        return redirect("blog:blog_list")
    else:
        return HttpResponse("你没有删除操作的权限。")


@login_required(login_url='/userprofile/login/')
def user_logout(request, id):
    user = User.objects.get(id=id)
    if request.user == user:
        logout(request)
        return redirect("blog:blog_list")
    else:
        return HttpResponse("你没有操作的权限。")


@login_required(login_url='/userprofile/login/')
def profile_edit(request, id):
    user = User.objects.get(id=id)
    # user_id是OneToOneField自动生成的字段
    profile = Profile.objects.get(user_id=id)

    if request.method == 'POST':
        # 验证修改数据者是否为本人
        if request.user != user:
            return HttpResponse("你没有权限修改次用户信息")

        profile_form = ProfileForm(data=request.POST)
        if profile_form.is_valid():
            # 取得清洗后的合法数据
            profile_cleaned_data = profile_form.cleaned_data
            profile.phone = profile_cleaned_data['phone']
            profile.bio = profile_cleaned_data['bio']
            profile.save()
            return redirect("userprofile:edit", id=id)

        else:
            return HttpResponse("注册表单输入有误,请重新输入")

    elif request.method == "GET":
        profile_form = ProfileForm()
        context = {'profile_form': profile_form, 'profile': profile, 'user': user}
        return render(request, 'userprofile/edit.html', context)
    else:
        return HttpResponse("请使用GET或POST请求数据")


def hash_code(s, salt='mysite_login'):
    h = hashlib.sha256()
    s += salt
    h.update(s.encode())  # update方法只接收bytes类型
    return h.hexdigest()


class LoginView(generic.FormView):
    model = User
    template_name = 'userprofile/login.html'
    form_class = UserLoginForm

    def get(self, request, *args, **kwargs):
        if request.session.get('is_login', None):
            return redirect("/")
        else:
            login_form = self.form_class()
            return render(request, self.template_name, locals())

    def post(self, request, *args, **kwargs):
        login_form = self.form_class(request.POST)
        message = "请检查填写的内容！"
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            try:
                user = User.objects.get(name=username)
            except:
                message = "用户名不存在！"
            else:
                if user.password == hash_code(password):
                    request.session['is_login'] = True
                    request.session['user_id'] = user.id
                    request.session['user_name'] = user.name
                    return redirect('/')
                else:
                    message = "密码不正确！"
        return render(request, self.template_name, locals())
