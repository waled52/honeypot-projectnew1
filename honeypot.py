import socket
import sqlite3
from datetime import datetime
import threading

running = False

def init_db():
    conn = sqlite3.connect('attacks.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS incidents
        (id INTEGER PRIMARY KEY, ip TEXT, port INTEGER, time TEXT)
    ''')
    conn.commit()
    conn.close()

def log_attack(ip, port):
    conn = sqlite3.connect('attacks.db')
    c = conn.cursor()
    c.execute(
        "INSERT INTO incidents (ip, port, time) VALUES (?, ?, ?)",
        (ip, port, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    )
    conn.commit()
    conn.close()

def start_trap(port):
    global running

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(('0.0.0.0', port))
    server.listen(5)

    while running:
        try:
            client, addr = server.accept()
            log_attack(addr[0], port)
            client.send(b"Access Denied. Security System Active.\n")
            client.close()
        except:
            break

def start_honeypot():
    global running
    if running:
        return

    running = True

    for p in [5000]:
        t = threading.Thread(target=start_trap, args=(p,), daemon=True)
        t.start()

def stop_honeypot():
    global running
    running = False
