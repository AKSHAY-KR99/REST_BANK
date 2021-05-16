from django.db import models

# Create your models here.


class AccountDetails(models.Model):
    accno=models.IntegerField(unique=True)
    username=models.CharField(max_length=50)
    balance=models.FloatField(default=0)
    account_type=models.CharField(max_length=50)

    def __str__(self):
        return self.accno

class TransactionDetails(models.Model):
    fromaccno=models.IntegerField()
    toaccno=models.IntegerField()
    amount=models.FloatField()
    date=models.DateTimeField(auto_now=True)