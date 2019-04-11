#_*_coding:utf-8_*_
from django.shortcuts import render,HttpResponseRedirect,HttpResponse,redirect
from django.http import HttpResponseNotFound,Http404,FileResponse
from django.contrib import auth
from django.contrib.auth.decorators import login_required 
import django.utils.timezone
from django.core.exceptions import ObjectDoesNotExist

#from .forms import *

import json

from vrvtools.vrvctrl import *
from vrvtools.to_django import *
from vrvtools import sshmodifi
from vrvtools import mdeth

# Create your views here.

# 主页
@login_required
def index(request):
    try :
        sysinfo = get_data()
    except BaseException as e :
        print(e)
        return render(request,'index.html')
        #raise Http404()
    return render(request,'index.html',sysinfo)

# 用户中心配置
@login_required
def profile(request):
    return render(request,'profile.html')

# 用户登录
def login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request,user)
            request.session.set_expiry(60*30) # session半个小时后过期
            #request.session.set_expiry(0)
            return HttpResponseRedirect('../')
        else:
            return render(request,'login.html',{'login_err': '用户名或密码错误'})

    else:
        return render(request, 'login.html')


@login_required
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect("../login")


# 服务列表展示
@login_required
def servicelist(request):
    if request.method == "POST":
        logs = request.POST.get('logname')
        logdir = request.POST.get('logdir')
        server = request.POST.get('servername')
        mode = request.POST.get('servermode')

        # 服务启停
        if server and mode :
            vrvctrl(server,mode)
            return HttpResponse(json.dumps({'status':'1'}))

        # 日志下载
        if logs and logdir :
            logs = json.loads(logs)
            global logfile
            logfile = getlog(logdir,logs)
            if logfile : # 打包完毕后下载日志
                return HttpResponse(json.dumps({'status':'1'}))
            else :    # 打包失败
                return HttpResponse(json.dumps({'status':'0'}))
        return HttpResponse(json.dumps({'status':'0'}))
    
    base = vrvcheck()    # 检查所有服务状态
    return render(request,'servicelist.html',{"vrvserver":base})

# 日志下载
@login_required
def downlog(request):
    logzip=open(logfile,'rb')  
    response =FileResponse(logzip)  
    response['Content-Type']='application/octet-stream'  
    response['Content-Disposition']='attachment;'  
    return response 


# ssh安全配置
@login_required
def sshctrl(request,mode):
    status = {"ssh": {"isOpen": None,"port": None}}

    ssh_port = sshmodifi.check() # 检查当前端口号

    if request.method == "POST": 
        isopen = request.POST.get('isOpen')
        port   = request.POST.get('port')
        if isopen :
            if ssh_port :    
                #sshmodifi.modifi(int(port))    # 服务开启状态修改端口
                pass
            else :
                #sshmodifi.start()    # 先启动服务并修改端口
                #sshmodifi.modifi(int(port))    
                pass
        else :
            #sshmodifi.stop()        # 关闭服务
            pass

        return HttpResponse(json.dumps({'code':1}))

    # 返回ssh状态
    if ssh_port :
        status["ssh"]["isOpen"] = True
        status["ssh"]["port"] = ssh_port
    else :
        status["ssh"]["isOpen"] = False

    return HttpResponse(json.dumps({'data':status}))

# 安全中心主页
@login_required
def sysecurity(request):
    return render(request,'sysecurity.html')


# 网卡配置中心
@login_required
def ethctrl(request,mode):
    if mode == 'check' :  
        info = mdeth.get_server_info()
        return HttpResponse(json.dumps({'data':{'serverIP':info}}))    # 返回当前网卡信息
    elif request.method == "POST" and mode == 'commit':    
        info = request.POST.get('serverIP')
        if mdeth.parse(info) :    # 修改当前网卡信息
            return HttpResponse(json.dumps({'code':1}))
        else :
            return HttpResponse(json.dumps({'code':0}))
    else :
        raise Http404()

# 网卡配置主页
@login_required
def eth(request):
    return render(request,'eth.html')
