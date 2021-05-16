import sys

from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.shortcuts import render
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token

from rest_framework.response import Response

from .models import AccountDetails,TransactionDetails
from .serializer import UserCreationSerializer,BankAccountCreationSerializer,DepositSerializer,WithdrawSerializer,LoginSerializer,TransactionSerializer
from rest_framework import mixins,generics,status,permissions
from rest_framework.views import APIView

# Create your views here.

class UserCreationMixin(mixins.CreateModelMixin,generics.GenericAPIView):
    serializer_class = UserCreationSerializer
    def post(self,request):
        return self.create(request)


class BankAccountCreationApi(mixins.CreateModelMixin,generics.GenericAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = BankAccountCreationSerializer
    def post(self, request):
        account = AccountDetails.objects.last()
        if account:
            accno = account.accno + 1
        else:
            accno = 1000
        request.data["accno"]=accno
        serializer=BankAccountCreationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class DepositApi(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    def post(self,request,accno):
        serializer=DepositSerializer(data=request.data)
        account = AccountDetails.objects.get(accno=accno)

        if serializer.is_valid():
            if account:
                amount=serializer.validated_data.get("amount")
                account.balance+=amount
                account.save()
                return Response({"message":"amount Credited, Balance is "+str(account.balance)})
            else:
                return Response({"message":"Account Number Doesn't Exist"})

        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class WithdrawApi(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    def post(self,request,accno):
        serializer=WithdrawSerializer(data=request.data)
        account=AccountDetails.objects.get(accno=accno)
        if serializer.is_valid():
            amount=serializer.validated_data.get("amount")
            if amount<account.balance:
                account.balance-=amount
                account.save()
                return Response({"message":"Amount debited, Balance : "+str(account.balance)})
            else:
                return Response({"message": "Insufficient Balance, Balance : " + str(account.balance)})
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class BalanceCheckApi(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    def get(self,request,accno):
        account=AccountDetails.objects.get(accno=accno)
        return Response({"message":"accno:"+str(account.accno)+" balance is "+str(account.balance)})


class LoginApi(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            print("works")
            username = serializer.validated_data.get("username")
            password = serializer.validated_data.get("password")
            # user = authenticate(request, username=username, password=password)
            user = User.objects.get(username=username)
            if (user.username == username) & (user.password == password):
                login(request, user)
                token, created = Token.objects.get_or_create(user=user)
                return Response({"token": token.key}, status=status.HTTP_204_NO_CONTENT)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutApi(APIView):
    def get(self, request):
        logout(request)
        return Response({"message": "user logged out"})
        # request.user.auth_token.delete()


class TransactionApi(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    def post(self,request,accno):
        fromaccount=AccountDetails.objects.get(accno=accno)
        request.data["fromaccno"]=accno
        print(request.data)
        serializer=TransactionSerializer(data=request.data)
        if serializer.is_valid():
            amount=serializer.validated_data.get("amount")
            toaccno=serializer.validated_data.get("toaccno")

            toaccount=AccountDetails.objects.get(accno=toaccno)
            if((fromaccount.balance>=amount)&(toaccno==toaccount.accno)):
                fromaccount.balance-=amount
                toaccount.balance+=amount
                fromaccount.save()
                toaccount.save()
                serializer.save()
                return Response(serializer.data,status=status.HTTP_201_CREATED)
            else:
                return Response({"message":"insufficient balance"})

        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class TransactionHistoryApi(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    def get(self,request,accno):
        transaction=TransactionDetails.objects.filter(toaccno=accno) | TransactionDetails.objects.filter(fromaccno=accno)
        serializer=TransactionSerializer(transaction,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

class CreditTransaction(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    def get(self,request,accno):
        credit=TransactionDetails.objects.filter(toaccno=accno)
        serializer=TransactionSerializer(credit,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

class DebitTransaction(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    def get(self,request,accno):
        debit=TransactionDetails.objects.filter(fromaccno=accno)
        serializer=TransactionSerializer(debit,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)