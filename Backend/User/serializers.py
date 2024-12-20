from .models import *
from rest_framework import serializers


class UserlistSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields ="__all__"
       

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model= User
        fields='__all__'
