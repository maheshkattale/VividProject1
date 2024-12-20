from django.contrib import admin
from django.urls import path
from .views import *


urlpatterns = [


    path('deposit', deposit.as_view(), name = 'deposit'),

    
]
