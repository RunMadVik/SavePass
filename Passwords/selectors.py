from rest_framework.views import APIView
from Services.models import Service
from rest_framework.response import Response
from rest_framework import status
from rest_framework import serializers
from Users.customauth import CustomAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from hashlib import sha256
from cryptography.fernet import Fernet
from .models import Password
User = get_user_model()

class PasswordViewApi(APIView):
    
    authentication_classes = [CustomAuthentication]
    permission_classes = [IsAuthenticated]
    
    class PasswordViewSerializer(serializers.ModelSerializer):
        class Meta:
            model=User
            fields = ('decryption_key',)
            
    
    def get_hash(self, key):
        myhash = sha256(key.encode('utf-8'))
        return myhash.hexdigest()
    
    def decrypt_password(self, key, password):
        key = key.encode('utf-8')
        f= Fernet(key)
        password = password.encode('utf-8')
        print(password)
        d_pass = f.decrypt(password)
        return d_pass
    
    def get(self, request, pk):
        
        try:
            service = Service.objects.get(pk=pk)
        except Service.DoesNotExist:
            return Response({'service': "No service found for given uuid."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = self.PasswordViewSerializer(data=request.data)
        if serializer.is_valid():
            hash = self.get_hash(request.data['decryption_key'])
            if request.user.decryption_key != hash:
                return Response({"error": "Invalid Decryption Key"}, status=status.HTTP_406_NOT_ACCEPTABLE)
            
            password_obj = Password.objects.filter(service=service, user=request.user)
            if not password_obj.exists():
                return Response({"error": "User does not have any password stored for this service."}, status=status.HTTP_404_BAD_REQUEST)
            
            password = self.decrypt_password(request.data['decryption_key'], password_obj[0].password)
            
            return Response({"Password": password}, status=status.HTTP_200_OK)
            
        return Response(serializer.errors, status = status.HTTP_404_NOT_FOUND)