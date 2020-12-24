from django.db import models
from sniffer.models import Sniffer


# Model for all RAW Messgaes received by the Sniffer Server.
class RawMessage(models.Model):
    class Meta:
        indexes = [
            models.Index(fields=['id', 'msg_raw'])
        ]

    msg_type = models.CharField(max_length=50, null=False)
    msg_json = models.CharField(max_length=512, null=False)
    msg_raw = models.CharField(max_length=50, null=True)
    sniffer = models.ForeignKey(Sniffer, on_delete=models.DO_NOTHING)
    recv_date = models.DateField(auto_now=True)
    recv_time = models.TimeField(auto_now=True)

    def __str__(self):
        return "%s: %s" % (self.msg_type, self.msg_json)


# Parsed Messages
class CommandMessage(models.Model):
    class Meta:
        indexes = [
            models.Index(fields=['id', 'address', 'sniffer'])
        ]

    address = models.IntegerField(null=False)
    sniffer = models.ForeignKey(Sniffer, on_delete=models.SET_DEFAULT, default=0)

    def __str__(self):
        return self.address
