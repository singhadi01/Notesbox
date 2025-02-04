"""
URL configuration for notesbox project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from videos.views import *
urlpatterns = [
    path('admin/', admin.site.urls), 
    path("",home,name="home"),
    path('login/',login_page,name="login_page"),
    path('register/',register,name="register"),
    path('logout/',logout_page,name="logout_page"),
    path('delete_subject/<id>/',delete_subject,name="delete_subject"),
    path('delete_video/<str:video_title>/',delete_video,name="delete_video"),
    path('delete_account/',delete_account,name='delete_account'),
    path('copy_subject/',copy_subject_by_code,name='copy_subject_by_code'),
    path('chat_view/',chat_view, name='chat_view'),
    path('videos/', include('videos.urls')),
]

