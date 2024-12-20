from django.db import models
from helpers.models import TrackingModel
from datetime import datetime, timedelta
from django.db.models.deletion import CASCADE
# Create your models here.


class WalletTransactions(TrackingModel):
    userid = models.CharField(max_length=255,null=True, blank=True) #user id
    amount = models.CharField(max_length=255,null=True, blank=True)
    paymentmethod = models.CharField(max_length=255,null=True, blank=True)#upi/rtgs/neft
    transactionid = models.CharField(max_length=255,null=True, blank=True)#transaction id
    transactionstatus = models.CharField(max_length=255,null=True, blank=True) #pending/completed/rejected
    transactiontype = models.CharField(max_length=255,null=True, blank=True)#deposit/withdraw
    rejectionreason = models.TextField(null=True, blank=True)

class Wallet(TrackingModel):
    userid = models.CharField(max_length=255,null=True, blank=True) #user id
    amount = models.CharField(max_length=255,null=True, blank=True)#available balence



