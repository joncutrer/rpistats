from . import Publisher

import grpc

class GrpcPublisher:
    def __init__(self, host, port):
        self.channel = grpc.insecure_channel(f'{host}:{port}')
        # self.client = GeneratedClient(self.channel)  # Assuming a GeneratedClient is defined from .proto files

    async def publish(self, data):
        print("Data sent via gRPC")
        # response = self.client.sendData(data)
        # print("gRPC response:", response)
