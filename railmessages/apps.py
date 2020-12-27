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
import queue

from django.apps import AppConfig
from django.db import connection

from logserver.dccpi import DCCDecoder

logger = logging.getLogger(__name__)


class RailmessagesConfig(AppConfig):
    name = 'railmessages'
    q = queue.Queue()
    threadpool = []

    def ready(self):
        # print("Start transformer thread")
        # logger.info("Start transformer thread")
        # transform = threading.Thread(target=transform_messages, name='transform-thread', daemon=True)
        # transform.start()
        # self.threadpool.append(transform)
        pass


def transform_messages():
    from .models import RawMessage

    while True:
        raw_messages = RawMessage.objects.all()

        for raw_message in raw_messages:
            print("TRANSFORMED %s" % raw_message.msg_json)

            decoder = DCCDecoder('0b' + raw_message.msg_raw)
            address = decoder.get_address()
            command = decoder.get_command()

            print('got address %d' % address)
            print(command)

            if raw_message.id is not None:
                if raw_message.id > 10_000:
                    print("alter sequence")
                    with connection.cursor() as cursor:
                        cursor.execute("update main.sqlite_sequence set seq = 0 where name = 'railmessages_rawmessage'")

            raw_message.delete()


def send_message_to_client():
    pass
