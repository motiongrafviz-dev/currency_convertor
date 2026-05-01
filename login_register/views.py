
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView
from django.conf import settings
import requests
from .models import *
import json
import time

from django.http import JsonResponse
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
import csv

from datetime import datetime, timedelta


import base64
from io import BytesIO

import pandas as pd
import seaborn as sns
import matplotlib


import matplotlib.pyplot as plt

from twilio.rest import Client
plt.switch_backend('Agg')

change_eur = 0
change_ils = 0
change_gbp = 0
change_jpy = 0
list_currencys = {}
your_number = 0
API_KEY = "*"
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
    global API_KEY,change_eur,change_gbp,change_ils,change_jpy,list_currencys
    data = DataBaseCurrencys.objects.all()
    username = (request.POST.get('username') or '').strip()
    email = (request.POST.get('email') or '').strip()
    password = (request.POST.get('password') or '').strip()
    if Login.objects.filter(username=username).exists() and Login.objects.filter(email=email).exists() and Login.objects.filter(password=password).exists():
        name = []
        valuat = []
        chrome_options = Options()
        chrome_options.add_argument("--log-level=3")
        chrome_options.add_argument("--disable-logging")
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        driver = webdriver.Chrome(service=Service(), options=chrome_options)
        wait = WebDriverWait(driver, 20)

        driver.get("https://www.boi.org.il/en/economic-roles/financial-markets/exchange-rates/")
        url = f'https://v6.exchangerate-api.com/v6/{API_KEY}/latest/USD'

        time.sleep(3)

        usd = wait.until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "odd"))
        )


        time.sleep(3)

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



    for i in data:
        for ie,v in i.currencys.items():
            print(ie,v)
            if ie == "USD":
                with open("usd.txt", "a") as datae:
                    datae.write(str(v) + "\n")
            if ie == "EUR":
                with open("eur.txt", "a") as datae:
                    datae.write(str(v) + "\n")
            if ie == "GBP":
                with open("gbp.txt", "a") as datae:
                    datae.write(str(v) + "\n")
            if ie == "JPY":
                with open("jpy.txt", "a") as datae:
                    datae.write(str(v) + "\n")
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






def chart_usd(request):
    indexes = []
    result_float = []
    with open("usd.txt", "r") as datae:
        saved = datae.read().split()
        for i in saved:
            result_float.append(float(i))
    
    for i in range(len(result_float)):
        indexes.append(i)
    df = pd.DataFrame(result_float)
    print(result_float,indexes)
    chart = None

    if not df.empty:
        sns.set_theme(style="white", context="talk")

        plt.figure(figsize=(10, 6))

        sns.lineplot(
            data=df,
            x=indexes,
            y=result_float,
            marker="o"
        )

        plt.title("Watch Time Statistics", fontsize=18, weight="bold")
        plt.xlabel("Date")
        plt.ylabel("Watch time, minutes")

        sns.despine()
        plt.tight_layout()

        buffer = BytesIO()
        plt.savefig(buffer, format="png", dpi=90)
        buffer.seek(0)

        chart = base64.b64encode(buffer.getvalue()).decode("utf-8")

        buffer.close()
        plt.close()

    return render(request, "app/main_page.html", {"chart1": chart})
    

def chart_eur(request):

    indexes = []
    result_float = []
    with open("eur.txt", "r") as datae:
        saved = datae.read().split()
        for i in saved:
            result_float.append(float(i))
    print(result_float)
    for i in range(len(result_float)):
        indexes.append(i)
    df = pd.DataFrame(result_float)
    chart = None

    if not df.empty:
        sns.set_theme(style="white", context="talk")

        plt.figure(figsize=(10, 6))

        sns.lineplot(
            data=df,
            x=indexes,
            y=result_float,
            marker="o"
        )

        plt.title("Watch Time Statistics", fontsize=18, weight="bold")
        plt.xlabel("Date")
        plt.ylabel("Watch time, minutes")

        sns.despine()
        plt.tight_layout()

        buffer = BytesIO()
        plt.savefig(buffer, format="png", dpi=90)
        buffer.seek(0)

        chart = base64.b64encode(buffer.getvalue()).decode("utf-8")

        buffer.close()
        plt.close()

    return render(request, "app/main_page.html", {"chart2": chart})

def chart_gbp(request):

    indexes = []
    result_float = []
    with open("gbp.txt", "r") as datae:
        saved = datae.read().split()
        for i in saved:
            result_float.append(float(i))
    print(result_float)
    for i in range(len(result_float)):
        indexes.append(i)
    df = pd.DataFrame(result_float)

    chart = None

    if not df.empty:
        sns.set_theme(style="white", context="talk")

        plt.figure(figsize=(10, 6))

        sns.lineplot(
            data=df,
            x=indexes,
            y=result_float,
            marker="o"
        )

        plt.title("Watch Time Statistics", fontsize=18, weight="bold")
        plt.xlabel("Date")
        plt.ylabel("Watch time, minutes")

        sns.despine()
        plt.tight_layout()

        buffer = BytesIO()
        plt.savefig(buffer, format="png", dpi=90)
        buffer.seek(0)

        chart = base64.b64encode(buffer.getvalue()).decode("utf-8")

        buffer.close()
        plt.close()

    return render(request, "app/main_page.html", {"chart3": chart})

def chart_jpy(request):

    indexes = []
    result_float = []
    with open("jpy.txt", "r") as datae:
        saved = datae.read().split()
        for i in saved:
            result_float.append(float(i))
    print(result_float)
    for i in range(len(result_float)):
        indexes.append(i)
    df = pd.DataFrame(result_float)

    chart = None

    if not df.empty:
        sns.set_theme(style="white", context="talk")

        plt.figure(figsize=(10, 6))

        sns.lineplot(
            data=df,
            x=indexes,
            y=result_float,
            marker="o"
        )

        plt.title("Watch Time Statistics", fontsize=18, weight="bold")
        plt.xlabel("Date")
        plt.ylabel("Watch time, minutes")

        sns.despine()
        plt.tight_layout()

        buffer = BytesIO()
        plt.savefig(buffer, format="png", dpi=90)
        buffer.seek(0)

        chart = base64.b64encode(buffer.getvalue()).decode("utf-8")

        buffer.close()
        plt.close()

    return render(request, "app/main_page.html", {"chart4": chart})





def msg_for_usd(request):
    account_sid = "*"
    auth_token = "*"
    name = []
    valuat = []
    number_you_want_see = request.POST.get("number_you_want_see")
    while True:
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        driver = webdriver.Chrome(service=Service(), options=chrome_options)
        wait = WebDriverWait(driver, 22)

        driver.get("https://www.boi.org.il/en/economic-roles/financial-markets/exchange-rates/")
        url = f'https://v6.exchangerate-api.com/v6/{API_KEY}/latest/USD'

        time.sleep(3)

        usd = wait.until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "odd"))
        )


        time.sleep(3)

        rows = driver.find_elements(By.TAG_NAME, "tr")
        
        for row in rows:
            text = row.text
            match = re.search(r'\b([A-Z]{3})\b.*?(\d+\.\d+)', text)
            if match:
                name.append(match.group(1))
                valuat.append(match.group(2))

        if float(valuat[0]) == float(number_you_want_see):
            new_Client = Client(account_sid, auth_token)
            message = new_Client.messages.create(
                to="+972532251473",
                from_="+19895642482",
                body=f'USD is now {valuat[0]} how you wanted {number_you_want_see}')
            print(message.sid)
            break
        else:
            print(valuat[0],"wait some more")
            valuat = []
            name = []
            time.sleep(5)






    return render(request, "app/main_page.html", )


