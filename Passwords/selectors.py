from .models import Password

def get_passwords(service, user):
    password = Password.objects.filter(service=service, user=user)
    return password