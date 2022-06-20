from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated
from cryptography.fernet import Fernet
from hashlib import sha256
from .customauth import CustomAuthentication
import jwt
User = get_user_model()



#Generating JWT token for user
def generate_token(user):
    
    payload = {
        "id": (user.uuid).hex
    }

    token = jwt.encode(payload, 'pass_secret',
                        algorithm="HS256")
    
    return token


#User Creation API
class UserCreationApi(APIView):

    class UserCheckSerializer(serializers.ModelSerializer):
        class Meta:
            model = User
            exclude = ['uuid','decryption_key']
    
    #Generating a key for user to access his/her passwords      
    def generate_key(self):
        key = Fernet.generate_key()
        return key.decode('utf-8')
    
    
    #Hashing the password to store to the server
    def generate_hash(self, key):
        hash = sha256(key.encode('utf-8'))
        return hash.hexdigest()

    def post(self, request):

        serializer = self.UserCheckSerializer(data=request.data)
        if serializer.is_valid():
            username = request.data['username']
            email = request.data['email']
            password = request.data['password']
            secret_key = self.generate_key()
            decryption_key = self.generate_hash(secret_key)
            user = User.objects.create_user(username=username,
                                            email=email,
                                            password=password,
                                            decryption_key=decryption_key)

            token = generate_token(user)

            return Response({"web token": token,
                             'decryption_key': secret_key}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginApi(APIView):
    
    class UserCredentialSerializer(serializers.Serializer):
        username = serializers.CharField(max_length=30)
        password = serializers.CharField(max_length=200)
        
        def validate(self, data):
            try:
                user = User.objects.get(username=data['username'])
            except User.DoesNotExist:
                raise serializers.ValidationError({'username': 'User not found with the given username.'})
            
            if not user.check_password(data['password']):
                raise serializers.ValidationError({"password":"Given Password is incorrect."})
            
            return data

    def post(self, request):
                
        serializer = self.UserCredentialSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        user = User.objects.get(username=request.data['username'])

        token = generate_token(user)

        return Response({"web token": token}, status=status.HTTP_202_ACCEPTED)


class UserPasswordResetApi(APIView):

    authentication_classes = [CustomAuthentication]
    permission_classes = [IsAuthenticated]
    
    class PasswordResetSerializer(serializers.ModelSerializer):
        class Meta:
            model = User
            fields = ('password',)

    def patch(self, request):
        user = request.user

        serializer = self.PasswordResetSerializer(user, data=request.data)
        if serializer.is_valid():
            password = request.data['password']
            user.set_password(password)
            user.save()
            return Response(status=status.HTTP_202_ACCEPTED)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDeletionApi(APIView):

    authentication_classes = [CustomAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        user = request.user

        user.delete()
        body = {
            'success_message': "User Successfully Deleted"
        }
        return Response(body, status=status.HTTP_200_OK)
