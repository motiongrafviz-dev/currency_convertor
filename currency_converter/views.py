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
import speech_recognition as sr
import csv

from datetime import datetime, timedelta
# from .forms import NewPageForm

API_KEY = "e677d093094d4d3564a2a1f0"
stop = True
change_eur = 0
change_usd  =0
change_gbp = 0
change_jpy = 0
eur = 0
usde = 0
gbp = 0
jpy = 0
def index(request):
    global API_KEY,change_eur,change_gbp,change_jpy,eur,usde,gbp,jpy
    name = []
    valuat = []
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    driver = webdriver.Chrome(service=Service(), options=chrome_options)
    wait = WebDriverWait(driver, 20)

    driver.get("https://www.boi.org.il/en/economic-roles/financial-markets/exchange-rates/")

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
    time.sleep(2)
    print(valuat, valuat[0])
    usde = valuat[0]
    gbp = valuat[1]
    jpy = valuat[2]
    eur = valuat[3]
    return render(request, "app/index.html", {"EUR": eur, "usdd": usde, "GBP": gbp, "JPY": jpy})


def start_timer(request):
    global API_KEY,change_eur,change_gbp,change_jpy,stop,eur,usde,gbp,jpy
    stop = True
    url = f'https://v6.exchangerate-api.com/v6/{API_KEY}/latest/USD'
    response = requests.get(url)
    data = response.json()

    while stop:
        time.sleep(3)
        response = requests.get(url)
        data = response.json()
        usd_new = (data["conversion_rates"]["USD"])
        eur_new = (data["conversion_rates"]["EUR"])
        gbp_new = (data["conversion_rates"]["GBP"])
        jpy_new = (data["conversion_rates"]["JPY"])
        time.sleep(2)
        print(usde, usd_new)
        change_usd = ((usd_new - float(usde)) / float(usde)) * 100
        change_eur = ((eur_new - float(eur)) / float(eur)) * 100
        change_gbp = ((gbp_new - float(gbp)) / float(gbp)) * 100
        change_jpy = ((jpy_new - float(jpy)) / float(jpy)) * 100
        print(round(change_eur, 2), round(change_usd, 2), round(change_gbp, 2), round(change_jpy, 2)) 
    return render(request, "app/index.html", {"USD": usde, "EUR": eur, "usdd": "1 USD", "GBP": gbp, "JPY": jpy, "change_eur": change_eur,
        "change_usd": change_usd, "change_gbp": change_gbp, "change_jpy": change_jpy})

def stop(request):
    global stop,API_KEY,change_eur,change_gbp,change_usd,change_jpy
    url = f'https://v6.exchangerate-api.com/v6/{API_KEY}/latest/USD'
    response = requests.get(url)
    data = response.json()
    eur = (data["conversion_rates"]["EUR"])
    ils = (data["conversion_rates"]["ILS"]) 
    gbp = (data["conversion_rates"]["GBP"])
    jpy = (data["conversion_rates"]["JPY"])
    stop = False
    return render(request, "app/index.html", {"ILS": ils, "EUR": eur, "usdd": "1 USD", "GBP": gbp, "JPY": jpy, "change_eur": change_eur,
    "change_usd": change_usd, "change_gbp": change_gbp, "change_jpy": change_jpy})



