from django.db import models
from helpers.models import TrackingModel
from datetime import datetime, timedelta
from django.db.models.deletion import CASCADE
# Create your models here.


class GameMaster(TrackingModel):
    gamename = models.CharField(max_length=255,null=True, blank=True) 
    gamedescription = models.TextField(null=True, blank=True)
    gamegamestarttime = models.TextField(null=True, blank=True)
    gamegameendtime = models.TextField(null=True, blank=True)
    minbetamount = models.TextField(null=True, blank=True)
    

class CompanyGames(TrackingModel):
    companyid = models.CharField(max_length=255,null=True, blank=True) 
    gameid = models.CharField(max_length=255,null=True, blank=True) 


