from django.shortcuts import render
from User.models import User
# Create your views here.
from rest_framework.authentication import (BaseAuthentication,
                                           get_authorization_header)
from rest_framework import permissions
from datetime import datetime
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
class get_deposit_transactions_list(GenericAPIView):
    authentication_classes=[userJWTAuthentication]
    permission_classes = (permissions.IsAuthenticated,)
    pagination_class=CustomPagination
    def post(self,request):
        amount=request.data.get('amount')
        paymenttype=request.data.get('paymenttype')
        transactionid=request.data.get('transactionid')
        transactionstatus=request.data.get('transactionstatus')
        mobilenumber=request.data.get('mobilenumber')
        print("data",request.data)
        objs = WalletTransactions.objects.filter(isActive=True,transactiontype='deposit').order_by('-createdAt')
        if amount is not None and amount !='':
            objs=objs.filter(amount__icontains=amount)
        if paymenttype is not None and paymenttype !='':
            objs=objs.filter(paymenttype__icontains=paymenttype)
        if transactionid is not None and transactionid !='':
            objs=objs.filter(transactionid__icontains=transactionid)

        if transactionstatus is not None and transactionstatus !='':
            objs=objs.filter(transactionstatus=transactionstatus)

        if mobilenumber is not None and mobilenumber !='':
            objs=objs.filter(mobilenumber__icontains=mobilenumber)
        print("objs",objs)
        if objs.exists():
            page = self.paginate_queryset(objs)               
            serializer = WalletTransactionsSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)  
        else:
            return Response({"data":[],"response": {"n": 0, "msg": "No transactions  found ","status": "faliure"}})

class get_withdraw_transactions_list(GenericAPIView):
    authentication_classes=[userJWTAuthentication]
    permission_classes = (permissions.IsAuthenticated,)
    pagination_class=CustomPagination
    def post(self,request):
        amount=request.data.get('amount')
        paymenttype=request.data.get('paymenttype')
        transactionid=request.data.get('transactionid')
        transactionstatus=request.data.get('transactionstatus')
        mobilenumber=request.data.get('mobilenumber')

        objs = WalletTransactions.objects.filter(isActive=True,transactiontype='withdraw').order_by('-createdAt')
        if amount is not None and amount !='':
            objs=objs.filter(amount__icontains=amount)
        if paymenttype is not None and paymenttype !='':
            objs=objs.filter(paymenttype__icontains=paymenttype)
        if transactionid is not None and transactionid !='':
            objs=objs.filter(transactionid__icontains=transactionid)

        if transactionstatus is not None and transactionstatus !='':
            objs=objs.filter(transactionstatus=transactionstatus)

        if mobilenumber is not None and mobilenumber !='':
            objs=objs.filter(mobilenumber__icontains=mobilenumber)
        print("objs",objs)
        if objs.exists():
            page = self.paginate_queryset(objs)               
            serializer = WalletTransactionsSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)  
        else:
            return Response({"data":[],"response": {"n": 0, "msg": "No transactions  found ","status": "faliure"}})

class get_transactions_list(GenericAPIView):
    authentication_classes=[userJWTAuthentication]
    permission_classes = (permissions.IsAuthenticated,)
    pagination_class=CustomPagination
    def post(self,request):
        amount=request.data.get('amount')
        paymenttype=request.data.get('paymenttype')
        transactionid=request.data.get('transactionid')
        transactionstatus=request.data.get('transactionstatus')
        transactiontype=request.data.get('transactiontype')
        mobilenumber=request.data.get('mobilenumber')

        objs = WalletTransactions.objects.filter(isActive=True).order_by('-createdAt')
        if amount is not None and amount !='':
            objs=objs.filter(amount__icontains=amount)
        if paymenttype is not None and paymenttype !='':
            objs=objs.filter(paymenttype__icontains=paymenttype)
        if transactionid is not None and transactionid !='':
            objs=objs.filter(transactionid__icontains=transactionid)

        if transactionstatus is not None and transactionstatus !='':
            objs=objs.filter(transactionstatus=transactionstatus)

        if transactiontype is not None and transactiontype !='':
            objs=objs.filter(transactiontype=transactiontype)
        if mobilenumber is not None and mobilenumber !='':
            objs=objs.filter(mobilenumber__icontains=mobilenumber)

        print("objs",objs)
        if objs.exists():
            page = self.paginate_queryset(objs)               
            serializer = WalletTransactionsSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)  
        else:
            return Response({"data":[],"response": {"n": 0, "msg": "No transactions  found ","status": "faliure"}})

