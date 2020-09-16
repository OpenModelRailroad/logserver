from django.apps import AppConfig
import socket
import threading
import json


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

            obj, created = Sniffer.objects.update_or_create(
                hostname=jmsg['hostname'],
                ip=jmsg['ip'],
                mac=jmsg['mac'],
                is_connected=True
            )

            if created:
                print('insert or updated sniffer %s (%s)' % (jmsg['mac'], jmsg['ip']))
            else:
                print('some error happend while insert or update %s (%s)' % (jmsg['mac'], jmsg['ip']))
