import socket
import time

target_server = "localhost"
port_number = 3000

def send_request():
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((target_server, port_number))
            s.sendall(b"Hello")
    except Exception as e:
        print(f"Connection error: {e}")

while True:
    send_request()
