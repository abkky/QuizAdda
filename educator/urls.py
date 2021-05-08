from django.contrib import admin
from django.urls import path, include
from . import views
urlpatterns = [
    path('',views.index,name='home'),
    path('signup', views.signup,name="signup"),
    path('login', views.login,name="login"),
    path('logout', views.logout,name="logout"),
    path('createquiz', views.createquiz,name="createquiz")
]