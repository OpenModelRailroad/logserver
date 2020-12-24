from socket import *
import logging
import json
from django_q.tasks import async_task

logger = logging.getLogger("logserver")
server_socket = None


def sniffer_server(port):
    logger.info("Starting Sniffer Server on port %s" % port)
    global server_socket
    server_socket = socket(AF_INET, SOCK_DGRAM)
    server_socket.bind(('', port))
    logger.info("Sniffer Server Ready to receive data")

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
