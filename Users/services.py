from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.serializers import ModelSerializer
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
User = get_user_model()


class UserCreationApi(APIView):

    class UserCheckSerializer(ModelSerializer):
        class Meta:
            model = User
            exclude = ['uuid']

    def post(self, request):
        try:
            username = request.data['username']
            email = request.data['email']
            password = request.data['password']
            decryption_key = request.data['decryption_key']

        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        serializer = self.UserCheckSerializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.create_user(username=username,
                                            email=email,
                                            password=password,
                                            decryption_key=decryption_key)
            refresh = RefreshToken.for_user(user)

            return Response({'refresh': str(refresh),
                            'access': str(refresh.access_token)},
                            status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UserLoginApi(APIView):
    
    def post(self, request):
        try:
            username = request.data['username']
            password = request.data['password']
            
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        if not user.check_password(password):
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        
        refresh = RefreshToken.for_user(user)
        return Response({'refresh': str(refresh),
                            'access': str(refresh.access_token)},
                            status=status.HTTP_202_ACCEPTED)
        

class UserPasswordResetApi(APIView):
    
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def patch(self, request):
        user = request.user
        
        try:
            password = request.data['password']
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        user.set_password(password)
        user.save()
        return Response(status=status.HTTP_202_ACCEPTED)
    
class UserDeletionApi(APIView):
    
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def delete(self, request):
        user = request.user
        
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)