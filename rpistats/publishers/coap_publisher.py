from . import Publisher

from coapthon.client.helperclient import HelperClient
import json

class CoapPublisher:
    def __init__(self, host, port):
        self.client = HelperClient(server=(host, port))

    async def publish(self, data):
        response = self.client.post("coap://server/resource", json.dumps(data))
        print("Data sent via CoAP:", response.pretty_print())
