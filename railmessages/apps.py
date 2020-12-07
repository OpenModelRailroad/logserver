from django.apps import AppConfig
from .dccpi import *
import threading
import logging
import queue
from django.db import connection

logger = logging.getLogger(__name__)


class RailmessagesConfig(AppConfig):
    name = 'railmessages'
    q = queue.Queue()
    threadpool = []

    def ready(self):
        print("Start transformer thread")
        logger.info("Start transformer thread")
        transform = threading.Thread(target=transform_messages, name='transform-thread')
        transform.start()
        self.threadpool.append(transform)


def transform_messages():
    from .models import RawMessage

    while True:
        raw_messages = RawMessage.objects.all()

        for raw_message in raw_messages:
            print("TRANSFORMED %s" % raw_message.msg_json)

            if raw_message.id is not None:
                if raw_message.id > 10_000:
                    print("alter sequence")
                    with connection.cursor() as cursor:
                        cursor.execute("update main.sqlite_sequence set seq = 0 where name = 'railmessages_rawmessage'")

            raw_message.delete()


def send_message_to_client():
    pass
