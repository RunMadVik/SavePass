from rest_framework.views import APIView
from .models import Service
from rest_framework.response import Response
from rest_framework import status
from rest_framework import serializers
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
            serializer.save()
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
           return Response({'user': "Not an authorized user to add a service"}, status=status.HTTP_401_UNAUTHORIZED)
             
        try:
            service = Service.objects.get(pk=pk)
        except Service.DoesNotExist:
            return Response({'service': "No service found for given uuid."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = self.ServiceUpdationSerializer(service, data=request.data, partial=True)
        if serializer.is_valid():
            for attr, value in request.data.items():
                setattr(service, attr, value)
                service.save()
                
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
            service = Service.objects.get(pk=pk)
        except Service.DoesNotExist:
            return Response({'service': "No service found for given uuid."}, status=status.HTTP_404_NOT_FOUND)
        
        service.delete()
        
        return Response({"service": "Service has been deleted!"}, status=status.HTTP_200_OK)