from .models import Service

def create_service(service_name, service_login_url, service_reset_password_url):
    service = Service(service_name=service_name,
                      service_login_url=service_login_url,
                      service_reset_password_url=service_reset_password_url)
    service.save()
    return None


def update_service(service, data):
    for attr, value in data.items():
        setattr(service, attr, value)
        service.save()
    
    return service

def delete_service(service):
    service.delete()
    return None