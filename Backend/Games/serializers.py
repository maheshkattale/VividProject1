from .models import *
from rest_framework import serializers




class GameMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model= GameMaster
        fields='__all__'
