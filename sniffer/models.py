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


class Sniffer(models.Model):
    hostname = models.CharField(max_length=255)
    ip = models.GenericIPAddressField()
    mac = models.CharField(max_length=17)
    is_connected = models.BooleanField(default=False)
    last_connection = models.DateTimeField(auto_now=False, auto_now_add=False, auto_created=False, null=True)
    port = models.IntegerField()

    def __str__(self):
        return "%s [%s]" % (self.hostname, self.ip)
