from django.contrib import admin
from django.urls import path
from .views import *


urlpatterns = [


    path('deposit_transactions', deposit_transactions.as_view(), name = 'deposit_transactions'),
    path('withdraw_transactions', withdraw_transactions.as_view(), name = 'withdraw_transactions'),

    path('accept_deposit_request', accept_deposit_request.as_view(), name = 'accept_deposit_request'),
    path('reject_deposit_request', reject_deposit_request.as_view(), name = 'reject_deposit_request'),
    path('accept_withdraw_request', accept_withdraw_request.as_view(), name = 'accept_withdraw_request'),
    path('reject_withdraw_request', reject_withdraw_request.as_view(), name = 'reject_withdraw_request'),
    
]
