from socket import *
import logging
import json
from datetime import datetime
from django.utils import timezone
import pytz

logger = logging.getLogger(__name__)


def sniffer_server(port):
    from .models import Sniffer
    from railmessages.models import RawMessage

    logger = logging.getLogger(__name__)

    print("Starting Sniffer Server on port %s" % port)
    server_socket = socket(AF_INET, SOCK_DGRAM)
    server_socket.bind(('', port))
    print("Sniffer Server Ready to receive data")

    while True:
        message, client_address = server_socket.recvfrom(2048)
        # print(message, client_address, client_address[1])

        if message:
            msg = message.decode("utf-8").replace("'", '"')
            jmsg = json.loads(msg)
            msg_type = jmsg['type']

            if msg_type == 'heartbeat':
                try:
                    e = Sniffer.objects.get(mac=jmsg['mac'])
                    e.ip = jmsg['ip']
                    e.hostname = jmsg['hostname']
                    e.is_connected = True
                    e.port = client_address[1]
                    e.last_connection = timezone.now()
                    e.save()

                    logger.info('updated sniffer %s (%s)' % (jmsg['mac'], jmsg['ip']))

                except Sniffer.DoesNotExist:
                    Sniffer.objects.create(
                        hostname=jmsg['hostname'],
                        ip=jmsg['ip'],
                        mac=jmsg['mac'],
                        is_connected=True,
                        last_connection=timezone.now(),
                        port=client_address[1],
                    ).save()

                    print('created sniffer %s (%s)' % (jmsg['mac'], jmsg['ip']))
            elif msg_type == 'dcc':
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
                    print("this sniffer does not exist. packet cannot be saved")
