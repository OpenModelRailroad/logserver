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
import time
from django.conf import settings
from .sniffer_manager import SnifferManager
from .sniffer_server import SnifferServer
from .message_pusher import MessagePusher

logger = logging.getLogger(__name__)
stop_threads = False


class SnifferInit:
    stop_threads = False
    threadpool = []

    def __init__(self):
        self.sniffer_manager_running = True
        self.sniffer_server_running = True
        self.message_pusher_running = True

    def set_message_pusher_running(self, status):
        self.message_pusher_running = status

    def is_message_pusher_running(self):
        return self.message_pusher_running

    def set_sniffer_manager_running(self, status):
        self.sniffer_manager_running = status

    def is_sniffer_manager_running(self):
        return self.sniffer_manager_running

    def set_sniffer_server_running(self, status):
        self.sniffer_server_running = status

    def is_sniffer_server_running(self):
        return self.sniffer_server_running

    def stop_all_threads(self):
        self.set_sniffer_manager_running(False)
        self.set_sniffer_server_running(False)
        self.set_message_pusher_running(False)
        for thread in self.threadpool:
            thread.join()

    def stop_named_thread(self, threadname):
        for thread in self.threadpool:
            if thread.name == threadname:
                thread.join()

    def stop_sniffer_manager_thread(self):
        self.set_sniffer_manager_running(False)
        self.stop_named_thread(settings.SNIFFER_MANAGER_THREAD_NAME)

    def stop_sniffer_server_thread(self):
        logger.info("Stopping Sniffer Server")
        self.set_sniffer_server_running(False)
        self.stop_named_thread(settings.SNIFFER_SERVER_THREAD_NAME)

    def stop_message_pusher_thread(self):
        logger.info("Stopping Message Pusher")
        self.set_message_pusher_running(False)
        self.stop_named_thread(settings.MESSAGE_PUSHER_THREAD_NAME)

    def start_message_pusher_thread(self):
        self.set_message_pusher_running(True)
        pusher_thread = MessagePusher()
        pusher_thread.start()

    # Start the check thread to check for active sniffers
    def start_sniffer_manager_thread(self):
        self.set_sniffer_manager_running(True)
        manager_thread = SnifferManager()
        manager_thread.start()

    # Start the sniffer server to listen for new messages
    def start_sniffer_server_thread(self):
        self.set_sniffer_server_running(True)
        sniffer_server_thread = SnifferServer(settings.SNIFFER_CONNECT_TO_PORT)
        sniffer_server_thread.start()
        self.threadpool.append(sniffer_server_thread)

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
