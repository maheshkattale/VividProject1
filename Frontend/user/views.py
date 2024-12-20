from django.shortcuts import render, redirect, HttpResponse,HttpResponseRedirect
# Create your views here.
import requests
from django.contrib import messages
from rest_framework.response import Response
import json
from rest_framework.generics import GenericAPIView
from helpers.validations import hosturl
# Create your views here.
login_url=hosturl+"/api/User/login"
logout_url = hosturl+'/api/User/logout'



# Create your views here.
class login(GenericAPIView):
    def get(self,request):
        return render(request, 'login.html',{})
    def post(self,request):
        mobileNumber = request.POST['mobileNumber']
        password = request.POST['password']
        source = request.POST['source']
        data = {}
        data['mobileNumber'] = mobileNumber
        data['password'] = password
        data['source'] = source
        
        
        login_request = requests.post(login_url, data=data)
        login_response = login_request.json()
        if login_response['response']['n']==0:
            msg = login_response['response']['msg']
            messages.error(request, msg)
            return redirect('user:login')
        else:
            request.session['token'] = login_response['data']['token']
            request.session['username'] = login_response['data']['username']
            request.session['mobileNumber'] = login_response['data']['username']
            request.session['user_id'] = login_response['data']['user_id']
  
        

            return redirect('user:dashboard')


class logout(GenericAPIView):
    def post(self,request):
        try:
            tok = request.session.get('token', False)
            t = 'Token {}'.format(tok)
            headers = {'Authorization': t}
            logout_request = requests.post(logout_url, headers=headers,data={'logouttoken':t})
            logout_response = logout_request.json()
            print("logout_response",logout_response)
            if logout_response['response']['n'] == 1:
                del request.session['token']
                return HttpResponse(json.dumps(logout_response), content_type="application/json")

            else:
                return HttpResponse(json.dumps(logout_response), content_type="application/json")

            
        except Exception as e:
            print("e",e)
            messages.error(request, e)
            return redirect('user:login')




class dashboard(GenericAPIView):
    def get(self,request):
        tok = request.session.get('token', False)
        if tok:
            t = 'Token {}'.format(tok)
            headers = {'Authorization': t}
            data={}
            
            return render(request, 'admin/dashboard/admin_dashboard.html',{})
            
            
        else:
            messages.error(request, 'Session expired please login again')
            return redirect('user:login')
    
class get_user_list(GenericAPIView):
    def get(self,request):

        tok = request.session.get('token', False)
        if tok:
            token = 'Bearer {}'.format(tok)
            headers = {'Authorization':token}
            return render(request, 'admin/usermaster/user_list.html',{})
           
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


class delete_user(GenericAPIView):

    def post(self,request):
        tok = request.session.get('token', False)
        if tok:
            token = 'Bearer {}'.format(tok)
            headers = {'Authorization':token}
            data=request.data.copy()
            delete_user_url=hosturl+'/api/User/delete_user'
            delete_user_request = requests.post(delete_user_url,headers=headers, data=data)
            delete_user_response = delete_user_request.json()
            print("delete_user_response",delete_user_response)
            return HttpResponse(json.dumps(delete_user_response), content_type="application/json")
        else:
            return redirect('user:login')
























