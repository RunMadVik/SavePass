from django.contrib.auth import get_user_model
User = get_user_model()


def create_user(username, email, password, decryption_key):
    user = User.objects.create_user(username=username,
                                    email=email,
                                    password=password,
                                    decryption_key=decryption_key)
    
    return user

def update_user_password(user, password):
    user.set_password(password)
    user.save()
    return user

def delete_user(user):
    user.delete()
    return None