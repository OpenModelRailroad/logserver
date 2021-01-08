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

from django.conf import settings
from django.utils import timezone
from django_q.cluster import Cluster
from django_q.monitor import Stat

from railmessages.models import RawMessage, CommandMessage
from sniffer.models import Sniffer
from .dccpi import DCCDecoder
from .sniffers import SnifferInit

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
    print("hello berfore")
    for stat in Stat.get_all():
        print("hello")
    #cluster.stop()
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

    if msg_type == 'dcc':
        logger.debug("Received dcc msg: %s" % jmsg['raw'])
        try:
            sniffer = Sniffer.objects.get(port=client_address[1])
            RawMessage.objects.create(
                msg_type=jmsg['type'],
                msg_json=jmsg,
                msg_raw=jmsg['raw'],
                sniffer_id=sniffer.id
            ).save()
        except Sniffer.DoesNotExist:
            logger.info("Sniffer does not exist. packet cannot be saved")

        decoder = DCCDecoder('0b' + jmsg['raw'])
        address = decoder.get_address()
        command = decoder.get_command()
        logger.info("DCC Message for %d, Command %s " % (address, command))
    elif msg_type == 'mfx':
        #TODO make MFX possible
        pass
    else:
        logger.error("Unknown Message Received")
        # Todo maybe save in a own table for later processing / showing to user


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
# Removes all Messages in (rawmessage, commandmessage, unplausiblemessage) older than 24h from now
def cleanup_database():
    RawMessage.objects.filter(received__lte=timezone.now() - timedelta(seconds=settings.MESSAGE_RETENTION_TIME)).delete()
    CommandMessage.objects.filter(received__lte=timezone.now() - timedelta(seconds=settings.MESSAGE_RETENTION_TIME)).delete()


# in (rawmessage, commandmessage, unplausiblemessage)
def remove_all_messages():
    RawMessage.objects.all().delete()
    CommandMessage.objects.all().delete()
