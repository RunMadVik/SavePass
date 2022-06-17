from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from uuid import uuid4
from .managers import CustomUserManager

class User(AbstractBaseUser, PermissionsMixin):
    uuid = models.UUIDField(
         primary_key = True,
         default = uuid4,
         editable = False)
    username = models.CharField(_('Username'), max_length=30, unique=True, null=False)
    first_name = models.CharField(_('First Name'),blank=True, max_length=50, null=True)
    last_name = models.CharField(_('Last Name'),blank=True, max_length=50, null=True)
    email = models.EmailField(_('Email Address'), unique=True, null=False)
    password = models.CharField(_('Password'), max_length=200, null=False)
    decryption_key = models.CharField(_('Decryption Key'), max_length=200, null=False)
    is_active = models.BooleanField(_('Active Status'), default=True)
    is_staff = models.BooleanField(_('Staff Status'), default=False)
    is_superuser = models.BooleanField(_('Superuser Status'), default=False)
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'password', 'decryption_key']
    
    objects = CustomUserManager()
    
    
    def __str__(self):
        return self.username
    
    @property
    def check_admin(self):
        return self.is_superuser
        