class add_wallet_money(GenericAPIView):
    authentication_classes=[userJWTAuthentication]
    permission_classes = (permissions.IsAuthenticated,)
    def post(self,request):
        data=request.data.copy()
        

        # Get current date and time
        now = datetime.now()

        data['isActive'] = True
        amount=request.data.get('amount')
        paymenttype=request.data.get('paymenttype')
        transactionid=request.data.get('transactionid')
        transactionstatus=request.data.get('transactionstatus')
        data['transactiontype']='deposit'
        data['userid']=str(request.user.id)
        data['mobilenumber']=request.user.mobileNumber
        data['date']=str(now.strftime("%Y-%m-%d"))
        data['time']=str(now.strftime("%H:%M:%S"))
        if amount is not None and amount !='':
            if paymenttype is not None and paymenttype !='':
                if transactionstatus is not None and transactionstatus !='':
                    if transactionstatus == 'completed':
                        if transactionid is not None and transactionid !='':
                            #add money to user wallet and add transation
                            obj = WalletTransactions.objects.filter(isActive=True, transactionid=data['transactionid'],userid=data['userid']).first() 
                            if obj is not None:        
                                return Response({"data":'',"response": {"n": 0, "msg": "Deposit request with this transaction id already exists", "status": "faliure"}})
                            else:
                                serializer = WalletTransactionsSerializer(data=data)
                                if serializer.is_valid():
                                    serializer.save()
                                    user_walet_obj=Wallet.objects.filter(userid=str(request.user.id)).first()
                                    if user_walet_obj is not None:
                                        new_amount=int(user_walet_obj.amount)+int(amount)
                                        user_walet_obj.amount=new_amount
                                        user_walet_obj.save()
                                    else:
                                        Wallet.objects.create(userid=str(request.user.id),amount=amount)

                                    return Response({"data":serializer.data,"response": {"n": 1, "msg": "Money added successfully","status":"success"}})
                                else:

                                    first_key, first_value = next(iter(serializer.errors.items()))
                                    return Response({"data":'',"response": {"n": 0, "msg":first_key + ' : '+first_value[0],"status": "failure"}})
            

                        else:
                            return Response({"data":'',"response": {"n": 0, "msg": "please provide transaction id", "status": "faliure"}})
                    elif transactionstatus == 'pending':
                        if transactionid is not None and transactionid !='':
                            #add transation
                            obj = WalletTransactions.objects.filter(isActive=True, transactionid=data['transactionid'],userid=data['userid']).first() 
                            if obj is not None:        
                                return Response({"data":'',"response": {"n": 0, "msg": "Deposit request with this transaction id already exists", "status": "faliure"}})
                            else:
                                serializer = WalletTransactionsSerializer(data=data)
                                if serializer.is_valid():
                                    serializer.save()
                                    # user_walet_obj=Wallet.objects.filter(userid=str(request.user.id)).first()
                                    # if user_walet_obj is not None:
                                    #     new_amount=int(user_walet_obj.amount)+int(amount)
                                    #     user_walet_obj.amount=new_amount
                                    #     user_walet_obj.save()
                                    # else:
                                    #     Wallet.objects.create(userid=str(request.user.id),amount=amount)

                                    return Response({"data":serializer.data,"response": {"n": 1, "msg": "Deposit request send successfully","status":"success"}})
                                else:

                                    first_key, first_value = next(iter(serializer.errors.items()))
                                    return Response({"data":'',"response": {"n": 0, "msg":first_key + ' : '+first_value[0],"status": "failure"}})
            

                        else:
                            return Response({"data":'',"response": {"n": 0, "msg": "please provide transaction id", "status": "faliure"}})



                    else:
                        return Response({"data":'',"response": {"n": 0, "msg": "please provide valid transaction status", "status": "faliure"}})


                else:
                    return Response({"data":[],"response": {"n": 0, "msg": "please provide transaction status ","status": "faliure"}})

            else:
                return Response({"data":[],"response": {"n": 0, "msg": "please provide transaction payment type ","status": "faliure"}})
        else:
            return Response({"data":[],"response": {"n": 0, "msg": "please provide transaction amount ","status": "faliure"}})

class withdraw_wallet_money(GenericAPIView):
    authentication_classes=[userJWTAuthentication]
    permission_classes = (permissions.IsAuthenticated,)
    def post(self,request):
        data=request.data.copy()
        

        # Get current date and time
        now = datetime.now()

        data['isActive'] = True
        amount=request.data.get('amount')
        paymenttype=request.data.get('paymenttype')
        transactionid=request.data.get('transactionid')
        data['transactionstatus']='pending'
        data['transactiontype']='withdraw'
        data['userid']=str(request.user.id)
        data['mobilenumber']=request.user.mobileNumber
        data['date']=str(now.strftime("%Y-%m-%d"))
        data['time']=str(now.strftime("%H:%M:%S"))
        if amount is not None and amount !='':
            user_walet_obj=Wallet.objects.filter(userid=str(request.user.id)).first()

            if user_walet_obj is not None:
                if int(user_walet_obj.amount) >= int(amount):
                    serializer = WalletTransactionsSerializer(data=data)
                    if serializer.is_valid():
                        serializer.save()
                

                        return Response({"data":serializer.data,"response": {"n": 1, "msg": "withdraw request send successfully","status":"success"}})
                    else:

                        first_key, first_value = next(iter(serializer.errors.items()))
                        return Response({"data":'',"response": {"n": 0, "msg":first_key + ' : '+first_value[0],"status": "failure"}})
                else:
                    return Response({"data":[],"response": {"n": 0, "msg": "sorry requested amount not available  in wallet","status": "faliure"}})

            else:
                return Response({"data":[],"response": {"n": 0, "msg": "sorry requested amount not available  in wallet","status": "faliure"}})

        else:
            return Response({"data":[],"response": {"n": 0, "msg": "please provide transaction amount ","status": "faliure"}})


