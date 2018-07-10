from django.shortcuts import render
from . models import *
from django.core import paginator
from django.http import Http404


def index(request):
    types = TypeInfo.objects.all() # 共有6个分类
    # print(type)
    # for i in range(len(type)):
    #     print(type[i])
    # 获取最新的4个商品对象
    # 获取点击量最多的4个商品对象
    type_0_g = types[0].goodsinfo_set.order_by('-id')[0: 4]
    type_0_gc = types[0].goodsinfo_set.order_by('-gclick')[0: 4]
    type_1_g = types[1].goodsinfo_set.order_by('-id')[0: 4]
    type_1_gc = types[1].goodsinfo_set.order_by('-gclick')[0: 4]
    type_2_g = types[2].goodsinfo_set.order_by('-id')[0: 4]
    type_2_gc = types[2].goodsinfo_set.order_by('-gclick')[0: 4]
    type_3_g = types[3].goodsinfo_set.order_by('-id')[0: 4]
    type_3_gc = types[3].goodsinfo_set.order_by('-gclick')[0: 4]
    type_4_g = types[4].goodsinfo_set.order_by('-id')[0: 4]
    type_4_gc = types[4].goodsinfo_set.order_by('-gclick')[0: 4]
    type_5_g = types[5].goodsinfo_set.order_by('-id')[0: 4]
    type_5_gc = types[5].goodsinfo_set.order_by('-gclick')[0: 4]

    # 两种获取商品的方式都可以
    # type_0_g = GoodsInfo.objects.filter(gtype=types[0]).order_by('-id')[0:4]
    context = {'title': '首页', 'page_name': 0, 'guest_cart': 1,
               'type0': types[0], "type_0_g": type_0_g, 'type_0_gc': type_0_gc,
               'type1': types[1], "type_1_g": type_1_g, 'type_1_gc': type_1_gc,
               'type2': types[2], "type_2_g": type_2_g, 'type_2_gc': type_2_gc,
               'type3': types[3], "type_3_g": type_3_g, 'type_3_gc': type_3_gc,
               'type4': types[4], "type_4_g": type_4_g, 'type_4_gc': type_4_gc,
               'type5': types[5], "type_5_g": type_5_g, 'type_5_gc': type_5_gc,
               }
    return render(request, 'df_goods/index.html', context)


def list(request, tid, pindex, sort):  # get方法传过来的参数都是str类型
    type = TypeInfo.objects.get(id=tid)  # 用get得到唯一的一个
    goods_new = type.goodsinfo_set.order_by('-id')[0: 2]  # 最新推荐2个

    if int(sort) == 1:  # 默认排序最新
        goods_sort = type.goodsinfo_set.order_by('-id')
    elif int(sort) == 2:  # 价格排序
        goods_sort = type.goodsinfo_set.order_by('gprice')
    elif int(sort) == 3:  # 人气排序，点击量
        goods_sort = type.goodsinfo_set.order_by('-gclick')
    else:
        raise Http404
    print(goods_sort)
    print(goods_sort[0].gclick)
    print(goods_sort[1].gclick)
    print(goods_sort[2].gclick)

    pagina = paginator.Paginator(goods_sort, 8)  # 每页放8个
    page = pagina.page(int(pindex))

    if 1 < int(pindex) <= len(page.paginator.page_range):
        front_page = int(pindex) - 1
    elif int(pindex) < 1 or int(pindex) > len(page.paginator.page_range):
        raise Http404
    else:
        front_page = int(pindex)

    if 1 <= int(pindex) < len(page.paginator.page_range):
        behind_page = int(pindex) + 1
    elif int(pindex) < 1 or int(pindex) > len(page.paginator.page_range):
        raise Http404
    else:
        behind_page = int(pindex)

    context = {'title': '商品列表', 'page_name': 0, 'guest_cart': 1,
               'goods_new': goods_new, 'type': type, 'page': page,
               'tid': tid, 'pindex': pindex, 'sort': int(sort),
               'front_page': front_page, 'behind_page': behind_page
               # 'behind_page': page.next_page_number(), 'front_page': page.previous_page_number()
               }
    # print(goods_sort)
    return render(request, 'df_goods/list.html', context)


def detail(request, gid):
    goods = GoodsInfo.objects.get(pk=gid)
    goods.gclick = goods.gclick + 1
    goods.save()  # 记住要save()，这样点击量增加才会写入到数据库中
    gtype = goods.gtype

    # type = TypeInfo.objects.filter(ttitle=gtype)
    # goods_adv = type[0].goodsinfo_set.order_by('-id')[0: 2]
    # 两种方法都可以获取到最新的的前两个商品
    goods_new = gtype.goodsinfo_set.order_by('-id')[0: 2]
    context = {'title': '商品详情', 'page_name': 0,
               'guest_cart': 1, 'goods': goods,
               'gtype': gtype, 'goods_new': goods_new}
    response = render(request, 'df_goods/detail.html', context)
    # 在访问detail页面的时候把访问的商品信息添加到cookie中
    # 最近浏览，将最近看过的5件商品展示出来
    # 由于最近浏览不为私密信息，因此将最近浏览的信息放在cookie，没必要放在session

    goods_ids = request.COOKIES.get('goods_ids', '') # goods_ids是字符串（例：'23,4,5,12,22'），默认值为''
    goods_id = '%d' % goods.id
    if goods_ids != '': # 判断是否有浏览记录
        goods_ids1 = goods_ids.split(',')  # 字符串拆分成列表
        if goods_ids1.count(goods_id) >= 1:  # 判断goods_id在列表中是否已存在
            goods_ids1.remove(goods_id)  # 若之前存在，删除
        goods_ids1.insert(0, goods_id)  # 将其插入到第一个的位置
        if len(goods_ids1) >= 6:  # 只要前五个记录
            del goods_ids1[5]
        goods_ids = ','.join(goods_ids1)
    else:
        goods_ids = goods_id

    response.set_cookie('goods_ids', goods_ids)
    return response