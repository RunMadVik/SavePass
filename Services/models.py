from django.db import models
from django.utils.translation import gettext as _
from uuid import uuid4

class Service(models.Model):
    uuid = models.UUIDField(_('ID'),
         primary_key = True,
         default = uuid4,
         editable = False)
    service_name = models.CharField(_("Service Name"), max_length=200, null=False, unique=True)
    service_login_url = models.URLField(_("Service Login URL"), null=False, unique=True)
    service_reset_password_url = models.URLField(_("Service Password Reset URL"), null=False, unique=True)
    
    def __str__(self):
        return self.service_name