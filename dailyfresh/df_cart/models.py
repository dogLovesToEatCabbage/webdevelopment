from django.db import models

class CartInfo(models.Model):
    user = models.ForeignKey('df_user.UserInfo', models.CASCADE)
    goods = models.ForeignKey('df_goods.GoodsInfo', models.CASCADE)
    count = models.IntegerField()

