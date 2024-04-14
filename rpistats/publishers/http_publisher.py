from . import Publisher

import requests

class HttpPublisher:
    def __init__(self, url):
        self.url = url

    async def publish(self, data):
        response = requests.post(self.url, json=data)
        print(f"Data posted via HTTP: {response.status_code}")