class get_user_wallet_transactions(GenericAPIView):
    authentication_classes=[userJWTAuthentication]
    permission_classes = (permissions.IsAuthenticated,)
    pagination_class=CustomPagination
    def post(self,request):
        amount=request.data.get('amount')
        paymenttype=request.data.get('paymenttype')
        transactionid=request.data.get('transactionid')
        transactionstatus=request.data.get('transactionstatus')
        transactiontype=request.data.get('transactiontype')
        mobilenumber=request.data.get('mobilenumber')

        objs = WalletTransactions.objects.filter(isActive=True,userid=str(request.user.id)).order_by('-createdAt')
        if amount is not None and amount !='':
            objs=objs.filter(amount__icontains=amount)
        if paymenttype is not None and paymenttype !='':
            objs=objs.filter(paymenttype__icontains=paymenttype)
        if transactionid is not None and transactionid !='':
            objs=objs.filter(transactionid__icontains=transactionid)

        if transactionstatus is not None and transactionstatus !='':
            objs=objs.filter(transactionstatus=transactionstatus)

        if transactiontype is not None and transactiontype !='':
            objs=objs.filter(transactiontype=transactiontype)
        if mobilenumber is not None and mobilenumber !='':
            objs=objs.filter(mobilenumber__icontains=mobilenumber)

        print("objs",objs)
        if objs.exists():
            page = self.paginate_queryset(objs)               
            serializer = WalletTransactionsSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)  
        else:
            return Response({"data":[],"response": {"n": 0, "msg": "No transactions  found ","status": "faliure"}})

class get_user_wallet_balence_amount(GenericAPIView):
    authentication_classes=[userJWTAuthentication]
    permission_classes = (permissions.IsAuthenticated,)
    pagination_class=CustomPagination
    def post(self,request):


        objs = Wallet.objects.filter(isActive=True,userid=str(request.user.id)).first()
    

        print("objs",objs)
        if objs is not None:
                
            serializer = WalletSerializer(objs)
            return Response({"data":serializer.data,"response": {"n": 1, "msg": "Wallet details found ","status": "success"}})
        else:
            return Response({"data":[],"response": {"n": 0, "msg": "No   found ","status": "faliure"}})

class accept_deposit_request(GenericAPIView):
    authentication_classes=[userJWTAuthentication]
    permission_classes = (permissions.IsAuthenticated,)
    def post(self,request):
        data=request.data.copy()
        
        data['transactionstatus'] = 'completed'
        wallet_transactions_id=request.data.get('wallet_transactions_id')

        if wallet_transactions_id is not None and wallet_transactions_id !='':
            obj = WalletTransactions.objects.filter(isActive=True, id=wallet_transactions_id,).first() 
            if obj is not None:        
                serializer = WalletTransactionsSerializer(obj,data=data,partial=True)
                if serializer.is_valid():
                    serializer.save()
                    print("serializer",serializer)
                    user_walet_obj=Wallet.objects.filter(userid=str(serializer.data['userid'])).first()
                    if user_walet_obj is not None:
                        new_amount=int(user_walet_obj.amount)+int(serializer.data['amount'])
                        user_walet_obj.amount=new_amount
                        user_walet_obj.save()
                    else:
                        Wallet.objects.create(userid=str(request.user.id),amount=serializer.data['amount'])
                    return Response({"data":serializer.data,"response": {"n": 1, "msg": "deposit request accepted successfully","status":"success"}})
                else:
                    first_key, first_value = next(iter(serializer.errors.items()))
                    return Response({"data":'',"response": {"n": 0, "msg":first_key + ' : '+first_value[0],"status": "failure"}})
            else:
                return Response({"data":[],"response": {"n": 0, "msg": " transaction request id not found ","status": "faliure"}})
        else:
            return Response({"data":[],"response": {"n": 0, "msg": "please provide transaction request id ","status": "faliure"}})

