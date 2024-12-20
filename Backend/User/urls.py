from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [

    #authentication
    path('login', login.as_view(), name = 'login'),
    path('logout', logout.as_view(), name = 'logout'),
    path('changepassword', ChangePassword.as_view(), name = 'changepassword'),
    path('forgetpasswordmail', forgetpasswordmail.as_view(), name = 'forgetpasswordmail'),
    path('setnewpassword', setnewpassword.as_view(), name = 'setnewpassword'),
    path('resetpassword', resetpassword.as_view(), name = 'resetpassword'),


    path('createuser', createuser.as_view(), name = 'createuser'),
    path('get_user_by_id', get_user_by_id.as_view(), name = 'get_user_by_id'),
    path('userlist', userlist.as_view(), name = 'userlist'),
    path('update_user', update_user.as_view(), name = 'update_user'),
    path('delete_user', delete_user.as_view(), name = 'delete_user'),
    path('SendOTP', SendOTP.as_view(), name = 'SendOTP'),
    path('get_user_list', get_user_list.as_view(), name = 'get_user_list'),
   
]