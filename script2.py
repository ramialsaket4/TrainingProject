import socket
import time

target_server = "localhost"
port_number = 3000

def send_request(i):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((target_server, port_number))
            s.sendall(b"Hello")
    except Exception as e:
        print(f"Request {i} failed: {e}")

for i in range(8721684619846513549684132039864526268465132164):
    send_request(i+1)
