from django.db import models


# Types of Messages
class SnifferMessageType(models.Model):
    name = models.CharField(max_length=50)


# All Messages
class SnifferMessage(models.Model):
    datetime = models.DateTimeField()
    raw_message = models.TextField()


class Sniffer(models.Model):
    hostname = models.CharField(max_length=255)
    ip = models.GenericIPAddressField()
    mac = models.CharField(max_length=17)
    is_connected = models.BooleanField(default=False)
