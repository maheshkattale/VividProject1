from django.contrib import admin
from django.urls import path
from .views import *


urlpatterns = [
    path('company_list', company_list.as_view(), name = 'company_list'),
    path('add_company', add_company.as_view(), name = 'add_company'),
    path('delete_company', delete_company.as_view(), name = 'delete_company'),
    path('update_company/<str:id>', update_company.as_view(), name = 'update_company'),
   
]
