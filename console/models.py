from django.db import models


# Create your models here.
class Sniffer(models.Model):
    hostname = models.CharField(max_length=255)
    ip = models.GenericIPAddressField()
    mac = models.CharField(max_length=17)
    is_connected = models.BooleanField(default=False)
