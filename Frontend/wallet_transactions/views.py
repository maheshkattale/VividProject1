from django.shortcuts import render, redirect, HttpResponse,HttpResponseRedirect
# Create your views here.
import requests
from django.contrib import messages
from rest_framework.response import Response
import json
from rest_framework.generics import GenericAPIView
from helpers.validations import hosturl
# Create your views here.
class deposit(GenericAPIView):
    def get(self,request):

        tok = request.session.get('token', False)
        if tok:
            token = 'Bearer {}'.format(tok)
            headers = {'Authorization':token}
            return render(request, 'admin/wallet_transactions/deposittransactionslist.html',{})
           
        else:
            return redirect('user:login')
        
    def post(self,request):
        tok = request.session.get('token', False)
        if tok:
            token = 'Bearer {}'.format(tok)
            headers = {'Authorization':token}
            get_user_list_url=hosturl+'/api/User/get_user_list'
            p = request.POST.get('p')
            get_user_list_url_pagination_url = get_user_list_url + "?p=" +str(p)     
            get_users_request = requests.post(get_user_list_url_pagination_url,headers=headers, data={})
            get_users_response = get_users_request.json()
            print("get_users_response",get_users_response)
            return HttpResponse(json.dumps(get_users_response), content_type="application/json")
        else:
            return redirect('user:login')

