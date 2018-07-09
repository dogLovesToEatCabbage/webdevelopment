from django.db import models
from tinymce.models import HTMLField

class TypeInfo(models.Model):
    ttitle = models.CharField(max_length=20)
    isDelete = models.BooleanField(default=False)

    def __str__(self):
        return self.ttitle

    class Meta():
        ordering = ['id']

class GoodsInfo(models.Model):
    gtitle = models.CharField(max_length=20,)
    gpic = models.ImageField()
    gprice = models.DecimalField(max_digits=5, decimal_places=2)
    gunit = models.CharField(max_length=20)
    gkucun = models.IntegerField()
    gclick = models.IntegerField()
    gintroduce = models.CharField(max_length=200)
    gcontent = HTMLField()
    gtype = models.ForeignKey(TypeInfo, on_delete=models.CASCADE)
    isDelete = models.BooleanField(default=False)
    # gadv = models.BooleanField(default=False)

    def __str__(self):
        return self.gtitle

    class Meta():
        ordering = ['id', 'gprice', 'gkucun', 'gclick']