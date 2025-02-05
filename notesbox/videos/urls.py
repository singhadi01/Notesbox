from django.urls import path
from .views import *


urlpatterns = [
    path('',instructions,name='instructions'),
    path('home/', home, name='homepage'),
    path('chat/',chat_view, name='chat_view'),
]
