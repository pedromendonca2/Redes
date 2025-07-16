import threading
from protocol import HEADER, FORMAT, DISCONNECT_MESSAGE

def handle_client(conn, addr):
    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        msg_length = int(msg_length)
        msg = conn.recv(msg_length).decode(FORMAT)
        if msg == DISCONNECT_MESSAGE:
            break

        print(f"[{addr}] {msg}")

    conn.close()
