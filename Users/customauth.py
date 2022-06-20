from rest_framework.authentication import BaseAuthentication
import jwt
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth import get_user_model
User = get_user_model()

class CustomAuthentication(BaseAuthentication):
    
    def authenticate(self, request):
        try:
            token = request.META['HTTP_AUTHORIZATION']
            header_value = token.split(' ')
            if len(header_value) != 2:
                raise AuthenticationFailed("Invalid Token")
        
        except KeyError:
            return None
        
        try:
            body = jwt.decode(header_value[1], 'pass_secret', algorithms=['HS256'])
        
        except jwt.exceptions.InvalidSignatureError:
            raise AuthenticationFailed("Signature Verification Falied")
        
        except jwt.exceptions.ExpiredSignatureError:
            raise AuthenticationFailed("Token is expired")
        
        except jwt.exceptions.InvalidIssuedAtError:
            raise AuthenticationFailed("Token validation date not reached.")
        
        id = body['id']
        try:
            user = User.objects.get(uuid=id)
        
        except User.DoesNotExist:
            raise AuthenticationFailed("User Does Not Exist")
        
        return (user, token)
            
        
        