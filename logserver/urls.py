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
import logging

from django.contrib import admin
from django.urls import path, include

from appsettings import urls as settings
from console import urls as console
from logsearch import urls as logsearch
from sniffer import urls as sniffer_url
from . import tasks
from .sniffers import SnifferInit

logger = logging.getLogger("logserver")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('search/', include(logsearch)),
    path('sniffer/', include(sniffer_url)),
    path('settings/', include(settings)),
    path('', include(console)),
]


# Add one time start elements here
logger.info("Start the Message Cluster")

tasks.start_message_cluster()

# Start the Sniffer Server
sniffers = SnifferInit()
sniffers.start_sniffer_manager_thread()
sniffers.start_sniffer_server_thread()
