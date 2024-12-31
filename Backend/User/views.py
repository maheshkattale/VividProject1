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
from .jwt import userJWTAuthentication
from django.template.loader import get_template, render_to_string
from django.core.mail import EmailMessage
from matka.settings import EMAIL_HOST_USER
from django.contrib.auth.hashers import make_password,check_password
import firebase_admin
import os
from matka.settings import BASE_DIR
from .custom_function import *


import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

# Firebase configuration
FIREBASE_API_KEY = "AIzaSyBJ9YtS5NChm7I_6D43f138kIgnabALeh0"


class SendOTP(GenericAPIView):
    permission_classes = [AllowAny]  # Allows public access to this endpoint

    def post(self, request):
        try:
            # Parse the request body to get the phone number and recaptcha token
            body = request.data  # Use DRF's request.data for JSON parsing
            phone_number = body.get("phone_number")
            print("phone_number",phone_number)
            recaptcha_token = body.get("recaptcha_token")

            if not phone_number:
                return Response({"status": "error", "message": "Phone number is required"}, status=400)

            if not recaptcha_token:
                return Response({"status": "error", "message": "Recaptcha token is required"}, status=400)

            # Firebase endpoint for sending OTP
            firebase_url = f"https://identitytoolkit.googleapis.com/v1/accounts:sendVerificationCode?key={FIREBASE_API_KEY}"

            # Request payload
            payload = {
                "phoneNumber": phone_number,
                "recaptchaToken": recaptcha_token
            }

            # Send POST request to Firebase
            response = requests.post(firebase_url, json=payload)
            response_data = response.json()

            if response.status_code == 200:
                return Response({"status": "success", "sessionInfo": response_data.get("sessionInfo")}, status=200)
            else:
                return Response({"status": "error", "message": response_data.get("error", {}).get("message", "Failed to send OTP")}, status=400)

        except Exception as e:
            return Response({"status": "error", "message": str(e)}, status=500)



class login(GenericAPIView):
    def post(self,request):
        Username = request.POST.get("mobileNumber")
        Password = request.data.get("password")
    
        if Username is None or Password is None:
            return Response( {
                    "data" : {'token':'','username':'','user_id':'','Menu':[]},
                    "response":{
                    "status":"error",
                    'msg': 'Please provide mobile number and password',
                    'n':0
                    }})
        userexist = User.objects.filter(Username=Username, isActive=True).first()
        if userexist is None:
           return Response(
                    {
                    "data" : {'token':'','username':'','user_id':'','Menu':[]},
                    "response":{
                    "status":"error",
                    'msg': 'This user is not found',
                    'n':0
                    }}
                           )
        else:
            user_serializer=UserSerializer(userexist)
            p = check_password(Password,userexist.password)
            if p is False:
                return Response({
                    "data" : {'token':'','username':'','user_id':'','Menu':[]},
                    "response":{
                    "status":"error",
                    'msg': 'Please enter correct password',
                    'n':0
                    }})
            else:
                useruuid = str(userexist.id)
                username = userexist.Username
                userdata = User.objects.filter(Username=Username,isActive=True).first()
               
                tokenexist = UserToken.objects.filter(User=useruuid,isActive=True).first()
                if tokenexist is not None:
                
                    tokenupdate = UserToken.objects.filter(User=useruuid,isActive=True).update(isActive=False)
                    createtoken = UserToken.objects.create(User=useruuid,authToken=userdata.token)
                else:
                    createtoken = UserToken.objects.create(User=useruuid,authToken=userdata.token)

                TokenObj=UserToken.objects.filter(User=useruuid,isActive=True).first()
                userobj = User.objects.filter(id=TokenObj.User).first()
                name = userobj.Username
                
                return Response({
                    "data" : {'token':createtoken.authToken,'username':name,'user_id':useruuid},
                    "response":{
                    "n": 1 ,
                    "msg" : "login successful",
                    "status":"success"
                    }
                })
          



class logout(GenericAPIView):
    authentication_classes=[userJWTAuthentication]
    permission_classes = (permissions.IsAuthenticated,)
    def post(self,request):
        logouttoken = request.data.get('logouttoken')
        print("logouttoken1",logouttoken)

        if logouttoken is None or logouttoken =='':
            logouttoken=request.session.get('token')
            print("logouttoken2",logouttoken)

        objectd = UserToken.objects.filter(authToken=logouttoken,isActive=True).first()
        if objectd is not None:
            tokenfalse = UserToken.objects.filter(authToken=logouttoken,isActive=True).update(isActive=False)
            return Response({
                            "data" : '',
                            "response":{
                            "n": 1 ,
                            "msg" : "logout successful",
                            "status":"success"
                            }
                        })
        else:
            return Response({
                            "data" : '',
                            "response":{
                            "n": 0,
                            "msg" : "logout unsuccessful",
                            "status":"failed"
                            }
                        })


    

