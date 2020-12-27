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


# Model for all RAW Messgaes received by the Sniffer Server.
class RawMessage(models.Model):
    class Meta:
        indexes = [
            models.Index(fields=['id', 'msg_raw'])
        ]

    msg_type = models.CharField(max_length=50, null=False)
    msg_json = models.CharField(max_length=512, null=False)
    msg_raw = models.CharField(max_length=50, null=True)
    sniffer = models.ForeignKey(Sniffer, on_delete=models.SET_NULL, blank=True, null=True)
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
    sniffer = models.ForeignKey(Sniffer, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.address
