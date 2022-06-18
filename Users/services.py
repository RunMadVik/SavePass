from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.serializers import ModelSerializer
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated
from .customauth import CustomAuthentication
import jwt
from datetime import datetime, timedelta
User = get_user_model()


def generate_token(user):
        payload = {
            "id": (user.uuid).hex,
            "exp": datetime.now() + timedelta(hours=1),
            "iat": datetime.now()
        }

        token = jwt.encode(payload, 'pass_secret',
                           algorithm="HS256")
        
        return token

class UserCreationApi(APIView):

    class UserCheckSerializer(ModelSerializer):
        class Meta:
            model = User
            exclude = ['uuid']

    def post(self, request):
        try:
            username = request.data['username']
            email = request.data['email']
            password = request.data['password']
            decryption_key = request.data['decryption_key']

        except KeyError as exc:
            body = {
                'error': f'Missing Parameter: {exc}'
            }
            return Response(body, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            body = {
                'error': f'{e} Occured!'
            }
            return Response(body, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        serializer = self.UserCheckSerializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.create_user(username=username,
                                            email=email,
                                            password=password,
                                            decryption_key=decryption_key)

            token = generate_token(user)

            return Response({"web token": token}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginApi(APIView):

    def post(self, request):
        try:
            username = request.data['username']
            password = request.data['password']

        except KeyError as exc:
            body = {
                'error': f'Missing Parameter: {exc}'
            }
            return Response(body, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            body = {
                'error': f'{e} Occured!'
            }
            return Response(body, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            body = {
                'error': 'Username Does Not Exist!'
            }
            return Response(body, status=status.HTTP_404_NOT_FOUND)

        if not user.check_password(password):
            body = {
                'error': 'Invalid Password!'
            }
            return Response(body, status=status.HTTP_401_UNAUTHORIZED)

        token = generate_token(user)

        return Response({"web token": token}, status=status.HTTP_202_ACCEPTED)


class UserPasswordResetApi(APIView):

    authentication_classes = [CustomAuthentication]
    permission_classes = [IsAuthenticated]

    def patch(self, request):
        user = request.user

        try:
            password = request.data['password']
        except KeyError as exc:
            body = {
                'error': f'Missing Parameter: {exc}'
            }
            return Response(body, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            body = {
                'error': f'{e} Occured!'
            }
            return Response(body, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        user.set_password(password)
        user.save()
        return Response(status=status.HTTP_202_ACCEPTED)


class UserDeletionApi(APIView):

    authentication_classes = [CustomAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        user = request.user

        user.delete()
        body = {
            'success_message': "User Successfully Deleted"
        }
        return Response(body, status=status.HTTP_204_NO_CONTENT)
