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
import time
from datetime import datetime
from random import randint, uniform
import logging
import threading
from django_q.tasks import async_task
from django.conf import settings
import websockets
import json
import asyncio
from asgiref.sync import async_to_sync
from sniffer.models import Sniffer
from railmessages.models import CommandMessage

logger = logging.getLogger("logserver")


class MessagePusher(threading.Thread):

    def __init__(self, name=settings.MESSAGE_PUSHER_THREAD_NAME):
        self._stopevent = threading.Event()
        self._sleepperiod = 0.1
        threading.Thread.__init__(self, name=name)

    def run(self):
        logger.info("Starting Message Pusher")

        event_loop = asyncio.new_event_loop()

        while not self._stopevent.isSet():
            msgs = CommandMessage.objects.filter(console=False)
            for msg in msgs:
                sniffers = Sniffer.objects.filter(is_connected=True)
                console_text = "Kommando %s %s an Adresse %s gesendet" % (msg.command, msg.parameters, msg.address)
                event_loop.run_until_complete(self.send(console_text, len(sniffers)))
                msg.console = True
                try:
                    msg.save()
                except Exception as e:
                    pass
                time.sleep(0.2)

            self._stopevent.wait(self._sleepperiod)

    def join(self, timeout=None) -> None:
        self._stopevent.set()
        threading.Thread.join(self, timeout)

    async def send(self, console_text, sniffers):
        uri = settings.WS_URI

        message = {
            'type': 'console',
            'message': console_text,
            'category': 'undefined',
            'timestamp': datetime.now().strftime('%H:%M:%S.%f')[:-3],
            'second': datetime.now().strftime('%S'),
            'sniffers': sniffers
        }
        async with websockets.connect(uri) as websocket:
            await websocket.send(json.dumps(message))
            await websocket.recv()
