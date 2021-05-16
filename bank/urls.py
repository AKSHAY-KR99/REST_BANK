"""rest_Bank URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from .views import UserCreationMixin, BankAccountCreationApi, DepositApi, WithdrawApi, BalanceCheckApi, \
    LoginApi, LogoutApi, TransactionApi, TransactionHistoryApi, CreditTransaction, DebitTransaction

urlpatterns = [
    path("usercreation/",UserCreationMixin.as_view()),
    path("accountcreation/",BankAccountCreationApi.as_view()),
    path("deposit/<int:accno>",DepositApi.as_view()),
    path("withdraw/<int:accno>",WithdrawApi.as_view()),
    path("balance/<int:accno>",BalanceCheckApi.as_view()),
    path("login/",LoginApi.as_view()),
    path("logout/",LogoutApi.as_view()),
    path('transaction/<int:accno>',TransactionApi.as_view()),
    path('trans-history/<int:accno>',TransactionHistoryApi.as_view()),
    path('trans-history/credit/<int:accno>',CreditTransaction.as_view()),
    path('trans-history/debit/<int:accno>',DebitTransaction.as_view()),

]
