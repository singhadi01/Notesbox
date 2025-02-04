from django.urls import path
from .views import *


urlpatterns = [
    path('', home, name='homepage'),
    path('chat/',chat_view, name='chat_view'),
]
