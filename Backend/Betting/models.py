from django.db import models
from helpers.models import TrackingModel
from datetime import datetime, timedelta
from django.db.models.deletion import CASCADE
# Create your models here.


class BettingMaster(TrackingModel):
    userid = models.CharField(max_length=255,null=True, blank=True) 
    gameid = models.CharField(max_length=255,null=True, blank=True) 
    companyid = models.CharField(max_length=255,null=True, blank=True)
    betfordate = models.CharField(max_length=255,null=True, blank=True)
    betamount = models.CharField(max_length=255,null=True, blank=True)
    betselectedoption = models.CharField(max_length=255,null=True, blank=True)
    



