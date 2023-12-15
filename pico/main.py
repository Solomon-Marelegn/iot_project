
from machine import Pin
import net
from mqtt_pub import MQTT_Publisher
import utime
#import my_lcd
import network
import ping


led = Pin('LED', Pin.OUT)

def get_ap_mac():
    ssid = 'iot-network'
    password = "test!12345"
    mac = net.net_connect(ssid, password)
    if mac:
        led.on()
    return mac

def check_wifi():
    print('checking')
    return ping.ping()


def reconnect():
    led.off()
    mac = get_ap_mac()

    return mac if mac is not None else get_ap_mac()


def kontakt_pral(button):
    while button.value():
        pass
    else:
        utime.sleep(0.10)

def send_message(btn_label_pairs, mq, mac):
    for btn, label in btn_label_pairs:
        if btn.value() == 1:
            _time, _date = get_timestamp()
            message = f"{label}{mac}{_time}{_date}"
            try:
                output = mq.publish(message)
                if output:
                    print(f"Published: {message}")
                    kontakt_pral(btn)
            except Exception as e:
                print(f"Error sending message: {e}")

def get_timestamp(mode=None):
    current_time = utime.localtime()
    if mode is None:
        formatted_time = "{:02}:{:02}:{:02}".format(current_time[3], current_time[4], current_time[5])
        formatted_date = "{:02}/{:02}/{:04}".format(current_time[2], current_time[1], current_time[0])
        return formatted_time, formatted_date
    
    elif mode =='unformated':
        return int("{:02}{:02}{:02}".format(current_time[3],
                                            current_time[4],
                                            current_time[5]))

def main():
    mac = get_ap_mac()

    pleased = Pin(13, Pin.IN, Pin.PULL_DOWN)
    neutral = Pin(14, Pin.IN, Pin.PULL_DOWN)
    displeased = Pin(15, Pin.IN, Pin.PULL_DOWN)

    btn_label_pairs = [
        (pleased, 'pleased' + 3 * ' '),
        (neutral, 'neutral' + 3 * ' '),
        (displeased, 'displeased')
    ]

    broker = '192.168.2.18'
    client_id = 'pico_mqtt_publisher'
    topic = "ratings"
    mq = MQTT_Publisher(broker, client_id, topic)

    #my_lcd.display_msg("Service Rating")

    reference_time = get_timestamp('unformated')

    while True:
        current_time = get_timestamp('unformated')
        if current_time - reference_time >= 1500 :
            if check_wifi():
                pass
            else:
                mac = reconnect()
            reference_time = current_time
        send_message(btn_label_pairs, mq, mac)

if __name__ == "__main__":
    main()



