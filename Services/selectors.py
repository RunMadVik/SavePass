from .models import Service

def get_service(pk):
    service = Service.objects.get(pk=pk)
    return service

def get_all_services():
    services = Service.objects.all()
    return services