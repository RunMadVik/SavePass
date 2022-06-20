from rest_framework.views import APIView
from Users.customauth import CustomAuthentication
from rest_framework.permissions import IsAuthenticated
from Services.models import Service
from rest_framework.response import Response
from rest_framework import status
from rest_framework import serializers
from Users.helpers import generate_hash
from .helpers import encrypt_password, decrypt_password
from Services.selectors import get_service
from .selectors import get_passwords
from .services import create_password, update_password, delete_password

class PasswordCreationApi(APIView):
    
    authentication_classes = [CustomAuthentication]
    permission_classes = [IsAuthenticated]
    
    class PasswordCreationSerializer(serializers.Serializer):
        password = serializers.CharField(max_length=200)
        decryption_key = serializers.CharField(max_length=200)

    def post(self, request, pk):
        
        try:
            service = get_service(pk)
        except Service.DoesNotExist:
            return Response({'service': "No service found for given uuid."}, status=status.HTTP_404_NOT_FOUND)
        
        passwords = get_passwords(service=service, user=request.user)
        if passwords.exists():
            return Response({"errors": "Service already registered with the given user."}, status = status.HTTP_400_BAD_REQUEST)
        
        serializer = self.PasswordCreationSerializer(data=request.data)
        if serializer.is_valid():
            key_hash = generate_hash(request.data['decryption_key'])
            if not key_hash == request.user.decryption_key:
                return Response({'decryption_key': "Invalid Decryption Key"}, status = status.HTTP_400_BAD_REQUEST)
            
            token = encrypt_password(request.data['password'], request.data['decryption_key'])
            create_password(user=request.user, service=service, password=token)
            
            return Response({'status': "Service Password Stored"}, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


class PasswordViewApi(APIView):
    
    authentication_classes = [CustomAuthentication]
    permission_classes = [IsAuthenticated]
    
    class PasswordViewSerializer(serializers.Serializer):
        decryption_key = serializers.CharField(max_length=200)
    
    def get(self, request, pk):
        
        try:
            service = get_service(pk)
        except Service.DoesNotExist:
            return Response({'service': "No service found for given uuid."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = self.PasswordViewSerializer(data=request.data)
        if serializer.is_valid():
            hash = generate_hash(request.data['decryption_key'])
            if request.user.decryption_key != hash:
                return Response({"error": "Invalid Decryption Key"}, status=status.HTTP_406_NOT_ACCEPTABLE)
            
            password_obj = get_passwords(service=service, user=request.user)
            if not password_obj.exists():
                return Response({"error": "User does not have any password stored for this service."}, status=status.HTTP_404_BAD_REQUEST)
            
            password = decrypt_password(request.data['decryption_key'], password_obj[0].password)
            
            return Response({"Password": password}, status=status.HTTP_200_OK)
            
        return Response(serializer.errors, status = status.HTTP_404_NOT_FOUND)
    
    
class PasswordUpdationApi(APIView):
    
    authentication_classes = [CustomAuthentication]
    permission_classes = [IsAuthenticated]
    
    class PasswordUpdationSerializer(serializers.Serializer):
        password = serializers.CharField(max_length=200)
        decryption_key = serializers.CharField(max_length=200)
    
    def put(self, request, pk):
        
        try:
            service = get_service(pk)
        except Service.DoesNotExist:
            return Response({'service': "No service found for given uuid."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = self.PasswordUpdationSerializer(data=request.data)
        if serializer.is_valid():
            hash = generate_hash(request.data['decryption_key'])
            if request.user.decryption_key != hash:
                return Response({"error": "Invalid Decryption Key"}, status=status.HTTP_406_NOT_ACCEPTABLE)
            
            password_obj = get_passwords(service=service, user=request.user)
            if not password_obj.exists():
                return Response({"error": "User does not have any password stored for this service."}, status=status.HTTP_404_NOT_FOUND)
            
            token = encrypt_password(request.data['password'], request.data['decryption_key'])
            update_password(password_obj[0], password=token)
            
            return Response({"success": "Your Password has been successfully updated."}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class PasswordDeletionApi(APIView):
    
    authentication_classes = [CustomAuthentication]
    permission_classes = [IsAuthenticated]
    
    def delete(self, request, pk):
        try:
            service = get_service(pk)
        except Service.DoesNotExist:
            return Response({'service': "No service found for given uuid."}, status=status.HTTP_404_NOT_FOUND)
        
        password_obj = get_passwords(service=service, user=request.user)
        if not password_obj.exists():
            return Response({"error": "User does not have any password stored for this service."}, status=status.HTTP_404_NOT_FOUND)
        
        delete_password(password_obj[0])
        return Response({"success": "Your Password has been successfully deleted"}, status=status.HTTP_200_OK)