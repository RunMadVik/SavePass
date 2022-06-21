from .models import Service
from django.core.exceptions import ValidationError

def create_service(service_name, service_login_url, service_reset_password_url):
    service = Service(service_name=service_name,
                      service_login_url=service_login_url,
                      service_reset_password_url=service_reset_password_url)
    try:
        service.full_clean()
    except ValidationError as e:
        return (e, False)
    service.save()
    return (service, True)


def update_service(service, data):
    for attr, value in data.items():
        setattr(service, attr, value)
    
    try:
        service.full_clean() 
    except ValidationError as e:
        return (e, False)  
     
    service.save()
    return (service, True)

def delete_service(service):
    service.delete()
    #Handle Error while calling
    return None