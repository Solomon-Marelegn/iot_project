import network
import time

def get_signal_strength(ap):
    return ap[3]

def net_connect():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)

    available_aps = [ap for ap in wlan.scan() if ap[0].decode('utf-8') == "IOT-project"]

    if not available_aps:
        print("No access points with SSID 'IOT-project' found.")
        return

    sorted_aps = sorted(available_aps, key=get_signal_strength, reverse=True)

    selected_ap = sorted_aps[0]
    ssid = selected_ap[0].decode('utf-8')
    password = "test!12345"
    mac_address = ':'.join(['{:02x}'.format(b) for b in selected_ap[1]])
    wlan.connect(ssid, password)

    timeout = 20  # Adjust the timeout value as needed
    start_time = time.time()

    while not wlan.isconnected():
        print('Connecting to {}: Waiting...'.format(ssid))
        time.sleep(1)

        if time.time() - start_time > timeout:
            print('Connection timeout. Unable to connect to {}.'.format(ssid))
            break

    if wlan.isconnected():
        ip = wlan.ifconfig()[0]
        print(f"mac {mac_address}, dbm {selected_ap[3]}")
        return (mac_address, selected_ap[3])
    
     

