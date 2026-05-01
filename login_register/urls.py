
from django.urls import path, re_path
from .views import *

urlpatterns = [
    path('login/', login, name='login'),
    path('register/', register, name='register'),
    path('login_window/', login_window, name='login_window'),
    path('register_window/', register_window, name='register_window'),
    path('currency_amount/', currency_amount, name='currency_amount'),
    path('chart_usd/', chart_usd, name='chart_usd'),
    path('chart_eur/', chart_eur, name='chart_eur'),
    path('chart_gbp/', chart_gbp, name='chart_gbp'),
    path('chart_jpy/', chart_jpy, name='chart_jpy'),
    path('msg_for_usd/', msg_for_usd, name='msg_for_usd'),

]