import json
from channels.generic.websocket import WebsocketConsumer
from random import randint, uniform
import time
from datetime import datetime
from sniffer.models import Sniffer
from logserver.helper import Helper
import logging

logger = logging.getLogger("logserver")


class ConsoleConsumerSimulator(WebsocketConsumer):
    simulator = True
    i = 0
    helper = Helper()

    def connect(self):
        self.accept()

    def disconnect(self, code):
        pass

    def receive(self, text_data=None, bytes_data=None):

        logger.info("client connected %s" % text_data)

        text_data_json = json.loads(text_data)
        if text_data_json['message'] == "ready":

            while True:
                sniffers = Sniffer.objects.filter(is_connected=True)
                messages = [
                    ('Loco #%s changed speed to %s (V as Step)' % (randint(1, 25), randint(0, 255)), 'loco'),
                    ('Loco #%s issued function F%s' % (randint(1, 25), randint(1, 20)), 'loco'),
                    ('Switch %s switched to left' % randint(1, 999), 'switch'),
                    ('Switch %s switched to right' % randint(1, 999), 'switch'),
                    ('Signal %s now halt' % randint(1, 500), 'signal'),
                    ('Signal %s now attention' % randint(1, 500), 'signal'),
                    ('Signal %s now go' % randint(1, 500), 'signal'),
                    ('Lost connection to asset %s ' % randint(1, 50), 'connection'),
                    ('Connection to asset %s established' % randint(1, 50), 'connection'),
                ]

                msg_types = [
                    'console',
                    'unplausible'
                ]

                message = randint(0, 7)
                msg_range = uniform(0.0, 10.0)
                msg_type = 1

                if msg_range < 9.9:
                    msg_type = 0

                self.send(
                    text_data=json.dumps({
                        'type': msg_types[msg_type],
                        'message': messages[message][0],
                        'category': messages[message][1],
                        'timestamp': datetime.now().strftime('%H:%M:%S.%f')[:-3],
                        'second': datetime.now().strftime('%S'),
                        'sniffers': len(sniffers)
                    })
                )
                time.sleep((randint(1, 50) / 100))
