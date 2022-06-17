from django.urls import path
from .services import ServiceCreationApi

urlpatterns = [
    path('create/', ServiceCreationApi.as_view(), name='create_service'),
]
