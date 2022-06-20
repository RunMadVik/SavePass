from django.urls import path
from .views import PasswordCreationApi, PasswordViewApi, PasswordUpdationApi

urlpatterns = [
    path('create/<slug:pk>/', PasswordCreationApi.as_view(), name='create_password'),
    path('view/<slug:pk>/', PasswordViewApi.as_view(), name='view_password'),
    path('update/<slug:pk>/', PasswordUpdationApi.as_view(), name='update_password'),
]
