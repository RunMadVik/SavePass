from re import L
from django import views
from rest_framework.views import APIView
from .models import Service
from rest_framework.response import Response
from rest_framework import status
from rest_framework.serializers import ModelSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated

class ServiceCreationApi(APIView):
    
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    class ServiceCreationSerializer(ModelSerializer):
        class Meta:
            model = Service
            exclude = ['uuid']
    
    def post(self, request):
        
        user = request.user
        if not user.check_admin:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        
        
        serializer = self.ServiceCreationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        