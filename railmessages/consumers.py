import logging
from channels.generic.websocket import WebsocketConsumer

logger = logging.getLogger(__name__)


class RailMessageConsumer(WebsocketConsumer):

    def connect(self):
        self.accept()

    def disconnect(self, code):
        pass

    def receive(self, text_data=None, bytes_data=None):
        print(text_data)
