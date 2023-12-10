

#assigne gpio for buttons
#connect to the internet : wifi indicater led on
#listen to button inputs in a loop and send MQTT message to the given topic

from machine import Pin
import net
from mqtt_pub import MQTT_Publisher
import time
import utime
import my_lcd

mac, dbm = net.net_connect()
led = Pin('LED', Pin.OUT)
led.on()

#define 3 button
pleased =  Pin(13, Pin.IN, Pin.PULL_DOWN)
neutral =  Pin(14, Pin.IN, Pin.PULL_DOWN)
displeased = Pin(15, Pin.IN, Pin.PULL_DOWN)

info = [(pleased, 'pleased' + 3 * ' ' ),
        (neutral, 'neutral'+ 3 * ' ' ),
        (displeased, 'displeased')]

broker = '10.100.0.96'
client_id = 'pico_mqtt_publisher'
topic = "ratings"
mq = MQTT_Publisher(broker, client_id, topic)


def kontakt_pral(button):
    while button.value():
        pass
    else:
        time.sleep(0.15)

count = 0
while True:
    for i in info:
        
        if i[0].value() == 1:
            count += 1
            my_lcd.dis(f'sent_msg: {count}')
            message = i[1] + mac + str(dbm)
            mq.publish((message))
            print('published:', message[0:10])
            kontakt_pral(i[0])



