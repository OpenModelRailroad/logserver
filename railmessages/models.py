"""
    Copyright (C) 2020  OpenModelRailRoad, Florian Thiévent

    This file is part of "OMRR".

    "OMRR" is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    "OMRR" is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
from django.db import models

from sniffer.models import Sniffer
from .choices import MESSAGE_TYPE


# Model for all RAW Messgaes received by the Sniffer Server.
class RawMessage(models.Model):
    class Meta:
        indexes = [
            models.Index(fields=['msg_raw'])
        ]

    msg_type = models.CharField(max_length=3, choices=MESSAGE_TYPE, default='def', null=False)
    msg_json = models.CharField(max_length=512, null=False)
    msg_raw = models.CharField(max_length=50, null=True)
    sniffer = models.ForeignKey(Sniffer, on_delete=models.SET_NULL, blank=True, null=True)
    received = models.DateTimeField(auto_created=False, auto_now_add=False, auto_now=True, blank=True, null=True)
    recv_date = models.DateField(auto_now=True)
    recv_time = models.TimeField(auto_now=True)

    def __str__(self):
        return "%s: %s" % (self.msg_type, self.msg_json)


# Parsed Messages
class CommandMessage(models.Model):
    class Meta:
        verbose_name = 'Command Message'
        verbose_name_plural = 'Command Messages'
        indexes = [
            models.Index(fields=['address', 'sniffer', 'received'])
        ]

    address = models.IntegerField(null=True, default=None)
    sniffer = models.ForeignKey(Sniffer, on_delete=models.SET_NULL, blank=True, null=True)
    received = models.DateTimeField(auto_created=False, auto_now_add=False, auto_now=False, blank=True, null=True)
    type = models.CharField(max_length=3, choices=MESSAGE_TYPE, default='def')
    asset_type = models.CharField(max_length=50, null=True, blank=True)
    command = models.CharField(max_length=255, blank=True, null=True)
    parameters = models.CharField(max_length=1000, blank=True, null=True)
    unplausible = models.BooleanField(default=False, null=False, blank=True)
    console = models.BooleanField(default=False, null=False, blank=True)

    def __str__(self):
        return self.address
