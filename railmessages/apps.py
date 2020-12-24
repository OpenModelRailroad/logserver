from django.apps import AppConfig
import logging
import queue
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
