from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('get_game_list', get_game_list.as_view(), name = 'get_game_list'),
    path('add_game', add_game.as_view(), name = 'add_game'),
    path('update_game', update_game.as_view(), name = 'update_game'),
    path('delete_game', delete_game.as_view(), name = 'delete_game'),
    path('get_by_id_game', get_by_id_game.as_view(), name = 'get_by_id_game'),
    path('get_games', get_games.as_view(), name = 'get_games'),
   
]