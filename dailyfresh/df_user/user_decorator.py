from django.http import HttpResponseRedirect

# 是否已登录。是。则进入请求页面；否，则转到登录界面，且登录之后在进入之前的请求页面
def login(func):
    def login_func(request, *args, **kwargs):
        if request.session.has_key('user_id'):
            return func(request, *args, **kwargs)
        else:
            red = HttpResponseRedirect('/user/login/')
            # 这里不要用request.get_full_path()，因为程序走到这里都是在登录页面点击登录后再
            # 跳转到想去的页面，因此都是以POST方法来请求的，所以用request。get_full_path()会把
            # POST中的所有参数也都放到url中，然后会以get方法请求，造成404
            red.set_cookie('url', request.path)


            return red
    return login_func

"""
request.path与request.get_full_path区别
示例：http://127.0.0.1:8080/goods/13/?type=6
request.path表当前路径: /goods/13/
request.get_full_path()表完整路径: /goods/13/?type=6
"""