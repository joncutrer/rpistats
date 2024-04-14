from . import Publisher
from websocket import create_connection
import json

class WebSocketPublisher:
    def __init__(self, uri):
        self.ws = create_connection(uri)

    async def publish(self, data):
        self.ws.send(json.dumps(data))
        print("Data sent via WebSocket")
