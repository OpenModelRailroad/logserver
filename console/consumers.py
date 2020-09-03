import json
from channels.generic.websocket import WebsocketConsumer
from random import randint
import time
from datetime import datetime
from .models import Sniffer


class ConsoleConsumerSimulator(WebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, code):
        pass

    def receive(self, text_data=None, bytes_data=None):
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
                message = randint(0, 7)

                self.send(
                    text_data=json.dumps({
                        'message': messages[message][0],
                        'category': messages[message][1],
                        'timestamp': datetime.now().strftime('%H:%M:%S.%f')[:-3],
                        'sniffers': len(sniffers)
                    })
                )
                time.sleep((randint(1, 50) / 100))
