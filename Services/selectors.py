from rest_framework.views import APIView
from .models import Service
from rest_framework.response import Response
from rest_framework import status
from rest_framework.serializers import ModelSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated


class ServicesViewApi(APIView):
    
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    class ServiceViewSerializer(ModelSerializer):
        class Meta:
            model=Service
            fields="__all__"
            
    def get(self, request):
        services  = Service.objects.all()
        serializer = self.ServiceViewSerializer(services, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)