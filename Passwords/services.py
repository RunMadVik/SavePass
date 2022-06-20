from .models import Password

def create_password(user, service, password):
    Password.objects.create(user=user, service=service, password=password)
    return None

def update_password(pass_obj, password):
    pass_obj.password = password
    pass_obj.save()
    return None