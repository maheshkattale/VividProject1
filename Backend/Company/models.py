from django.db import models
from helpers.models import TrackingModel
from datetime import datetime, timedelta
from django.db.models.deletion import CASCADE
# Create your models here.


class CompanyMaster(TrackingModel):
    companyname = models.CharField(max_length=255,null=True, blank=True) 
    companydescription = models.TextField(null=True, blank=True)
    companygamestarttime = models.TextField(null=True, blank=True)
    companygameendtime = models.TextField(null=True, blank=True)
    

class CompanyGames(TrackingModel):
    companyid = models.CharField(max_length=255,null=True, blank=True) 
    gameid = models.CharField(max_length=255,null=True, blank=True) 
