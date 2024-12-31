from .models import *
from rest_framework import serializers




class CompanyMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model= CompanyMaster
        fields='__all__'

class CompanyGamesSerializer(serializers.ModelSerializer):
    class Meta:
        model= CompanyGames
        fields='__all__'
