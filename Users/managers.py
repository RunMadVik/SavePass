from django.contrib.auth.models import BaseUserManager
from hashlib import sha256

class CustomUserManager(BaseUserManager):
    
    def generate_hash(self,key):
        myhash = sha256(key.encode('ascii'))
        return myhash.hexdigest()
    
    def create_user(self, email, username, password, decryption_key, **other_fields):
        
        if not email:
            raise ValueError("Email Field Must Not Be Empty")    
        
        if not username:
            raise ValueError("Username Field Must Not Be Empty") 
        
        if not password:
            raise ValueError("Password Field Must Not Be Empty") 
        
        if not decryption_key:
            raise ValueError("Decrpytion Key Field Must Not Be Empty")
        
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **other_fields)
        user.set_password(password)
        user.decryption_key = self.generate_hash(decryption_key)
        user.save()
        return user
    
    def create_superuser(self, email, username, password, decryption_key, **other_fields):
        
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        
        if other_fields.get('is_staff') is not True:
            raise ValueError("Staff Status must be set to True")
        
        if other_fields.get('is_superuser') is not True:
            raise ValueError("Superuser Status must be set to True")
        
        return self.create_user(email, username, password, decryption_key, **other_fields)