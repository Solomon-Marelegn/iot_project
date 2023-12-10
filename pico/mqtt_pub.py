import network, time
from machine import Pin, UART
from simple import MQTTClient

class MQTT_Publisher():
    def __init__(self, broker, client_id, topic):
        self.broker = broker
        self.client_id = client_id
        self.topic = topic
        self.client = self.connect()

    def connect(self):
        client = MQTTClient(self.client_id, self.broker, keepalive=3600)
        client.connect()
        print('Connected to %s MQTT Broker' % self.broker)
        return client

    def publish(self, message):
            self.client.publish(self.topic, message)
    




