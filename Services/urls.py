from django.urls import path
from .views import ServiceCreationApi, ServiceUpdationApi, ServiceDeletionApi, ServicesViewApi

urlpatterns = [
    path('create/', ServiceCreationApi.as_view(), name='create_service'),
    path('view/', ServicesViewApi.as_view(), name='view_services'),
    path('update/<slug:pk>/', ServiceUpdationApi.as_view(), name='update_service'),
    path('delete/<slug:pk>/', ServiceDeletionApi.as_view(), name='delete_service'),
]
