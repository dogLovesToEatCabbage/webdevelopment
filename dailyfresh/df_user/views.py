#coding=utf-8
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from df_user.models import *
from hashlib import sha1
from . import user_decorator
from df_goods.models import *


def register(request):
    """注册页面"""
    title = '天天生鲜-注册'
    context = {'title': title}
    return render(request,'df_user/register.html', context)


def register_handle(request):
    """注册按钮处理"""
    uname = request.POST.get('user_name')
    upwd = request.POST.get('pwd')
    upwd2 = request.POST.get('cpwd')
    uemail = request.POST.get('email')

    # 如果两次密码不相等，重定向到这个URL：/user/register/
    if upwd != upwd2:
        return redirect('/user/register/')

    # 利用sha1进行密码加密，因为数据库中存的是加密后的密码
    s1 = sha1()
    s1.update(upwd.encode())
    upwd3 = s1.hexdigest()

    # 不用检查是否与数据库中的用户名和email冲突吗？
    # 创建模型类对象，写入数据库
    user = UserInfo()
    user.uname = uname
    user.upwd = upwd3
    user.uemail = uemail
    user.save()

    # 注册成功，转到登录页面
    return redirect('/user/login/')


def register_exist(request):
    """接收AJAX传递过来的数据，作判断是否已存在"""
    uname = request.GET.get('user_name')
    count = UserInfo.objects.filter(uname=uname).count()
    data = {'count': count}
    return JsonResponse(data)


def login(request):
    """"注册页"""
    uname = request.COOKIES.get('uname', '')
    context = {'title': '天天生鲜-登录', 'error_name': 0, 'error_pwd': 0, 'uname': uname}
    return render(request, 'df_user/login.html', context)


def login_handle(request):
    """注册页处理"""
    # 接收请求数据
    uname = request.POST.get('username')
    upwd = request.POST.get('pwd')
    jizhu = request.POST.get('jizhu', 0)

    # 根据用户名查询对象
    users = UserInfo.objects.filter(uname=uname) #查询集是个列表[]
    # print(uname)

    if len(users)==1:
         # 密码加密
        s1 = sha1()
        s1.update(upwd.encode())
        if s1.hexdigest() == users[0].upwd:
            url = request.COOKIES.get('url', '/index/')
            red = HttpResponseRedirect(url)
            # 记住用户名
            if jizhu != 0:
                red.set_cookie('uname', uname)
            else:
                red.set_cookie('uname', '', max_age=-1)
            request.session['user_id'] = users[0].id
            request.session['user_name'] = uname
            return red
        else:
            context = {'title': '天天生鲜-登录', 'error_name': 0, 'error_pwd': 1, 'uname': uname, 'upwd': upwd}
            return render(request, 'df_user/login.html', context)
    else:
        context = {'title': '天天生鲜-登录', 'error_name': 1, 'error_pwd': 0, 'uname': uname, 'upwd': upwd}
        return render(request, 'df_user/login.html', context)


def logout(request):
    request.session.flush()  # 清除了session中所有数据，当然也可以只清楚部分
    return redirect('/index/')


@user_decorator.login
def info(request):
    """用户中心页面"""
    # 从cookie中取出最近浏览的商品信息
    goods_ids = request.COOKIES.get('goods_ids', '')  # 字符串格式
    goods_list = []
    if goods_ids != '':
        goods_ids1 = goods_ids.split(',')
        for gid in goods_ids1:
            goods_list.append(GoodsInfo.objects.get(id=int(gid)))

    uname = request.COOKIES.get('uname')
    if uname:
        uemail = UserInfo.objects.filter(uname=uname)[0].uemail
        uphone = ''
        # uaddress = ''
        context = {'title': '用户中心', 'uname': uname,
                   'uemail': uemail, 'uphone': uphone,
                   'page_name': 1, 'guest_cart': 0,
                   'goods_list': goods_list
                   }
        return render(request, 'df_user/user_center_info.html', context)
    else:
        return redirect('/user/login/')


@user_decorator.login
def order(request):
    """订单页面"""
    context = {'title': '用户中心', 'page_name': 1, 'guest_cart': 0}
    return render(request, 'df_user/user_center_order.html', context)


@user_decorator.login
def site(request):
    """收货信息页面"""
    user = UserInfo.objects.get(pk=request.session['user_id'])
    if request.method == 'POST':
        post = request.POST
        user.urecipients = post.get('urecipients')
        user.uaddress = post.get('uaddress')
        user.upostcode = post.get('upostcode')
        user.uphone = post.get('uphone')
        user.save()

    context = {'title': '用户中心', 'user': user, 'page_name': 1, 'guest_cart': 0}

    return render(request, 'df_user/user_center_site.html', context)

