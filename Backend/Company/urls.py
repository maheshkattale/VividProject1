from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('get_company_list', get_company_list.as_view(), name = 'get_company_list'),
    path('add_company', add_company.as_view(), name = 'add_company'),
    path('update_company', update_company.as_view(), name = 'update_company'),
    path('delete_company', delete_company.as_view(), name = 'delete_company'),
    path('get_by_id_company', get_by_id_company.as_view(), name = 'get_by_id_company'),
    path('get_company_games', get_company_games.as_view(), name = 'get_company_games'),
    path('get_company_gamesids', get_company_gamesids.as_view(), name = 'get_company_gamesids'),
   
]