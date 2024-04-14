from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import json

class AwsIotPublisher:
    def __init__(self, endpoint, client_id, path_to_certificate, path_to_private_key, path_to_root_ca):
        self.myAWSIoTMQTTClient = AWSIoTMQTTClient(client_id)
        self.myAWSIoTMQTTClient.configureEndpoint(endpoint, 8883)
        self.myAWSIoTMQTTClient.configureCredentials(path_to_root_ca, path_to_private_key, path_to_certificate)

    def publish(self, data):
        topic = "sdk/test/Python"
        self.myAWSIoTMQTTClient.connect()
        self.myAWSIoTMQTTClient.publish(topic, json.dumps(data), 1)
        print("Data published to AWS IoT")
        self.myAWSIoTMQTTClient.disconnect()
