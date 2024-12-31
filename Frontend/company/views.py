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
class company_list(GenericAPIView):
    def get(self,request):

        tok = request.session.get('token', False)
        if tok:
            token = 'Bearer {}'.format(tok)
            headers = {'Authorization':token}
            return render(request, 'admin/company/company_list.html',{})
        else:
            return redirect('user:login')
        

        
    def post(self,request):
        tok = request.session.get('token', False)
        if tok:
            token = 'Bearer {}'.format(tok)
            headers = {'Authorization':token}
            get_company_list_url=hosturl+'/api/Company/get_company_list'
            p = request.POST.get('p')
            get_company_list_url_pagination_url = get_company_list_url + "?p=" +str(p)     
            get_companys_request = requests.post(get_company_list_url_pagination_url,headers=headers, data={})
            get_companys_response = get_companys_request.json()
            print("get_companys_response",get_companys_response)
            return HttpResponse(json.dumps(get_companys_response), content_type="application/json")
        else:
            return redirect('user:login')

# Create your views here.
class add_company(GenericAPIView):
    def get(self,request):

        tok = request.session.get('token', False)
        if tok:
            token = 'Bearer {}'.format(tok)
            headers = {'Authorization':token}
            get_games_list_url=hosturl+'/api/Games/get_games'
            get_games_list_request = requests.post(get_games_list_url,headers=headers, data=request.data.copy())
            get_games_list_response = get_games_list_request.json()
            return render(request, 'admin/company/add_company.html',{'games':get_games_list_response['data']})
        else:
            return redirect('user:login')
        

        
    def post(self,request):
        tok = request.session.get('token', False)
        if tok:
            token = 'Bearer {}'.format(tok)
            headers = {'Authorization':token}
            add_company_url=hosturl+'/api/Company/add_company'
            add_company_request = requests.post(add_company_url,headers=headers, data=request.data.copy())
            add_company_response = add_company_request.json()
            print("add_company_response",add_company_response)
            return HttpResponse(json.dumps(add_company_response), content_type="application/json")
        else:
            return redirect('user:login')

class delete_company(GenericAPIView):

        

        
    def post(self,request):
        tok = request.session.get('token', False)
        if tok:
            token = 'Bearer {}'.format(tok)
            headers = {'Authorization':token}
            delete_company_url=hosturl+'/api/Company/delete_company'
            delete_company_request = requests.post(delete_company_url,headers=headers, data=request.data.copy())
            delete_company_response = delete_company_request.json()
            print("delete_company_response",delete_company_response)
            return HttpResponse(json.dumps(delete_company_response), content_type="application/json")
        else:
            return redirect('user:login')


class update_company(GenericAPIView):
    def get(self,request,id):

        tok = request.session.get('token', False)
        if tok:
            token = 'Bearer {}'.format(tok)
            headers = {'Authorization':token}
            data={}
            data['company_id']=id
            get_by_id_company_url=hosturl+'/api/Company/get_by_id_company'
            get_by_id_company_request = requests.post(get_by_id_company_url,headers=headers,data=data)
            get_by_id_company_response = get_by_id_company_request.json()
            get_games_list_url=hosturl+'/api/Games/get_games'
            get_games_list_request = requests.post(get_games_list_url,headers=headers, data=request.data.copy())
            get_games_list_response = get_games_list_request.json()
            # print("data",data)
            get_company_games_url=hosturl+'/api/Company/get_company_gamesids'
            get_company_games_request = requests.post(get_company_games_url,headers=headers, data=data)
            get_company_games_response = get_company_games_request.json()

            print("get_company_games_response",get_company_games_response['data'])
            return render(request, 'admin/company/update_company.html',{'company':get_by_id_company_response['data'],'games':get_games_list_response['data'],'company_gammes':get_company_games_response['data']})
        else:
            return redirect('user:login')
        

        
    def post(self,request,id):
        tok = request.session.get('token', False)
        if tok:
            token = 'Bearer {}'.format(tok)
            headers = {'Authorization':token}
            data=request.data.copy()
            data['company_id']=id
            update_company_url=hosturl+'/api/Company/update_company'
            update_company_request = requests.post(update_company_url,headers=headers, data=data)
            update_company_response = update_company_request.json()
            print("update_company_response",update_company_response)
            return HttpResponse(json.dumps(update_company_response), content_type="application/json")
        else:
            return redirect('user:login')














