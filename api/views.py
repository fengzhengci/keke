from django.shortcuts import render
from django.shortcuts import HttpResponse
from vrvtools.update_interface import *

# Create your views here.

def api_update(request):
    # 以get请求的方式赋值
    update = request.GET.get('update')
    allow = request.GET.get('allow_time')
    ret = application(update, allow)
    return HttpResponse(ret)


def version(request):
    ret = get_version()
    return HttpResponse(ret)