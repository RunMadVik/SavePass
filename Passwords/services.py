from rest_framework.views import APIView
from Users.customauth import CustomAuthentication
from rest_framework.permissions import IsAuthenticated
from Services.models import Service
from rest_framework.response import Response
from rest_framework import status
from rest_framework import serializers
from .models import Password
from hashlib import sha256
from cryptography.fernet import Fernet

class PasswordCreationApi(APIView):
    
    authentication_classes = [CustomAuthentication]
    permission_classes = [IsAuthenticated]
    
    class PasswordCreationSerializer(serializers.Serializer):
        password = serializers.CharField(max_length=200)
        decryption_key = serializers.CharField(max_length=200)
            
    def get_hash(self, key):
        myhash = sha256(key.encode('utf-8'))
        return myhash.hexdigest()
    
    def encrypt_password(self, password, key):
        f = Fernet(key.encode('utf-8'))
        e_pass = f.encrypt(password.encode('utf-8'))
        return e_pass.decode('utf-8')
    
    def post(self, request, pk):
        
        try:
            service = Service.objects.get(pk=pk)
        except Service.DoesNotExist:
            return Response({'service': "No service found for given uuid."}, status=status.HTTP_404_NOT_FOUND)
        
        present = Password.objects.filter(service=service, user=request.user)
        if present.exists():
            return Response({"errors": "Service already registered with the given user."}, status = status.HTTP_400_BAD_REQUEST)
        
        serializer = self.PasswordCreationSerializer(data=request.data)
        if serializer.is_valid():
            key_hash = self.get_hash(request.data['decryption_key'])
            if not key_hash == request.user.decryption_key:
                return Response({'decryption_key': "Invalid Decryption Key"}, status = status.HTTP_406_NOT_ACCEPTABLE)
            
            token = self.encrypt_password(request.data['password'], request.data['decryption_key'])
            password = self.get_hash(token) 
            Password.objects.create(user=request.user, service=service, password=password)
            
            return Response({'status': "Service Password Stored"}, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
        