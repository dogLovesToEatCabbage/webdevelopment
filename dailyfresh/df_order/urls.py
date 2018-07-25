from django.urls import re_path
from . import views

urlpatterns = [
    re_path('^$', views.order),
    re_path('^order_handle/$', views.order_handle),
]