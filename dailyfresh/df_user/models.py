from django.db import models


class UserInfo(models.Model):
    uname = models.CharField(max_length=20)
    upwd = models.CharField(max_length=40)
    uemail = models.EmailField()
    uphone = models.CharField(max_length=11, default='')
    uaddress = models.CharField(max_length=100, default='')
    upostcode = models.CharField(max_length=6,default='')
    urecipients = models.CharField(max_length=20,default='')