class ChangePassword(GenericAPIView):
    authentication_classes=[userJWTAuthentication]
    permission_classes = (permissions.IsAuthenticated,)
    def post(self,request):
        data = {}
        id = request.user.id
        if id is not None:
            userObject = User.objects.filter(id=id,isActive=True).first()
        
            if userObject:
                password = request.POST.get('oldpassword')
                currentPassword = check_password(password,userObject.password)
            
                if currentPassword==True:
                    newpassword = request.POST.get('newpassword')
                
                    confirmpassword = request.POST.get('confirmpassword')
                
                    if newpassword==confirmpassword:
                        data['password']= make_password(newpassword)
                        data['textPassword'] = newpassword
                        userSerializer = UserSerializer(userObject,data=data,partial=True)
                        if userSerializer.is_valid():
                            userSerializer.save()

                            tokenfalse = UserToken.objects.filter(User=id,isActive=True).update(isActive=False)
                           
                            return Response({"data":'',"response": {"n": 1, "msg": "password updated successfully","status": "success"}})
                        else:
                            return Response({"data":'',"response": {"n": 0, "msg": "password not updated ","status": "failed"}})
                    else:
                        return Response({"data":'',"response": {"n": 0, "msg": "new and confirm password not matched ","status": "failed"}})
                else:
                    return Response({"data":'',"response": {"n": 0, "msg": "old password is wrong","status": "failed"}})

        else:
            return Response({"data":'',"response": {"n": 0, "msg": "Couldnt find id","status": "failed"}})



class forgetpasswordmail(GenericAPIView):
    def post(self,request):
        data={}
        data['Email']=request.data.get('Email')
        userdata = User.objects.filter(email=data['Email'],isActive=True,PasswordSet=True).first()
        if userdata is not None:
            email =   data['Email']
            data2 = {'user_id':userdata.id,'user_email':userdata.email}
            html_mail = render_to_string('mails/reset_password.html',data2)
            
            mailMsg = EmailMessage(
                'Forgot Password?',
                html_mail,
                'no-reply@onerooftech.com',
                [email],
                )
            mailMsg.content_subtype ="html"
            mailsend = mailMsg.send()
           
            return Response({"data":{},"response":{"n": 1,"msg":"Email Sent Successfully!", "status":"success" }})
        else:
            return Response({"data":{},"response":{"n": 0,"msg" : "User not found", "status":"error"}})


