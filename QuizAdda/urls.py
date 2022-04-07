from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index,name="home"),
    path('joinquiz/<int:id>', views.joinquiz,name="joinquiz"),
    path('tjoin', views.tjoin,name="tjoin"),
    path('educator/',include('educator.urls')),
    path('attemptquiz', views.attemptquiz,name="attemptquiz"),
]
