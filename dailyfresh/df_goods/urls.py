from django.urls import path, re_path
from . import views


urlpatterns = [
    re_path('list(\d+)_(\d+)_(\d+)/', views.list),
    re_path('(\d+)/', views.detail),
    path('search/', views.MySearchView()),
    # re_path('type/(\d+)/',)

]