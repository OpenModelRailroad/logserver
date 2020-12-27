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
from socket import *

from django_q.tasks import async_task

logger = logging.getLogger("logserver")
server_socket = None


def sniffer_server(port):
    logger.info("Starting Sniffer Server on port %s" % port)
    global server_socket
    server_socket = socket(AF_INET, SOCK_DGRAM)
    try:
        server_socket.bind(('', port))
        logger.info("Sniffer Server Ready to receive data")
    except Exception as e:
        logger.error("Cannot start Sniffer Server %s" % e)

    while True:
        message, client_address = server_socket.recvfrom(2048)

        if message:
            msg = message.decode("utf-8").replace("'", '"')
            jmsg = json.loads(msg)
            msg_type = jmsg['type']

            if msg_type == 'heartbeat':
                async_task("logserver.tasks.process_heartbeat", message, client_address, q_options={'task_name': 'sniffer-heartbeat'})
            elif msg_type == 'dcc':
                async_task("logserver.tasks.process_rail_message", message, client_address, q_options={'task_name': 'sniffer-message'})
            elif msg_type == 'mfx':
                async_task("logserver.tasks.process_rail_message", message, client_address, q_options={'task_name': 'sniffer-message'})
            else:
                logger.error("Unknown message received, will be discarded.")
