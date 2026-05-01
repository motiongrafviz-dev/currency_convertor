from django.urls import path, re_path

from .views import *


urlpatterns = [
    path('', index, name='index'),
    path('start/', start_timer, name='start_timer'),
    path('stop/', stop, name='stop'),
    
]