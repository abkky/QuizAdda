from django.contrib import admin
from django.urls import path, include
from . import views
urlpatterns = [
    path('',views.index,name='home'),
    path('signup', views.signup,name="signup"),
    path('login', views.login,name="login"),
    path('logout', views.logout,name="logout"),
    path('createquestion', views.createquestion,name="createquestion"),
    path('createquiz', views.createquiz,name="createquiz"),
    path('userprofile', views.userprofile,name="userprofile"),
    path('updateprofile', views.updateprofile,name="updateprofile"),
    path('updatepassword',views.updatepassword,name="updatepassword",),
    path('publishquiz',views.publishquiz,name="publishquiz",),
    path('validateusername', views.validateusername, name='validateusername'),
    path('validateemail', views.validateemail, name='validateemail'),
    path('quizzes', views.quizzes, name='quizzes'),
    path('viewquiz', views.viewquiz, name='viewquiz'),
    path('quizmodify', views.quizmodify, name='quizmodify'),
    path('deletequiz', views.deletequiz, name='deletequiz'),
    path('deleteques', views.deleteques, name='deleteques'),
    path('updatequiz', views.updatequiz, name='updatequiz'),
    path('analytics', views.analytics, name='analytics'),
    path('analytics/<int:qid>', views.anquiz, name='anquiz'),
    path('analytics/<int:qid>/<int:uid>', views.squiz, name='squiz'),
]