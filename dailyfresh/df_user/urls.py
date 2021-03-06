from django.urls import path, re_path
from . import views

urlpatterns = [
    path('register/', views.register),
    path('register_handle/', views.register_handle),
    path('register_exist/', views.register_exist),
    path('login/', views.login),
    path('login_handle/', views.login_handle),
    path('info/', views.info),
    re_path('order(\d*)/', views.order),
    path('site/', views.site),
    path('logout/', views.logout),
]