class setnewpassword(GenericAPIView):
    def post(self,request):
        data={}
        data['id']=request.data.get('id')
        print("id",data['id'])
        empdata = User.objects.filter(id=data['id'],isActive=True).first()
        if empdata is not None:
            data['Password']=request.data.get('Password')
            data['cfpassword']=request.data.get('cfpassword')
            userpassword = data['Password']
            if data['Password'] != data['cfpassword']:
                return Response({"data":{},"response":{"n": 0 ,"msg":"Passwords do not match","status":"passwords do not match"}})
            else:
                data['password']=make_password(userpassword)
                data['textPassword'] = userpassword
                data['PasswordSet'] = True
                serializer = UserSerializer(empdata,data=data,partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response({"data" : serializer.data,"response":{"n":1,"msg":"Password set Successfully!","status":"success"}})
                else:
                    return Response({"data" : serializer.errors,"response":{"n":0,"msg":"serializer is not valid","status":"failure"}})
        else:
            return Response({ "data":{},"response":{"n":0,"msg":"user not found", "status":"failure"}})


class resetpassword(GenericAPIView):
    authentication_classes=[userJWTAuthentication]
    permission_classes = (permissions.IsAuthenticated,)
    def post(self,request):
        data={}
        data['id']=request.data.get('id')
        empdata = User.objects.filter(id=data['id'],isActive=True,PasswordSet=True).first()
        if empdata is not None:
            data['Password']=request.data.get('Password')
            data['cfpassword']=request.data.get('cfpassword')
            userpassword = data['Password']
            if data['Password'] != data['cfpassword']:
                return Response({"data":{},"response":{"n": 0 ,"msg":"Passwords do not match","status":"passwords do not match"}})
            else:
                data['password']=make_password(userpassword)
                data['textPassword'] = userpassword
                serializer = UserSerializer(empdata,data=data,partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response({"data" : serializer.data,"response":{"n":1,"msg":"Password Reset Successfully!","status":"success"}})
                else:
                    return Response({"data" : serializer.errors,"response":{"n":0,"msg":"serializer is not valid","status":"failure"}})
        else:
            return Response({ "data":{},"response":{"n":0,"msg":"user not found", "status":"failure"}})
        


class createuser(GenericAPIView):
    # authentication_classes=[userJWTAuthentication]
    # permission_classes = (permissions.IsAuthenticated,)
    def post(self,request):
        data={}
        # data['Username']=request.data.get('Username')
        data['textPassword']=request.data.get('textPassword')
        data['mobileNumber']=request.data.get('mobileNumber')
        data['Username']=request.data.get('mobileNumber')
        data['email']=request.data.get('email')
        data['password'] = data['textPassword']
        data['isActive'] = True
        usernameobj = User.objects.filter(isActive=True, Username=data['Username']).first()
        mobileobj = User.objects.filter(isActive=True, mobileNumber=data['mobileNumber']).first()        
              
        if mobileobj is not None:        
            return Response({"data":'',"response": {"n": 0, "msg": "mobile already exist", "Status": "Failed"}})
        elif usernameobj is not None:
            return Response({"data":'',"response": {"n": 0, "msg": "username already exist", "Status": "Failed"}})  
        else:
            serializer = UserSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response({"data":serializer.data,"response": {"n": 1, "msg": "user registered successfully","status":"success"}})
            else:
                return Response({"data":serializer.errors,"response": {"n": 0, "msg": "user not registered successfully","status":"failure"}})
                
        
class userlist(GenericAPIView):
    authentication_classes=[userJWTAuthentication]
    permission_classes = (permissions.IsAuthenticated,)
    def get(self,request):
        empobjects = User.objects.filter(isActive=True).order_by('id')
        serializer = UserlistSerializer(empobjects, many=True)
        return Response({"data":serializer.data,"response": {"n": 1, "msg": "user list shown successfully","status": "success"}})

class get_user_by_id(GenericAPIView):
    authentication_classes=[userJWTAuthentication]
    permission_classes = (permissions.IsAuthenticated,)
    def post(self,request):
        id=request.data.get('id')
        empobjects = User.objects.filter(id=id,isActive=True).first()
        if empobjects is not None:

            serializer = UserlistSerializer(empobjects)
            return Response({"data":serializer.data,"response": {"n": 1, "msg": "user found successfully","status": "success"}})
        else:
            return Response({"data":{},"response": {"n": 0, "msg": "user not found","status": "error"}})

class update_user(GenericAPIView):
    authentication_classes=[userJWTAuthentication]
    permission_classes = (permissions.IsAuthenticated,)
    def post(self,request):
        id=request.data.get('id')
        data=request.data.copy()
        empobjects = User.objects.filter(id=id,isActive=True).first()
        if empobjects is not None:
            serializer = UserSerializer(empobjects,data=data,partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({"data":serializer.data,"response": {"n": 1, "msg": "user updated successfully","status": "success"}})

            else:
                first_key, first_value = next(iter(serializer.errors.items()))
                return Response({"data":'',"response": {"n": 0, "msg":first_key + ' : '+first_value[0],"status": "failure"}})
        else:
            return Response({"data":{},"response": {"n": 0, "msg": "user not found","status": "error"}})
        
class delete_user(GenericAPIView):
    authentication_classes=[userJWTAuthentication]
    permission_classes = (permissions.IsAuthenticated,)
    def post(self,request):
        id=request.data.get('id')
        data={}
        data['isActive']=False
        empobjects = User.objects.filter(id=id,isActive=True).first()
        if empobjects is not None:
            serializer = UserSerializer(empobjects,data=data,partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({"data":serializer.data,"response": {"n": 1, "msg": "user deleted successfully","status": "success"}})
            else:
                first_key, first_value = next(iter(serializer.errors.items()))
                return Response({"data":'',"response": {"n": 0, "msg":first_key + ' : '+first_value[0],"status": "failure"}})
        else:
            return Response({"data":{},"response": {"n": 0, "msg": "user not found","status": "error"}})


class get_user_list(GenericAPIView):
    authentication_classes=[userJWTAuthentication]
    permission_classes = (permissions.IsAuthenticated,)
    pagination_class=CustomPagination
    def post(self,request):
        empobjects = User.objects.filter(isActive=True).order_by('id')
        if empobjects.exists():

            page = self.paginate_queryset(empobjects)               
            serializer = UserlistSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)  
        else:
            return Response({"data":[],"response": {"n": 0, "msg": "No users  found ","status": "faliure"}})
























