from django.contrib import admin
from django.urls import path, include
from django_q.cluster import Cluster

from console import urls as console
from appsettings import urls as settings
from logsearch import urls as logsearch
import logging
from sniffer import urls as sniffer_url
from .sniffers import SnifferInit
from . import tasks

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
