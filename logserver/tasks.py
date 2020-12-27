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

from django.utils import timezone
from django_q.cluster import Cluster

from railmessages.models import RawMessage
from sniffer.models import Sniffer
from .dccpi import DCCDecoder

logger = logging.getLogger("logserver")

cluster = Cluster()


def start_message_cluster():
    global cluster
    try:
        cluster.start()
    except Exception as e:
        pass

    if cluster.is_running:
        logger.info("Message Cluster is running %d" % cluster.pid)


def stop_message_cluster():
    global cluster
    cluster.stop()
    sys.exit()


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
    else:
        logger.error("Unknown Message Received")
        # Todo save in a own table for later processing / showing to user


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
