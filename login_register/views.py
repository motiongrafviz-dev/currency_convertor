from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView
from django.conf import settings
import requests
from .models import *
import json
import time


import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import StaleElementReferenceException
import re
import logging
import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import speech_recognition as sr
import csv

from datetime import datetime, timedelta


change_eur = 0
change_ils = 0
change_gbp = 0
change_jpy = 0
list_currencys = {}
your_number = 0
API_KEY = "e677d093094d4d3564a2a1f0"
def register(request):
    register_base = Login.objects.all()
    username = (request.POST.get('username') or '').strip()
    email = (request.POST.get('email') or '').strip()
    password1 = (request.POST.get('password1') or '').strip()
    password2 = (request.POST.get('password2') or '').strip()
    if register_base:
        if not Login.objects.filter(username=username).exists() and not Login.objects.filter(email=email).exists() and not Login.objects.filter(password=password1).exists() and password1 == password2 :
            Login.objects.create(username=username,email=email,password=password1)
            return render(request, "app/index.html", {})
         
    return render(request, "app/register.html", {})

def login(request):
    global API_KEY,change_eur,change_gbp,change_ils,change_jpy
    data = DataBaseCurrencys.objects.all()
    username = (request.POST.get('username') or '').strip()
    email = (request.POST.get('email') or '').strip()
    password = (request.POST.get('password') or '').strip()
    if Login.objects.filter(username=username).exists() and Login.objects.filter(email=email).exists() and Login.objects.filter(password=password).exists():
        name = []
        valuat = []
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        driver = webdriver.Chrome(service=Service(), options=chrome_options)
        wait = WebDriverWait(driver, 20)

        driver.get("https://www.boi.org.il/en/economic-roles/financial-markets/exchange-rates/")
        url = f'https://v6.exchangerate-api.com/v6/{API_KEY}/latest/USD'

        time.sleep(2)

        usd = wait.until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "odd"))
        )


        time.sleep(2)

        rows = driver.find_elements(By.TAG_NAME, "tr")

        for row in rows:
            text = row.text
            match = re.search(r'\b([A-Z]{3})\b.*?(\d+\.\d+)', text)
            if match:
                name.append(match.group(1))
                valuat.append(match.group(2))

        list_currencys[name[0]] = valuat[0]
        list_currencys[name[1]] = valuat[1]
        list_currencys[name[2]] = valuat[2]
        list_currencys[name[3]] = valuat[3]
        for i in data:
            i.currencys = list_currencys
            i.save(update_fields=['currencys'])
        print(list_currencys)
        
        response = requests.get(url)
        data = response.json()
        eur_ = (data["conversion_rates"]["EUR"])
        ils_ = (data["conversion_rates"]["ILS"]) 
        gbp_ = (data["conversion_rates"]["GBP"])
        jpy_ = (data["conversion_rates"]["JPY"])
 

        response = requests.get(url)
        data = response.json()
        eur_new = (data["conversion_rates"]["EUR"])
        ils_new = (data["conversion_rates"]["ILS"]) 
        gbp_new = (data["conversion_rates"]["GBP"])
        jpy_new = (data["conversion_rates"]["JPY"])
        change_eur = ((eur_new - eur_) / eur_) * 100
        change_ils = ((ils_new - ils_) / ils_) * 100
        change_gbp = ((gbp_new - gbp_) / gbp_) * 100
        change_jpy = ((jpy_new - jpy_) / jpy_) * 100
        return render(request, "app/main_page.html", {"list_currencys": list_currencys, "change_ils": change_ils, "change_gbp": change_gbp, "change_jpy": change_jpy})
    return render(request, "app/login.html", {})

def login_window(request):
    return render(request, "app/login.html", {})
def register_window(request):
    return render(request, "app/register.html", {})

def currency_amount(request):
    global change_eur,change_gbp,change_ils,change_jpy,your_number
    data = DataBaseCurrencys.objects.all()
    from_currency = (request.POST.get('from_currency') or '').strip()
    amount = (request.POST.get('amount') or '').strip()
    for i in data:
        for ie,v in i.currencys.items():
            int_v = float(v)
            int_amount = float(amount)
            if ie == from_currency:
                your_number = float(int_amount * int_v)
    return render(request, "app/main_page.html", {"data": data, "change_ils": change_ils, "change_gbp": change_gbp, "change_jpy": change_jpy,"your_number": your_number})
