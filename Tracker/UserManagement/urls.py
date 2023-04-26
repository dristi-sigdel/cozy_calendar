from django.urls import path
from django.contrib import admin
from . import  views
from .views import *

urlpatterns = [
    path('', views.home, name='home'),
    path('index/', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('info/', views.info, name='info'),
    path('logout', views.handleLogout, name="handleLogout"),
]