import grpc

class GrpcPublisher:
    def __init__(self, host, port):
        self.channel = grpc.insecure_channel(f'{host}:{port}')
        # self.client = GeneratedClient(self.channel)  # Assuming a GeneratedClient is defined from .proto files

    def publish(self, data):
        print("Data sent via gRPC")
        # response = self.client.sendData(data)
        # print("gRPC response:", response)
