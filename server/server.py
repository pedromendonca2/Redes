import socket
import threading
from protocol import HOST, PORT
from client_manager import handle_client
from audio_handler import AudioHandler

# Instancia global do audio handler
audio_handler = AudioHandler()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))

def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {HOST}:{PORT}")
    
    # Lista arquivos disponíveis na inicialização
    available_files = audio_handler.get_available_files()
    print(f"[AUDIO] Available files: {available_files}")
    
    while True:
        conn, addr = server.accept() # new socket conn will interact with the address returned, which includes the port 
        thread = threading.Thread(target=handle_client, args=(conn, addr, audio_handler))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")

print("[STARTING] server is starting...")
start()