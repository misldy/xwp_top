from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect

from messagelog.forms import MessageLogForm
from messagelog.models import MessageLog


# Create your views here.
@login_required(login_url='/userprofile/login/')
def post_message_log(request):
    # 处理post请求
    if request.user.id == 1:
        message_logs = MessageLog.objects.all()
    else:
        message_logs = MessageLog.objects.filter(user=request.user)
    if request.method == 'POST':
        message_log_from = MessageLogForm(request.POST)
        if message_log_from.is_valid():
            new_message_log = message_log_from.save(commit=False)
            new_message_log.user = request.user
            new_message_log.save()
            return redirect('messagelog:post_message_log')
        else:
            return HttpResponse("表单内容有误,请重新填写。")
    else:
        # checkmobile = checkMobile(request)
        context = {'message_logs': message_logs}
        return render(request, 'messagelog.html', context)
