import json
import os
import sys

from channels.generic.websocket import WebsocketConsumer

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'engine')))
from runtime import Runtime  # import runtime in connect to avoid None import
runtime = Runtime.getInstance()


class DoorConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()
    
    def disconnect(self, code):
        return super().disconnect(code)
    
    def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)
        if data.get('message') == 'get_status':
            self.send(text_data=json.dumps({
                "signal": "200",
                "command": data.get('message'),
                "message": runtime.door.status
                })
            )
        elif data.get('message') == 'open':
            runtime.door.move(2)
            self.send(text_data=json.dumps({
                "signal": "200",
                "command": data.get('message'),
                "message": "Door is opening"
                })
            )
        elif data.get('message') == 'close':
            runtime.door.move(1)
            self.send(text_data=json.dumps({
                "signal": "200",
                "command": data.get('message'),
                "message": "Door is closing"
                })
            )
        else:
            self.send(text_data=json.dumps({
                "signal": "400",
                "command": data.get('message'),
                "message": "Invalid request"
                })
            )