class reject_deposit_request(GenericAPIView):
    authentication_classes=[userJWTAuthentication]
    permission_classes = (permissions.IsAuthenticated,)
    def post(self,request):
        data=request.data.copy()
        
        data['transactionstatus'] = 'rejected'
        data['rejectionreason'] = request.data.get('rejectionreason')
        wallet_transactions_id=request.data.get('wallet_transactions_id')
        print("daa",data)

        if data['rejectionreason'] is not None and data['rejectionreason'] !='':

            if wallet_transactions_id is not None and wallet_transactions_id !='':
                obj = WalletTransactions.objects.filter(isActive=True, id=wallet_transactions_id,).first() 
                if obj is not None:        
                    serializer = WalletTransactionsSerializer(obj,data=data,partial=True)
                    if serializer.is_valid():
                        serializer.save()
                        print("serializer",serializer)
                    
                        return Response({"data":serializer.data,"response": {"n": 1, "msg": "deposit request rejected successfully","status":"success"}})
                    else:
                        first_key, first_value = next(iter(serializer.errors.items()))
                        return Response({"data":'',"response": {"n": 0, "msg":first_key + ' : '+first_value[0],"status": "failure"}})
                else:
                    return Response({"data":[],"response": {"n": 0, "msg": " transaction request id not found ","status": "faliure"}})
            else:
                return Response({"data":[],"response": {"n": 0, "msg": "please provide transaction request id ","status": "faliure"}})
        else:
            return Response({"data":[],"response": {"n": 0, "msg": "please provide transaction rejection reason ","status": "faliure"}})




class accept_withdraw_request(GenericAPIView):
    authentication_classes=[userJWTAuthentication]
    permission_classes = (permissions.IsAuthenticated,)
    def post(self,request):
        data=request.data.copy()
        
        data['transactionstatus'] = 'completed'
        wallet_transactions_id=request.data.get('wallet_transactions_id')

        if wallet_transactions_id is not None and wallet_transactions_id !='':
            obj = WalletTransactions.objects.filter(isActive=True, id=wallet_transactions_id,).first() 
            if obj is not None:        
                serializer = WalletTransactionsSerializer(obj,data=data,partial=True)
                
                print("serializer",serializer)
                user_walet_obj=Wallet.objects.filter(userid=str(obj.userid)).first()
                if user_walet_obj is not None:
                    new_amount=int(user_walet_obj.amount)-int(obj.amount)
                    if new_amount >0:
                        if serializer.is_valid():
                            serializer.save()
                            user_walet_obj.amount=new_amount
                            user_walet_obj.save()
                            return Response({"data":serializer.data,"response": {"n": 1, "msg": "withdraw request accepted successfully","status":"success"}})
                        else:
                            first_key, first_value = next(iter(serializer.errors.items()))
                            return Response({"data":'',"response": {"n": 0, "msg":first_key + ' : '+first_value[0],"status": "failure"}})
                    else:
                        return Response({"data":[],"response": {"n": 0, "msg": "request amount not available in wallet","status":"failure"}})
                else:
                    return Response({"data":{},"response": {"n": 0, "msg": "request amount not available in wallet","status":"failure"}})

                
            else:
                return Response({"data":[],"response": {"n": 0, "msg": " transaction request id not found ","status": "faliure"}})
        else:
            return Response({"data":[],"response": {"n": 0, "msg": "please provide transaction request id ","status": "faliure"}})

class reject_withdraw_request(GenericAPIView):
    authentication_classes=[userJWTAuthentication]
    permission_classes = (permissions.IsAuthenticated,)
    def post(self,request):
        data=request.data.copy()
        
        data['transactionstatus'] = 'rejected'
        data['rejectionreason'] = request.data.get('rejectionreason')
        wallet_transactions_id=request.data.get('wallet_transactions_id')
        print("daa",data)

        if data['rejectionreason'] is not None and data['rejectionreason'] !='':

            if wallet_transactions_id is not None and wallet_transactions_id !='':
                obj = WalletTransactions.objects.filter(isActive=True, id=wallet_transactions_id,).first() 
                if obj is not None:        
                    serializer = WalletTransactionsSerializer(obj,data=data,partial=True)
                    if serializer.is_valid():
                        serializer.save()
                        print("serializer",serializer)
                    
                        return Response({"data":serializer.data,"response": {"n": 1, "msg": "withdraw request rejected successfully","status":"success"}})
                    else:
                        first_key, first_value = next(iter(serializer.errors.items()))
                        return Response({"data":'',"response": {"n": 0, "msg":first_key + ' : '+first_value[0],"status": "failure"}})
                else:
                    return Response({"data":[],"response": {"n": 0, "msg": " transaction request id not found ","status": "faliure"}})
            else:
                return Response({"data":[],"response": {"n": 0, "msg": "please provide transaction request id ","status": "faliure"}})
        else:
            return Response({"data":[],"response": {"n": 0, "msg": "please provide transaction rejection reason ","status": "faliure"}})






