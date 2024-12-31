from django.contrib import admin
from django.urls import path
from .views import *


urlpatterns = [
    path('game_list', game_list.as_view(), name = 'game_list'),
    path('add_game', add_game.as_view(), name = 'add_game'),
    path('delete_game', delete_game.as_view(), name = 'delete_game'),
    path('update_game/<str:id>', update_game.as_view(), name = 'update_game'),
   
]
