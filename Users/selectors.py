from django.contrib.auth import get_user_model
User = get_user_model()


def get_user(username):
    user = User.objects.get(username=username)
    return user