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
import json
import logging
import sys
from datetime import datetime, timedelta
from django.core.management import call_command
import os
from django.conf import settings
from django.utils import timezone
from django_q.cluster import Cluster
from django.utils import timezone
from django_q.monitor import Stat

from railmessages.models import RawMessage, CommandMessage
from sniffer.models import Sniffer
from .dccpi import DCCDecoder
from .mfx import MFXDecoder
from .sniffers import SnifferInit
from channels.layers import get_channel_layer
from console.models import Clients
from asgiref.sync import async_to_sync

logger = logging.getLogger("logserver")

cluster = Cluster()
sniffers = SnifferInit()


# Message Cluster
def start_message_cluster():
    try:
        logserver_cluster = cluster.start()
        logger.info(logserver_cluster.stat())
    except Exception as e:
        pass

    if cluster.is_running:
        logger.info("Message Cluster is running %d" % cluster.pid)


def stop_server():
    # cluster.stop()
    sys.exit()


def stop_message_cluster():
    cluster.stop()


# TODO Needs work, cannot restart
def restart_message_cluster():
    logger.info("Restart Message Cluster")
    cluster.stop()

    while not cluster.has_stopped:
        pass
    cluster.start()


def get_cluster_stats():
    return cluster.stat


# Sniffer Server
def start_sniffer_server():
    sniffers.stop_sniffer_server_thread()
    sniffers.start_sniffer_server_thread()


def stop_sniffer_server():
    sniffers.stop_sniffer_server_thread()


def restart_sniffer_server():
    stop_sniffer_server()
    start_sniffer_server()


def get_sniffer_server_status():
    return sniffers.is_sniffer_server_running()


# Sniffer Manager
def start_sniffer_manager():
    stop_sniffer_manager()
    sniffers.start_sniffer_manager_thread()


def stop_sniffer_manager():
    sniffers.stop_sniffer_manager_thread()


def restart_sniffer_manager():
    stop_sniffer_manager()
    start_sniffer_manager()

    # Messages


def process_rail_message(message, client_address):
    msg = message.decode("utf-8").replace("'", '"')
    jmsg = json.loads(msg)
    msg_type = jmsg['type']

    try:
        layer = get_channel_layer()
        async_to_sync(layer.group_send)('console', {
            'type': 'console.message',
            'content': 'triggered'
        })
        sniffer = Sniffer.objects.get(port=client_address[1])
        raw = RawMessage.objects.create(
            msg_type=jmsg['type'],
            msg_json=jmsg,
            msg_raw=jmsg['raw'],
            sniffer_id=sniffer.id
        ).save()

        if msg_type == 'dcc':

            decoder = DCCDecoder('0b' + jmsg['raw'])
            logger.info(decoder)
            CommandMessage.objects.create(address=decoder.get_address(), command=decoder.get_command(), sniffer_id=sniffer.id, received=timezone.now(),
                                          type="dcc")
            #async_to_sync(channel_layer.group_send)("console_name", {"type": "console_message", "text": decoder})

        elif msg_type == 'mfx':
            decoder = MFXDecoder(jmsg['raw'])
            logger.info(decoder)
            CommandMessage.objects.create(address=decoder.get_address(), command=decoder.get_command(), parameters=decoder.get_parameters(), asset_type='loco',
                                          sniffer_id=sniffer.id, received=timezone.now(), type="mfx")
            #async_to_sync(channel_layer.group_send)("console_name", {"type": "console_message", "text": decoder})
        else:
            logger.error("Unknown Message Received")

    except Sniffer.DoesNotExist:
        logger.info("Sniffer does not exist. packet cannot be saved")


def process_heartbeat(message, client_address):
    msg = message.decode("utf-8").replace("'", '"')
    jmsg = json.loads(msg)
    try:
        e = Sniffer.objects.get(mac=jmsg['mac'])
        e.ip = jmsg['ip']
        e.hostname = jmsg['hostname']
        e.is_connected = True
        e.port = client_address[1]
        e.last_connection = timezone.now()
        e.save()

        logger.info('received heratbeat for sniffer %s %s (%s)' % (jmsg['hostname'], jmsg['mac'], jmsg['ip']))

    except Sniffer.DoesNotExist:
        Sniffer.objects.create(
            hostname=jmsg['hostname'],
            ip=jmsg['ip'],
            mac=jmsg['mac'],
            is_connected=True,
            last_connection=timezone.now(),
            port=client_address[1],
        ).save()

        logger.info('created new sniffer  %s %s (%s)' % (jmsg['hostname'], jmsg['mac'], jmsg['ip']))


# Database Management

# dump to json
def dump_data_to_json():
    output = open(os.path.join(settings.MEDIA_ROOT, 'dump.json'), 'w')
    call_command('dumpdata', 'railmessages', format='json', indent=3, stdout=output)
    output.close()


# Removes all Messages in (rawmessage, commandmessage, unplausiblemessage) older than 24h from now
def cleanup_database():
    RawMessage.objects.filter(received__lte=timezone.now() - timedelta(seconds=settings.MESSAGE_RETENTION_TIME)).delete()
    CommandMessage.objects.filter(received__lte=timezone.now() - timedelta(seconds=settings.MESSAGE_RETENTION_TIME)).delete()


# in (rawmessage, commandmessage, unplausiblemessage)
def remove_all_messages():
    RawMessage.objects.all().delete()
    CommandMessage.objects.all().delete()
