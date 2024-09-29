from django.contrib import admin
from django.urls import path, re_path
from users import views

urlpatterns = [
    re_path('login', views.login),
    re_path('register', views.register),
    re_path('profile', views.profile),
    re_path('logout', views.logout),
]
