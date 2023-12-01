import time
import random
from paho.mqtt import client as mqtt_client
import update_db
from datetime import datetime


def main():

    broker = '10.100.0.96'
    client_id = 'mqtt_subscriber_vm'
    topic = "ratings"


    m_port = 1883


    def connect_mqtt() -> mqtt_client:
        def on_connect(client, userdata, flags, rc):
            if rc == 0:
                print("Connected to MQTT Broker!")
            else:
                print("Failed to connect, return code %d\n", rc)
        
        client = mqtt_client.Client(client_id) 
        client.on_connect = on_connect
        client.connect(broker,m_port)
        return client

    def get_timestamp():
        current_datetime = datetime.now()
        current_time = current_datetime.strftime("%H:%M:%S")
        current_date = current_datetime.strftime("%d/%m/%Y")
        return (current_time, current_date)
    
    def subscribe(client: mqtt_client):
        def on_message(client, userdata, msg):
            msg = msg.payload.decode()
            recived_time, recivede_date = get_timestamp()
            location = random.choice(['aarhus', 'copenhagen', 'allborg', 'skive', 'viborg'])
            print(f"Received message: {msg} at {recived_time}, {recivede_date}")
            update_db.insert_to_db(msg, recived_time, recivede_date, location)
            print(f'inserted message:{msg}, {recivede_date}, {recived_time} to db\n')
        client.subscribe(topic)
        client.on_message = on_message

    def run():
        client = connect_mqtt()
        subscribe(client)
        client.loop_forever()
    run()


if __name__ == "__main__":
    main()
