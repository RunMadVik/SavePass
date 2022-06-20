from django.urls import path
from .services import PasswordCreationApi
from .selectors import PasswordViewApi

urlpatterns = [
    path('create/<slug:pk>/', PasswordCreationApi.as_view(), name='create_password'),
    path('view/<slug:pk>/', PasswordViewApi.as_view(), name='view_password'),
]
