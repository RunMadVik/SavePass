from django.urls import path
from .services import PasswordCreationApi

urlpatterns = [
    path('create/<slug:pk>/', PasswordCreationApi.as_view(), name='create_password'),
]
