import logging
import threading
import time

from django.apps import AppConfig

from sniffer.sniffer_manager import check_active_sniffer
from sniffer.sniffer_server import sniffer_server

logger = logging.getLogger(__name__)
stop_threads = False


class SnifferConfig(AppConfig):
    name = 'sniffer'
    stop_threads = False

    listen = None
    port = 0
    threadpool = []

    def ready(self):
        from appsettings.models import Appsettings

        self.listen = Appsettings.objects.filter(key='listensniffers').values('value').get()['value']
        self.port = int(Appsettings.objects.filter(key='listenport').values('value').get()['value'])

        self.start_sniffer_manager_thread()
        self.start_sniffer_server_thread()

        threading.Thread(target=self.start_thread_checking, name="checking-thread").start()

    # Start the check thread to check for active sniffers
    def start_sniffer_manager_thread(self):
        check_thread = threading.Thread(target=check_active_sniffer, name='manager-thread')
        check_thread.start()
        self.threadpool.append(check_thread)

    # Start the sniffer server to listen for new messages
    def start_sniffer_server_thread(self):
        if self.listen is not None:
            sniffer_thread = threading.Thread(target=sniffer_server, args=(self.port,), name='sniffer-thread')
            sniffer_thread.start()
            self.threadpool.append(sniffer_thread)

    def start_thread_checking(self):
        if len(self.threadpool) > 0:
            print(self.threadpool)
            while True:
                for thread in self.threadpool:
                    if not thread.is_alive():
                        print("thread %s is dead, try to restart" % thread.name)
                        self.threadpool.remove(thread)
                        if thread.name == 'manager-thread':
                            self.start_sniffer_manager_thread()
                        elif thread.name == 'sniffer-thread':
                            self.start_sniffer_server_thread()
                time.sleep(10)
