import paho.mqtt.client as mqtt
import json

class MqttPublisher:
    def __init__(self, broker, port, topic, username, password):
        self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
        self.topic = topic
        self.client.username_pw_set(username, password)
        self.client.connect(broker, port, 60)
        self.client.loop_start()

    def publish(self, data):
        msg = json.dumps(data)
        result = self.client.publish(self.topic, msg)
        print(f"Publishing {msg} to topic {self.topic}")
