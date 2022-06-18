from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.serializers import ModelSerializer
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated
from .customauth import CustomAuthentication
User = get_user_model()


class UserDetailsApi(APIView):
    
    authentication_classes = [CustomAuthentication]
    permission_classes = [IsAuthenticated]
    
    class UserDetailSerializer(ModelSerializer):
        class Meta:
            model = User
            fields = ('username', 'first_name', 'last_name', 'email', 'is_active')
            
    def post(self, request):
                
        user = request.user
        serializer = self.UserDetailSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)        