from django.contrib.auth.models import AbstractUser,AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models

class User(AbstractUser):
    address = models.TextField(blank=True,null=True)
    age = models.PositiveSmallIntegerField(blank=True,null=True)
    date_joined = models.DateTimeField(null=True,blank=True,default='2020-10-10')
    description = models.TextField(blank=True,null=True)
    email = models.EmailField(blank=True,null=True)
    first_name = models.CharField(blank=True,null=True,max_length=50)
    gender = models.CharField(blank=True,null=True,choices=[('F','Female'),('M','Male')],max_length=1)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(blank=True)
    is_superuser = models.BooleanField(blank=True)
    last_login = models.DateTimeField(blank=True,null=True)
    last_name = models.CharField(blank=True,null=True,max_length=50)
    password = models.CharField(max_length=50)
    phone = models.CharField(blank=True,null=True,max_length=15)
    username = models.CharField(max_length=50,unique=True)

# class AbstractUser(AbstractBaseUser,PermissionsMixin):
#     date_joined = models.DateTimeField()
#     email = models.EmailField(blank=True,null=True)
#     first_name = models.CharField(blank=True,null=True,max_length=50)
#     is_active = models.BooleanField()
#     is_staff = models.BooleanField()
#     is_superuser = models.BooleanField(User)
#     last_login = models.DateTimeField(User,blank=True,null=True)
#     last_name = models.CharField(blank=True,null=True,max_length=50)
#     password = models.CharField(User,max_length=50)
#     username = models.CharField(AbstractUser,max_length=50)