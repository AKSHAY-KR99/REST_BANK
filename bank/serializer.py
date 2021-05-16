from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from bank.models import AccountDetails,TransactionDetails
from django.contrib.auth.models import User

class UserCreationSerializer(ModelSerializer):
    class Meta:
        model=User
        fields=['first_name', 'last_name', 'username', 'password']


class BankAccountCreationSerializer(ModelSerializer):
    class Meta:
        model=AccountDetails
        fields='__all__'


class WithdrawSerializer(serializers.Serializer):
    amount=serializers.IntegerField()

class DepositSerializer(serializers.Serializer):
    amount=serializers.IntegerField()

class LoginSerializer(serializers.Serializer):
    username=serializers.CharField()
    password=serializers.CharField()

class TransactionSerializer(ModelSerializer):
    class Meta:
        model=TransactionDetails
        fields='__all__'
