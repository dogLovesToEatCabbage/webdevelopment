from django.shortcuts import render, redirect
from df_user import user_decorator
from django.db import transaction
from df_cart.models import *
from df_user.models import *
from df_goods.models import *
from .models import *
from django.http import JsonResponse
import datetime

@user_decorator.login
def order(request):
    """从GET中获取传递过来的勾选的购物车id，展示提交的订单页面"""
    try:
        # 从数据库中获取当前登录的用户
        uid = request.session.get('user_id')
        user = UserInfo.objects.get(id=uid)

        # 获取GET中传过来的购物车id
        cart_ids = request.GET.getlist('cartid')
        # 提交订单页面商品序号，是序号不是商品的购物车编号，也不是商品的编号

        carts = []
        for cart_id in cart_ids:
            carts.append(CartInfo.objects.get(id=int(cart_id)))

        # 判断用户手机号是否为空，分别做展示
        if user.uphone == '':
            uphone = ''
        else:
            uphone = user.uphone
            uphone = uphone[:3] + '****' + uphone[-4:]
        context = {'title': '天天生鲜.提交订单', 'title2': '提交订单',
                   'page_name': 1, 'carts': carts,
                   'user': user, 'ureceive_phone': uphone,
                   }
        return render(request, 'df_order/place_order.html', context)
    except Exception as e:
        print(e)
        return redirect('/index/')

@transaction.atomic()
@user_decorator.login
def order_handle(request):
    tran_id = transaction.savepoint()
    try:
        # 1、创建订单对象, 相应信息写入到df_order_orderinfo数据库中
        uid = request.session.get('user_id')
        now = datetime.datetime.now()
        orderinfo = OrderInfo()
        orderid = '%s%d'%(now.strftime('%Y%m%d%H%M%S'), uid)
        orderinfo.oid= orderid
        orderinfo.odate = now
        orderinfo.oIsPay = False
        orderinfo.ototal = request.POST.get('total_pay')  # ajax传递过来的
        orderinfo.oaddress = request.POST.get('oaddress')  # ajax传递过来的

        orderinfo.user_id = uid
        orderinfo.save()

        # 2、判断已提交的购物车中商品的库存
        cart_ids = request.POST.getlist('cart_ids[]')  # ajax传递过来的,注意是如何取出数据的
        print(cart_ids)
        for cart_id in cart_ids:
            cartinfo = CartInfo.objects.get(id=cart_id)
            goodsinfo = GoodsInfo.objects.get(id=cartinfo.goods_id)

            # 库存足够
            if int(cartinfo.goods.gkucun) >= int(cartinfo.count):
               # 创建详单对象，向数据库中写入数据
                orderdetailinfo = OrderDetailInfo()
                orderdetailinfo.price = goodsinfo.gprice
                print(orderdetailinfo.price)
                orderdetailinfo.count = int(cartinfo.count)
                orderdetailinfo.goods_id = int(goodsinfo.id)
                orderdetailinfo.order_id = int(orderinfo.oid)
                orderdetailinfo.save()

               # 修改商品库存
                goodsinfo.gkucun -= int(cartinfo.count)
                goodsinfo.save()

                # 删除已经提交的购物车
                cartinfo.delete()

            else:
                # 库存不足
                transaction.savepoint_rollback(tran_id)
                return JsonResponse({'status': 2})
    except Exception as e:
        print(e)
        transaction.savepoint_rollback(tran_id)
    # 将这两个数据作为一个json对象传递给前段，前段通过data.status和data.orderid能够获取到这两个键的值
    return JsonResponse({'status': 1})
