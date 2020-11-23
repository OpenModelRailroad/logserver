from django.apps import AppConfig
import socket
import threading
import json
import logging

logger = logging.getLogger('main')


class SnifferConfig(AppConfig):
    name = 'sniffer'

    def ready(self):
        from appsettings.models import Appsettings

        listen = Appsettings.objects.filter(key='listensniffers').values('value').get()['value']
        port = int(Appsettings.objects.filter(key='listenport').values('value').get()['value'])

        if listen is not None:
            threading.Thread(target=sniffer_server, args=(port,), name='sniffer-thread').start()


def sniffer_server(port):
    from .models import Sniffer

    print("Starting Sniffer Connection Server on port %s" % port)

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('localhost', port)

    sock.bind(server_address)
    sock.listen()

    while True:
        connection, client_address = sock.accept()
        data = connection.recv(1248)
        if data:
            connection.sendall(client_address[0].encode())
            print(client_address, ": ", data)

            msg = data.decode("utf-8").replace("'", '"')
            jmsg = json.loads(msg)

            try:
                e = Sniffer.objects.get(mac=jmsg['mac'])
                e.ip = jmsg['ip']
                e.hostname = jmsg['hostname']
                e.is_connected = True
                e.save()

                print('updated sniffer %s (%s)' % (jmsg['mac'], jmsg['ip']))

            except Sniffer.DoesNotExist:
                Sniffer.objects.create(
                    hostname=jmsg['hostname'],
                    ip=jmsg['ip'],
                    mac=jmsg['mac'],
                    is_connected=True,
                ).save()

                print('created sniffer %s (%s)' % (jmsg['mac'], jmsg['ip']))

            connection.close()
