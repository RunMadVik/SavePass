from .models import Password
from django.core.exceptions import ValidationError

def create_password(user, service, password):
    password = Password(user=user, service=service, password=password)
    try:
        password.full_clean()
    except ValidationError as e:
        return (e, False)
    password.save()
    return (password, True)

def update_password(pass_obj, password):
    pass_obj.password = password
    try:
        pass_obj.full_clean()
    except ValidationError as e:
        return (e, False)
    pass_obj.save()
    return (pass_obj, True)

def delete_password(pass_obj):
    pass_obj.delete()
    return None