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

from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from logserver.helper import Helper
from sniffer.models import Sniffer
from railmessages.models import CommandMessage
from console.models import Clients

logger = logging.getLogger("logserver")


class ConsoleConsumer(WebsocketConsumer):
    def connect(self):
        # Join room group

        async_to_sync(self.channel_layer.group_add)(
            'chat',
            self.channel_name
        )
        Clients.objects.create(channel_name=self.channel_name)
        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            'chat',
            self.channel_name
        )
        Clients.objects.filter(channel_name=self.channel_name).delete()

    def receive(self, text_data=None, bytes_data=None):
        async_to_sync(self.channel_layer.group_send)(
            "chat",
            {
                "type": "chat_message",
                "text": text_data,
            },
        )

    def chat_message(self, event):
        async_to_sync(self.send(text_data=event["text"]))
