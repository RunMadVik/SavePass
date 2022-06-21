from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated
from .customauth import CustomAuthentication
from .services import create_user, update_user_password, delete_user
from .selectors import get_user
from .helpers import generate_token, generate_key, generate_hash
User = get_user_model()

#User Creation API
class UserCreationApi(APIView):

    class UserCheckSerializer(serializers.ModelSerializer):
        class Meta:
            model = User
            exclude = ['uuid','decryption_key']


    def post(self, request):

        serializer = self.UserCheckSerializer(data=request.data)
        if serializer.is_valid():
            username = request.data['username']
            email = request.data['email']
            password = request.data['password']
            secret_key = generate_key()
            decryption_key = generate_hash(secret_key)
            result, check = create_user(username, email, password, decryption_key)
            
            if not check:
                return Response(result, status=status.HTTP_400_BAD_REQUEST)
            
            token = generate_token(result)

            return Response({"web token": token,
                             'decryption_key': secret_key}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginApi(APIView):
    
    class UserCredentialSerializer(serializers.Serializer):
        
        username = serializers.CharField(max_length=30)
        password = serializers.CharField(max_length=200)
        
        def validate(self, data):
            try:
                user = get_user(data['username'])
            except User.DoesNotExist:
                raise serializers.ValidationError({'username': 'User not found with the given username.'})
            
            if not user.check_password(data['password']):
                raise serializers.ValidationError({"password":"Given Password is incorrect."})
            
            data['user'] = user
            return data

    def post(self, request):
                
        serializer = self.UserCredentialSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        user = serializer.validated_data['user']
        token = generate_token(user)

        return Response({"web token": token}, status=status.HTTP_202_ACCEPTED)


class UserPasswordResetApi(APIView):

    authentication_classes = [CustomAuthentication]
    permission_classes = [IsAuthenticated]
    
    class PasswordResetSerializer(serializers.Serializer):
        old_password = serializers.CharField(max_length=200)
        new_password = serializers.CharField(max_length=200)

    def patch(self, request):
        user = request.user

        serializer = self.PasswordResetSerializer(user, data=request.data)
        if serializer.is_valid():
            if not user.check_password(request.data['old_password']):
                return Response({"error": "Old Password is incorrect."}, status=status.HTTP_406_NOT_ACCEPTABLE)
                
            result, check = update_user_password(user, request.data['new_password'])
            if not check:
                return Response(result, status=status.HTTP_400_BAD_REQUEST)
            
            return Response({'status': "Password Updated Successfully"}, status=status.HTTP_202_ACCEPTED)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDeletionApi(APIView):

    authentication_classes = [CustomAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        user = request.user
        
        delete_user(user)
        body = {
            'success_message': "User Successfully Deleted"
        }
        return Response(body, status=status.HTTP_200_OK)


class UserDetailsApi(APIView):
    
    authentication_classes = [CustomAuthentication]
    permission_classes = [IsAuthenticated]
    
    class UserDetailSerializer(serializers.ModelSerializer):
        class Meta:
            model = User
            fields = ('username', 'first_name', 'last_name', 'email', 'is_active')
            
    def get(self, request):
                
        user = request.user
        serializer = self.UserDetailSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)        