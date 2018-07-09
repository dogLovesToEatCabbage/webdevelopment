from django.contrib import admin
from . models import *


class GoodsAdmin(admin.ModelAdmin):
    list_display = ['id', 'gtitle', 'gunit', 'gprice', 'gkucun', 'gintroduce', 'gtype']
    list_per_page = 15
    list_filter = ['id', 'gtitle', 'gunit', 'gprice', 'gkucun', 'gtype']
    search_fields = ['id', 'gtitle', 'gunit', 'gprice', 'gkucun', 'gtype']

class TypeAdmin(admin.ModelAdmin):
    list_display = ['id', 'ttitle']





admin.site.register(TypeInfo, TypeAdmin)
admin.site.register(GoodsInfo, GoodsAdmin)
