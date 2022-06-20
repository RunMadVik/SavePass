from django.urls import path
from .views import UserCreationApi, UserLoginApi, UserPasswordResetApi, UserDeletionApi, UserDetailsApi

urlpatterns = [
    path('create/', UserCreationApi.as_view(), name='create_user'),
    path('login/', UserLoginApi.as_view(), name='user_login'),
    path('details/', UserDetailsApi.as_view(), name='user_details'),
    path('reset-password/', UserPasswordResetApi.as_view(), name='user_reset_password'),
    path('delete/', UserDeletionApi.as_view(), name='user_delete'),
]
