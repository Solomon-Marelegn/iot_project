import socket
import net

def ping():
    google_ip = "8.8.8.8"
    port = 53 

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        sock.connect((google_ip, port))
        return True

    except Exception as e:
        return False

    finally:
        sock.close()



