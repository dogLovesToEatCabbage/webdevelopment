from django.urls import re_path
from . import views


urlpatterns = [
    re_path('^$', views.cart),
    re_path('add(\d+)_(\d+)/', views.add),
    re_path('edit(\d+)_(\d+)/', views.edit),
    re_path('delete(\d+)/', views.delete)
]