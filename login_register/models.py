from django.db import models
from django.urls import reverse





class Login(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    def __str__(self):
        return self.username
    


class DataBaseCurrencys(models.Model):
    currencys = models.JSONField(default=dict)  
    def __str__(self):
        return str(self.currencys)

