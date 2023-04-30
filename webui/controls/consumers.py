import json

from channels.generic.websocket import WebsocketConsumer
from controls.views import runtime

class DashboardConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)
        self.send(text_data=json.dumps({
            "message": runtime.door.get_status()
            })
        )  # send door status