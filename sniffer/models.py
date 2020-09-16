from django.db import models


# Create your models here.
class Sniffer(models.Model):
    hostname = models.CharField(max_length=255)
    ip = models.GenericIPAddressField()
    mac = models.CharField(max_length=17, unique=True)
    is_connected = models.BooleanField(default=False)
    last_connection = models.DateField(auto_now=True)
