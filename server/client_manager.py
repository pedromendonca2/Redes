import socket
import threading
from protocol import HEADER, FORMAT, DISCONNECT_MESSAGE

def handle_client(conn, addr, audio_handler=None):
    connected = True
    while connected:
        try:
            msg_length = conn.recv(HEADER).decode(FORMAT)
            if not msg_length:
                break
                
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            
            if msg == DISCONNECT_MESSAGE:
                break
                
            print(f"[{addr}] {msg}")
            
            # Processa comandos de áudio
            if audio_handler and msg.startswith("PLAY:"):
                filename = msg.split(":", 1)[1]
                if audio_handler.load_audio_file(filename):
                    send_message(conn, "AUDIO_READY")
                    stream_audio_to_client(conn, addr, audio_handler)
                else:
                    send_message(conn, "AUDIO_ERROR:File not found")
                    
            elif audio_handler and msg == "LIST_FILES":
                files = audio_handler.get_available_files()
                file_list = ",".join(files) if files else "No files available"
                send_message(conn, f"FILES:{file_list}")
                
            else:
                send_message(conn, f"Echo: {msg}")
                
        except Exception as e:
            print(f"[ERROR] Error handling client {addr}: {e}")
            break

    conn.close()

def send_message(conn, message):
    """Envia uma mensagem usando o protocolo estabelecido."""
    message_bytes = message.encode(FORMAT)
    msg_length = len(message_bytes)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    
    conn.send(send_length)
    conn.send(message_bytes)

def stream_audio_to_client(conn, addr, audio_handler):
    """Envia chunks de áudio para o cliente."""
    try:
        print(f"[AUDIO] Starting stream to {addr}")
        
        chunk_count = 0
        while audio_handler.has_more_chunks():
            chunk = audio_handler.get_next_chunk()
            if chunk is None:
                break
                
            # Envia o chunk diretamente (dados binários)
            conn.send(chunk)
            chunk_count += 1
            
        print(f"[AUDIO] Finished streaming {chunk_count} chunks to {addr}")
        
        # Sinaliza fim do stream fechando a conexão de envio
        conn.shutdown(socket.SHUT_WR)
        
    except Exception as e:
        print(f"[AUDIO ERROR] Error streaming to {addr}: {e}")
