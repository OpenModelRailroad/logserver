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
import os
from django.contrib import admin
from django.urls import path, include
from django.conf import settings as djsettings
from appsettings import urls as settings
from console import urls as console
from logsearch import urls as logsearch
from sniffer import urls as sniffer_url
from . import tasks
from .sniffers import SnifferInit
from django_q.tasks import async_task

logger = logging.getLogger("logserver")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('search/', include(logsearch)),
    path('sniffer/', include(sniffer_url)),
    path('settings/', include(settings)),
    path('', include(console)),
]

# Add one time start elements here
'''
To migrate Database set INSTALLED to False in settings
'''
if djsettings.INSTALLED:
    # Start Message Cluster
    logger.info("Start the Message Cluster")
    tasks.start_message_cluster()

    # Start the Sniffer Server
    logger.info("Starting Sniffer Server and Management")
    async_task("logserver.tasks.remove_all_messages", q_options={'task_name': 'remove-all-messages'})
    async_task("logserver.tasks.start_sniffer_manager", q_options={'task_name': 'start-sniffer-manager'})
    async_task("logserver.tasks.start_sniffer_server", q_options={'task_name': 'start-sniffer-server'})
    async_task("logserver.tasks.start_message_pusher", q_options={'task_name': 'start-message-pusher'})
'''
END --- After migration change INSTALLED back to True
'''
