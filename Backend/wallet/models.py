from django.db import models
from helpers.models import TrackingModel
from datetime import datetime, timedelta
from django.db.models.deletion import CASCADE
# Create your models here.
from django.utils import timezone


class WalletTransactions(TrackingModel):
    userid = models.CharField(max_length=255,null=True, blank=True) #user id
    amount = models.CharField(max_length=255,null=True, blank=True)
    paymenttype = models.CharField(max_length=255,null=True, blank=True)#upi/rtgs/neft
    transactionid = models.CharField(max_length=255,null=True, blank=True)#transaction id
    transactionstatus = models.CharField(max_length=255,null=True, blank=True) #pending/completed/rejected
    transactiontype = models.CharField(max_length=255,null=True, blank=True)#deposit/withdraw
    rejectionreason = models.TextField(null=True, blank=True)
    mobilenumber = models.TextField(null=True, blank=True)
    date = models.CharField(max_length=255,null=True, blank=True)
    time = models.CharField(max_length=255,null=True, blank=True)

class Wallet(TrackingModel):
    userid = models.CharField(max_length=255,null=True, blank=True) #user id
    amount = models.CharField(max_length=255,null=True, blank=True)#available balence



