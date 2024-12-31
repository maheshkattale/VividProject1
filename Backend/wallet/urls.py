from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [

    path('get_deposit_transactions_list', get_deposit_transactions_list.as_view(), name = 'get_deposit_transactions_list'),
    path('get_withdraw_transactions_list', get_withdraw_transactions_list.as_view(), name = 'get_withdraw_transactions_list'),
    path('get_transactions_list', get_transactions_list.as_view(), name = 'get_transactions_list'),
    path('add_wallet_money', add_wallet_money.as_view(), name = 'add_wallet_money'),
    path('withdraw_wallet_money', withdraw_wallet_money.as_view(), name = 'withdraw_wallet_money'),
    path('get_user_wallet_transactions', get_user_wallet_transactions.as_view(), name = 'get_user_wallet_transactions'),
    path('get_user_wallet_balence_amount', get_user_wallet_balence_amount.as_view(), name = 'get_user_wallet_balence_amount'),
    path('accept_deposit_request', accept_deposit_request.as_view(), name = 'accept_deposit_request'),
    path('reject_deposit_request', reject_deposit_request.as_view(), name = 'reject_deposit_request'),    
    path('accept_withdraw_request', accept_withdraw_request.as_view(), name = 'accept_withdraw_request'),
    path('reject_withdraw_request', reject_withdraw_request.as_view(), name = 'reject_withdraw_request'),

   
]