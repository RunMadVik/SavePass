from rest_framework.views import APIView
from .models import Service
from rest_framework.response import Response
from rest_framework import status
from rest_framework import serializers
from .services import create_service, update_service, delete_service
from .selectors import get_service, get_all_services
from Users.customauth import CustomAuthentication
from rest_framework.permissions import IsAuthenticated

class ServiceCreationApi(APIView):
    
    authentication_classes = [CustomAuthentication]
    permission_classes = [IsAuthenticated]
    
    class ServiceCreationSerializer(serializers.ModelSerializer):
        class Meta:
            model = Service
            exclude = ['uuid']
    
    def post(self, request):
        
        if not request.user.check_admin:
            return Response({'user': "Not an authorized user to add a service"}, status=status.HTTP_401_UNAUTHORIZED)
        
        serializer = self.ServiceCreationSerializer(data=request.data)
        if serializer.is_valid():
            create_service(request.data['service_name'], request.data['service_login_url'], request.data['service_reset_password_url'])
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class ServiceUpdationApi(APIView):
    
    authentication_classes = [CustomAuthentication]
    permission_classes = [IsAuthenticated]
    
    class ServiceUpdationSerializer(serializers.ModelSerializer):
        class Meta:
            model = Service
            exclude=['uuid']

    def put(self, request, pk):
        
        if not request.user.check_admin:
           return Response({'user': "Not an authorized user to update the service"}, status=status.HTTP_401_UNAUTHORIZED)
             
        try:
            service = get_service(pk)
        except Service.DoesNotExist:
            return Response({'service': "No service found for given uuid."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = self.ServiceUpdationSerializer(service, data=request.data, partial=True)
        if serializer.is_valid():
            service = update_service(service, request.data)
                            
            serializer2 = self.ServiceUpdationSerializer(service)
            return Response(serializer2.data, status=status.HTTP_200_OK)
                    
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ServiceDeletionApi(APIView):
    
    authentication_classes = [CustomAuthentication]
    permission_classes = [IsAuthenticated]
    
    def delete(self, request, pk):
        
        if not request.user.check_admin:
            return Response({'user': "Not an authorized user to add a service"}, status=status.HTTP_401_UNAUTHORIZED)
            
            
        try:
            service = get_service(pk)
        except Service.DoesNotExist:
            return Response({'service': "No service found for given uuid."}, status=status.HTTP_404_NOT_FOUND)
        
        delete_service(service)
        
        return Response({"service": "Service has been deleted!"}, status=status.HTTP_200_OK)
    
class ServicesViewApi(APIView):
    
    authentication_classes = [CustomAuthentication]
    permission_classes = [IsAuthenticated]
    
    class ServiceViewSerializer(serializers.ModelSerializer):
        class Meta:
            model=Service
            fields="__all__"
            
    def get(self, request):
        services  = get_all_services()
        serializer = self.ServiceViewSerializer(services, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)