from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
User = get_user_model()


def create_user(username, email, password, decryption_key):
    try:
        user = User.objects.create_user(username=username,
                                        email=email,
                                        password=password,
                                        decryption_key=decryption_key)
    
    except ValidationError as e:
        return (e, False)

    return (user, True)


def update_user_password(user, password):
    user.set_password(password)
    try:
        user.full_clean()
    except ValidationError as e:
        return (e, False)
    user.save()
    return (user, True)


def delete_user(user):
    user.delete()
    return None
