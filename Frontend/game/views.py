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
class game_list(GenericAPIView):
    def get(self,request):

        tok = request.session.get('token', False)
        if tok:
            token = 'Bearer {}'.format(tok)
            headers = {'Authorization':token}
            return render(request, 'admin/game/game_list.html',{})
        else:
            return redirect('user:login')
        

        
    def post(self,request):
        tok = request.session.get('token', False)
        if tok:
            token = 'Bearer {}'.format(tok)
            headers = {'Authorization':token}
            get_game_list_url=hosturl+'/api/Games/get_game_list'
            p = request.POST.get('p')
            get_game_list_url_pagination_url = get_game_list_url + "?p=" +str(p)     
            get_games_request = requests.post(get_game_list_url_pagination_url,headers=headers, data={})
            get_games_response = get_games_request.json()
            print("get_games_response",get_games_response)
            return HttpResponse(json.dumps(get_games_response), content_type="application/json")
        else:
            return redirect('user:login')

# Create your views here.
class add_game(GenericAPIView):
    def get(self,request):

        tok = request.session.get('token', False)
        if tok:
            token = 'Bearer {}'.format(tok)
            headers = {'Authorization':token}
            return render(request, 'admin/game/add_game.html',{})
        else:
            return redirect('user:login')
        

        
    def post(self,request):
        tok = request.session.get('token', False)
        if tok:
            token = 'Bearer {}'.format(tok)
            headers = {'Authorization':token}
            add_game_url=hosturl+'/api/Games/add_game'
            add_game_request = requests.post(add_game_url,headers=headers, data=request.data.copy())
            add_game_response = add_game_request.json()
            print("add_game_response",add_game_response)
            return HttpResponse(json.dumps(add_game_response), content_type="application/json")
        else:
            return redirect('user:login')

class delete_game(GenericAPIView):
        
    def post(self,request):
        tok = request.session.get('token', False)
        if tok:
            token = 'Bearer {}'.format(tok)
            headers = {'Authorization':token}
            delete_game_url=hosturl+'/api/Games/delete_game'
            delete_game_request = requests.post(delete_game_url,headers=headers, data=request.data.copy())
            delete_game_response = delete_game_request.json()
            print("delete_game_response",delete_game_response)
            return HttpResponse(json.dumps(delete_game_response), content_type="application/json")
        else:
            return redirect('user:login')


class update_game(GenericAPIView):
    def get(self,request,id):

        tok = request.session.get('token', False)
        if tok:
            token = 'Bearer {}'.format(tok)
            headers = {'Authorization':token}
            data={}
            data['game_id']=id
            get_by_id_game_url=hosturl+'/api/Games/get_by_id_game'
            get_by_id_game_request = requests.post(get_by_id_game_url,headers=headers,data=data)
            get_by_id_game_response = get_by_id_game_request.json()
            return render(request, 'admin/game/update_game.html',{'game':get_by_id_game_response['data']})
        else:
            return redirect('user:login')
        

        
    def post(self,request,id):
        tok = request.session.get('token', False)
        if tok:
            token = 'Bearer {}'.format(tok)
            headers = {'Authorization':token}
            data=request.data.copy()
            data['game_id']=id
            update_game_url=hosturl+'/api/Games/update_game'
            update_game_request = requests.post(update_game_url,headers=headers, data=data)
            update_game_response = update_game_request.json()
            print("update_game_response",update_game_response)
            return HttpResponse(json.dumps(update_game_response), content_type="application/json")
        else:
            return redirect('user:login')














