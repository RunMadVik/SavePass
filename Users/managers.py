from django.contrib.auth.models import BaseUserManager
from .helpers import generate_hash, generate_key
from django.core.exceptions import ValidationError

class CustomUserManager(BaseUserManager):
        
    def create_user(self, email, username, password, decryption_key, **other_fields):
        
        if not email:
            raise ValueError("Email Field Must Not Be Empty")    
        
        if not username:
            raise ValueError("Username Field Must Not Be Empty") 
        
        if not password:
            raise ValueError("Password Field Must Not Be Empty") 
        
        if not decryption_key:
            raise ValueError("Decryption Key Field Must Not Be Empty")
        
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, decryption_key=decryption_key, **other_fields)
        user.set_password(password)
        try:
            user.full_clean()
        except ValidationError as e:
            raise ValidationError(e)
        user.save()
        return user
    
    def create_superuser(self, email, username, password, decryption_key, **other_fields):
        
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        
        decryption_key = generate_hash(generate_key())
        
        if other_fields.get('is_staff') is not True:
            raise ValueError("Staff Status must be set to True")
        
        if other_fields.get('is_superuser') is not True:
            raise ValueError("Superuser Status must be set to True")
        
        return self.create_user(email, username, password, decryption_key, **other_fields)