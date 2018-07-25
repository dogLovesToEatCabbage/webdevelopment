# coding=utf-8
from django.db import models

class OrderInfo(models.Model):
    oid = models.CharField(max_length=20, primary_key=True)
    user = models.ForeignKey('df_user.UserInfo', on_delete=models.CASCADE)
    odate = models.DateTimeField(auto_now=True)
    oIsPay = models.BooleanField(default=False)
    ototal = models.DecimalField(max_digits=6, decimal_places=2)
    oaddress = models.CharField(max_length=150)

# 无法实现真实支付，物流信息

class OrderDetailInfo(models.Model):
    goods = models.ForeignKey('df_goods.GoodsInfo', on_delete=models.CASCADE)
    order = models.ForeignKey(OrderInfo, on_delete=models.CASCADE)
    # 实际交易中可能会存在临时调整价格的情况，因此需要price字段
    price = models.DecimalField(max_digits=6, decimal_places=2)
    count = models.IntegerField()
