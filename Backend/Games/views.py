from django.shortcuts import render
from User.models import User
# Create your views here.
from rest_framework.authentication import (BaseAuthentication,
                                           get_authorization_header)
from rest_framework import permissions

from rest_framework.response import Response
import json
from rest_framework.generics import GenericAPIView
from django.contrib.auth import authenticate
from .models import *
from .serializers import *
from User.jwt import userJWTAuthentication
from django.template.loader import get_template, render_to_string
from django.core.mail import EmailMessage
from matka.settings import EMAIL_HOST_USER
from django.contrib.auth.hashers import make_password,check_password
import firebase_admin
import os
from matka.settings import BASE_DIR
from User.custom_function import *


import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

# Create your views here.
class get_game_list(GenericAPIView):
    authentication_classes=[userJWTAuthentication]
    permission_classes = (permissions.IsAuthenticated,)
    pagination_class=CustomPagination
    def post(self,request):
        objs = GameMaster.objects.filter(isActive=True).order_by('id')
        print("objs",objs)
        if objs.exists():
            page = self.paginate_queryset(objs)               
            serializer = GameMasterSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)  
        else:
            return Response({"data":[],"response": {"n": 0, "msg": "No game  found ","status": "faliure"}})



class get_games(GenericAPIView):
    authentication_classes=[userJWTAuthentication]
    permission_classes = (permissions.IsAuthenticated,)
    pagination_class=CustomPagination
    def post(self,request):
        objs = GameMaster.objects.filter(isActive=True).order_by('id')
        print("objs",objs)
        if objs.exists():
            serializer = GameMasterSerializer(objs, many=True)
            return Response({"data":serializer.data,"response": {"n": 1, "msg": " game  found ","status": "success"}})
        else:
            return Response({"data":[],"response": {"n": 0, "msg": "No game  found ","status": "faliure"}})


class add_game(GenericAPIView):
    authentication_classes=[userJWTAuthentication]
    permission_classes = (permissions.IsAuthenticated,)
    def post(self,request):
        data=request.data.copy()

        data['isActive'] = True
        obj = GameMaster.objects.filter(isActive=True, gamename=data['gamename']).first() 
  
        if obj is not None:        
            return Response({"data":'',"response": {"n": 0, "msg": "game name already exists", "Status": "Failed"}})
   
        else:
            serializer = GameMasterSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response({"data":serializer.data,"response": {"n": 1, "msg": "game added successfully","status":"success"}})
            else:

                first_key, first_value = next(iter(serializer.errors.items()))
                return Response({"data":'',"response": {"n": 0, "msg":first_key + ' : '+first_value[0],"status": "failure"}})
    



class update_game(GenericAPIView):
    authentication_classes=[userJWTAuthentication]
    permission_classes = (permissions.IsAuthenticated,)
    def post(self,request):
        data=request.data.copy()

        data['isActive'] = True
        update_obj=GameMaster.objects.filter(id=data['game_id'],isActive=True).first()
        if update_obj is not None:

            obj = GameMaster.objects.filter(isActive=True, gamename=data['gamename']).exclude(id=update_obj.id).first() 
    
            if obj is not None:        
                return Response({"data":'',"response": {"n": 0, "msg": "game name already exists", "Status": "Failed"}})
    
            else:
                serializer = GameMasterSerializer(update_obj,data=data)
                if serializer.is_valid():
                    serializer.save()
                    return Response({"data":serializer.data,"response": {"n": 1, "msg": "game updated successfully","status":"success"}})
                else:

                    first_key, first_value = next(iter(serializer.errors.items()))
                    return Response({"data":'',"response": {"n": 0, "msg":first_key + ' : '+first_value[0],"status": "failure"}})
    
        else:
            
            return Response({"data":'',"response": {"n": 0, "msg":'game not found',"status": "failure"}})

class delete_game(GenericAPIView):
    authentication_classes=[userJWTAuthentication]
    permission_classes = (permissions.IsAuthenticated,)
    def post(self,request):
        data=request.data.copy()

        data['isActive'] = False
        delete_obj=GameMaster.objects.filter(id=data['game_id'],isActive=True).first()
        if delete_obj is not None:

            serializer = GameMasterSerializer(delete_obj,data=data)
            if serializer.is_valid():
                serializer.save()
                return Response({"data":serializer.data,"response": {"n": 1, "msg": "game deleted successfully","status":"success"}})
            else:

                first_key, first_value = next(iter(serializer.errors.items()))
                return Response({"data":'',"response": {"n": 0, "msg":first_key + ' : '+first_value[0],"status": "failure"}})
    
        else:
            
            return Response({"data":'',"response": {"n": 0, "msg":'game not found',"status": "failure"}})

class get_by_id_game(GenericAPIView):
    authentication_classes=[userJWTAuthentication]
    permission_classes = (permissions.IsAuthenticated,)
    def post(self,request):
        data=request.data.copy()

        data['isActive'] = False
        get_by_id_obj=GameMaster.objects.filter(id=data['game_id'],isActive=True).first()
        if get_by_id_obj is not None:

            serializer = GameMasterSerializer(get_by_id_obj)
            return Response({"data":serializer.data,"response": {"n": 1, "msg": "game found successfully","status":"success"}})
        else:
            return Response({"data":'',"response": {"n": 0, "msg":'game not found',"status": "failure"}})


