from django.urls import path
from .services import ServiceCreationApi, ServiceUpdationApi
from .selectors import ServicesViewApi

urlpatterns = [
    path('create/', ServiceCreationApi.as_view(), name='create_service'),
    path('view/', ServicesViewApi.as_view(), name='view_services'),
    path('update/', ServiceUpdationApi.as_view(), name='update_service'),
]
