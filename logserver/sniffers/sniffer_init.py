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

import logging
import threading
import time

from appsettings.models import Appsettings
from .sniffer_manager import check_active_sniffer
from .sniffer_server import sniffer_server

logger = logging.getLogger(__name__)
stop_threads = False


class SnifferInit:
    stop_threads = False
    listen = None
    port = 0
    threadpool = []

    def __init__(self):
        self.listen = Appsettings.objects.filter(key='listensniffers').values('value').get()['value']
        self.port = int(Appsettings.objects.filter(key='listenport').values('value').get()['value'])

    def stop_all_threads(self):
        for thread in self.threadpool:
            thread.join()

    # Start the check thread to check for active sniffers
    def start_sniffer_manager_thread(self):
        check_thread = threading.Thread(target=check_active_sniffer, name='manager-thread', daemon=True)
        check_thread.start()
        self.threadpool.append(check_thread)

    # Start the sniffer server to listen for new messages
    def start_sniffer_server_thread(self):
        if self.listen is not None:
            sniffer_thread = threading.Thread(target=sniffer_server, args=(self.port,), name='sniffer-thread',
                                              daemon=True)
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

    def start_thread_checking_q(self):
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
