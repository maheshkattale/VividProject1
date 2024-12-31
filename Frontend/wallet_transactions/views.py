from django.shortcuts import render, redirect, HttpResponse,HttpResponseRedirect
# Create your views here.
import requests
from django.contrib import messages
from rest_framework.response import Response
import json
from rest_framework.generics import GenericAPIView
from helpers.validations import hosturl
# Create your views here.
class deposit_transactions(GenericAPIView):
    def get(self,request):

        tok = request.session.get('token', False)
        if tok:
            token = 'Bearer {}'.format(tok)
            headers = {'Authorization':token}
            return render(request, 'admin/wallet_transactions/deposit_transactions_list.html',{})
           
        else:
            return redirect('user:login')
        
    def post(self,request):
        tok = request.session.get('token', False)
        if tok:
            token = 'Bearer {}'.format(tok)
            headers = {'Authorization':token}
            get_deposit_transactions_list_url=hosturl+'/api/Wallet/get_deposit_transactions_list'
            p = request.POST.get('p')
            data=request.data.copy()
            get_deposit_transactions_list_url_pagination_url = get_deposit_transactions_list_url + "?p=" +str(p)     
            get_deposit_transactionss_request = requests.post(get_deposit_transactions_list_url_pagination_url,headers=headers, data=data)
            get_deposit_transactionss_response = get_deposit_transactionss_request.json()
            return HttpResponse(json.dumps(get_deposit_transactionss_response), content_type="application/json")
        else:
            return redirect('user:login')

class accept_deposit_request(GenericAPIView):

        
    def post(self,request):
        tok = request.session.get('token', False)
        if tok:
            token = 'Bearer {}'.format(tok)
            headers = {'Authorization':token}
            accept_deposit_request_url=hosturl+'/api/Wallet/accept_deposit_request'
            data=request.data.copy()
            accept_deposit_requests_request = requests.post(accept_deposit_request_url,headers=headers, data=data)
            accept_deposit_requests_response = accept_deposit_requests_request.json()
            return HttpResponse(json.dumps(accept_deposit_requests_response), content_type="application/json")
        else:
            return redirect('user:login')


class reject_deposit_request(GenericAPIView):

        
    def post(self,request):
        tok = request.session.get('token', False)
        if tok:
            token = 'Bearer {}'.format(tok)
            headers = {'Authorization':token}
            reject_deposit_request_url=hosturl+'/api/Wallet/reject_deposit_request'
            data=request.data.copy()
            reject_deposit_requests_request = requests.post(reject_deposit_request_url,headers=headers, data=data)
            reject_deposit_requests_response = reject_deposit_requests_request.json()
            return HttpResponse(json.dumps(reject_deposit_requests_response), content_type="application/json")
        else:
            return redirect('user:login')

class withdraw_transactions(GenericAPIView):
    def get(self,request):

        tok = request.session.get('token', False)
        if tok:
            token = 'Bearer {}'.format(tok)
            headers = {'Authorization':token}
            return render(request, 'admin/wallet_transactions/withdraw_transactions_list.html',{})
           
        else:
            return redirect('user:login')
        
    def post(self,request):
        tok = request.session.get('token', False)
        if tok:
            token = 'Bearer {}'.format(tok)
            headers = {'Authorization':token}
            get_withdraw_transactions_list_url=hosturl+'/api/Wallet/get_withdraw_transactions_list'
            p = request.POST.get('p')
            data=request.data.copy()
            get_withdraw_transactions_list_url_pagination_url = get_withdraw_transactions_list_url + "?p=" +str(p)     
            get_withdraw_transactionss_request = requests.post(get_withdraw_transactions_list_url_pagination_url,headers=headers, data=data)
            get_withdraw_transactionss_response = get_withdraw_transactionss_request.json()
            return HttpResponse(json.dumps(get_withdraw_transactionss_response), content_type="application/json")
        else:
            return redirect('user:login')


class accept_withdraw_request(GenericAPIView):

        
    def post(self,request):
        tok = request.session.get('token', False)
        if tok:
            token = 'Bearer {}'.format(tok)
            headers = {'Authorization':token}
            accept_withdraw_request_url=hosturl+'/api/Wallet/accept_withdraw_request'
            data=request.data.copy()
            accept_withdraw_requests_request = requests.post(accept_withdraw_request_url,headers=headers, data=data)
            accept_withdraw_requests_response = accept_withdraw_requests_request.json()
            return HttpResponse(json.dumps(accept_withdraw_requests_response), content_type="application/json")
        else:
            return redirect('user:login')


class reject_withdraw_request(GenericAPIView):

        
    def post(self,request):
        tok = request.session.get('token', False)
        if tok:
            token = 'Bearer {}'.format(tok)
            headers = {'Authorization':token}
            reject_withdraw_request_url=hosturl+'/api/Wallet/reject_withdraw_request'
            data=request.data.copy()
            reject_withdraw_requests_request = requests.post(reject_withdraw_request_url,headers=headers, data=data)
            reject_withdraw_requests_response = reject_withdraw_requests_request.json()
            return HttpResponse(json.dumps(reject_withdraw_requests_response), content_type="application/json")
        else:
            return redirect('user:login')
