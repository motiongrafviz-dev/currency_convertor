from django.urls import path, re_path
from .views import *

urlpatterns = [
    path('login/', login, name='login'),
    path('register/', register, name='register'),
    path('login_window/', login_window, name='login_window'),
    path('register_window/', register_window, name='register_window'),
    path('currency_amount/', currency_amount, name='currency_amount'),
]