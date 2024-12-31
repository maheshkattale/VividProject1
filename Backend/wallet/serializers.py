from .models import *
from rest_framework import serializers




class WalletTransactionsSerializer(serializers.ModelSerializer):
    class Meta:
        model= WalletTransactions
        fields='__all__'

class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model= Wallet
        fields='__all__'