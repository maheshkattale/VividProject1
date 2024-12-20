from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager
from helpers.models import TrackingModel
from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_save
from rest_framework.authtoken.models import Token
import uuid
import jwt
from datetime import datetime, timedelta
from django.db.models.deletion import CASCADE

# Create your models here.

# class apikey(TrackingModel):
#     Apikey = models.CharField(max_length=255,null=True,blank=True)


class UserManager(BaseUserManager):
    def create(self,Username,password,**extra_fields):
        if not Username:
            raise ValueError("User must have a valid Username")
        user = self.model(Username=Username,**extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

class User(AbstractBaseUser,TrackingModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    Username = models.CharField(max_length=255,null=True,blank=True)
    textPassword = models.CharField(max_length=255,null=True,blank=True)
    mobileNumber = models.BigIntegerField(null=True,blank=True)
    email = models.CharField(max_length=255,null=True,blank=True)
    FirstName = models.CharField(max_length=255,null=True,blank=True)
    LastName = models.CharField(max_length=255,null=True,blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'Username'
    REQUIRED_FIELDS = []

    @property
    def token(self):
        token = jwt.encode(
            {'id': self.id.hex,
             'Username': self.Username,
                'mobile': self.mobileNumber,
                'exp': datetime.utcnow() + timedelta(hours=24)},
            settings.SECRET_KEY, algorithm='HS256')
        return token

class UserToken(TrackingModel):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    User = models.CharField(max_length=255,null=True, blank=True)
    authToken = models.TextField(null=True, blank=True)



# Create your models here.
