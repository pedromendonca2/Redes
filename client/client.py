import socket
from protocol import HOST, PORT
from audio_player import handle_user

def start():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        print(f"Connected to {HOST}:{PORT}.")

        handle_user(s)

print("[STARTING] client is starting...")
start()