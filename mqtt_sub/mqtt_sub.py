import logging
import signal
import sys
from paho.mqtt import client as mqtt_client
import update_db
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def connect_mqtt(broker, client_id, port):
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            logger.info("Connected to MQTT Broker!")
        else:
            logger.error(f"Failed to connect, return code {rc}")

    def on_disconnect(client, userdata, rc):
        if rc != 0:
            logger.warning(f"Unexpected disconnection. Trying to reconnect...")
            client.reconnect()

    client = mqtt_client.Client(client_id)
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.connect(broker, port)
    return client


def get_timestamp():
    current_datetime = datetime.now()
    current_time = current_datetime.strftime("%H:%M:%S")
    current_date = current_datetime.strftime("%d/%m/%Y")
    return current_time, current_date

def on_message(client, userdata, msg):
    try:
        msg = msg.payload.decode()
        feedback = msg[0:10]
        location = msg[10:-3]
        dbm = msg[-3:]
        recived_time, recived_date = get_timestamp()
        logger.info(f"Received message: {feedback} at {recived_time}, {recived_date}")
        update_db.insert_to_db(feedback, recived_time, recived_date, location)
        logger.info(f'Inserted message: {feedback}, {recived_date}, {recived_time} to db')
    except Exception as e:
        logger.error(f"Error processing message: {e}")

def subscribe(client, topic):
    client.subscribe(topic)
    client.on_message = on_message

def run():
    broker = '10.120.0.23'
    client_id = 'mqtt_subscriber_vm'
    topic = "ratings"
    port = 1883

    client = connect_mqtt(broker, client_id, port)
    subscribe(client, topic)

    def on_exit(signum, frame):
        logger.info("Shutting down gracefully...")
        client.disconnect()
        sys.exit(0)

    signal.signal(signal.SIGINT, on_exit)

    try:
        client.loop_forever()
    except KeyboardInterrupt:
        logger.info("Keyboard interrupt received. Exiting...")

if __name__ == "__main__":
    run()