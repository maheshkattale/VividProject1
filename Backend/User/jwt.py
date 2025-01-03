from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import exceptions
from rest_framework.response import Response
from rest_framework.authentication import (BaseAuthentication,
                                           get_authorization_header)

import jwt
from User.models import User,UserToken
from rest_framework.serializers import ValidationError
from rest_framework import status


class CustomAPIException(ValidationError):
    """
    raises API exceptions with custom messages and custom status codes
    """    
    status_code = 400
    default_code = 'error'    
    def __init__(self, detail, status_code=None):
        self.detail = detail
        if status_code is not None:
            self.status_code = status_code


class userJWTAuthentication(BaseAuthentication):

    def authenticate(self, request):

        auth_header = get_authorization_header(request)

        auth_data = auth_header.decode('utf-8')
        auth_token = auth_data.split(" ")

        if len(auth_token) != 2:
            error_msg = {
                    "data": [],
                    "response": {
                        "n": 0,
                        "msg": 'Token not valid',
                        "Status": "Failed"
                    }
                }
            raise CustomAPIException(error_msg)        

        token = auth_token[1]

        try:
            payload = jwt.decode(
                token, settings.SECRET_KEY, algorithms="HS256")
            Username = payload['Username']
            User_id = payload['id']

            Users = User.objects.get(id=User_id, Username=Username)
            userTok = UserToken.objects.filter(
                authToken=token, User=Users.id, isActive=True).first()
            if userTok is None:
                error_msg = {
                        "data": [],
                        "response": {
                            "n": 0,
                            "msg": 'Token is expired, login again',
                            "status": 'Failed'
                        }
                }
                raise CustomAPIException(error_msg)              
            return (Users, token)

        except jwt.ExpiredSignatureError as ex:
            error_msg = {
                    "data": [],
                    "response": {
                        "n": 0,
                        "msg": 'Token is expired, login again',
                        "Status": "Failed"
                    }
                }
            raise CustomAPIException(error_msg)        

        except jwt.DecodeError as ex:
            error_msg = {
                    "data": [],
                    "response": {
                        "n": 0,
                        "msg": "Token is invalid",
                        "Status": "Failed"
                    }
                }
            raise CustomAPIException(error_msg)        

        except ObjectDoesNotExist as no_user:
            return None

        return super().authenticate(request)
