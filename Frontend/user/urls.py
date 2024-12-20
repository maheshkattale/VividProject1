from django.contrib import admin
from django.urls import path
from .views import *


urlpatterns = [
    path('', login.as_view(), name = 'login'),
    path('logout', logout.as_view(), name = 'logout'),
    path('login', login.as_view(), name = 'login_page'),
    path('dashboard', dashboard.as_view(), name = 'dashboard'),

    path('get_user_list', get_user_list.as_view(), name = 'get_user_list'),

    path('delete_user', delete_user.as_view(), name = 'delete_user'),
    
]
