from django.shortcuts import render, redirect
from . models import *
from df_user import user_decorator
from django.http import JsonResponse

@user_decorator.login
def cart(request):
    """购物车页面"""
    # 去CartInfo中查找是否有该登录用户的购物信息
    uid = request.session['user_id']
    carts = CartInfo.objects.filter(user_id=uid)
    total_count = carts.count()
    context = {'title': '购物车', 'page_name': 0,
               'guest_cart': 0, 'carts': carts,
               'total_count': total_count
               }
    return render(request, 'df_cart/cart.html', context)

@user_decorator.login
def add(request, gid, count):
    """向购物车中添加商品"""
    # 用户uid购买了gid商品,数量为count
    # 将user,gods,count写入cart表中
    gid = int(gid)
    count = int(count)
    uid = request.session['user_id']
    carts = CartInfo.objects.filter(user_id=uid, goods_id=gid)
    # 判断购物车表中是否已有该商品，有则数量增加；无，则新增
    if len(carts) >= 1:
        cart = carts[0]
        cart.count = cart.count + count
    else:
        cart = CartInfo()
        cart.user_id = uid
        cart.goods_id = gid
        cart.count = count
    cart.save()
    # 是AJAX请求则返回json数据，不是则转向/cart/
    if request.is_ajax():
        count = CartInfo.objects.filter(user_id=request.session['user_id']).count()
        return JsonResponse({'count': count})
    else:
        return redirect('/cart/')

@user_decorator.login
def edit(request, cart_id, count):
    try:
        cart = CartInfo.objects.get(id=int(cart_id))
        cart.count = int(count)
        cart.save()
        data = {'ok': 1}
    except Exception as e:
        data = {'0k': 0}
    return JsonResponse(data)



@user_decorator.login
def delete(request, cart_id):
    """从数据库删除购物车中某一条数据，页面显示的删除在js中操作"""
    try:
        cart_del = CartInfo.objects.get(id=int(cart_id))
        cart_del.delete()
        data = {'ok': 1}
    except Exception as e:
        data = {'ok': 0}
    return JsonResponse(data)