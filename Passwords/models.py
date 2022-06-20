from django.db import models
from uuid import uuid4
from django.utils.translation import gettext as _

class Password(models.Model):
    uuid = models.UUIDField(_('ID'),
         primary_key = True,
         default = uuid4,
         editable = False)
    user = models.ForeignKey(to='Users.User', related_name='user', on_delete=models.CASCADE)
    service = models.ForeignKey(to='Services.Service', related_name='service', on_delete=models.PROTECT)
    password = models.CharField(_('Password'), max_length=200, null=False)
    
    class Meta:
        unique_together = [['user', 'service']]
        
    def __str__(self):
        return str(self.user) + "'s Password for " + str(self.service)