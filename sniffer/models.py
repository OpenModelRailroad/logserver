from django.db import models


class Sniffer(models.Model):
    hostname = models.CharField(max_length=255)
    ip = models.GenericIPAddressField()
    mac = models.CharField(max_length=17)
    is_connected = models.BooleanField(default=False)
    last_connection = models.DateTimeField(auto_now=False, null=True)
    port = models.IntegerField()

    def __str__(self):
        return "%s [%s]" % (self.hostname, self.ip)
