import pyaudio
from protocol import HEADER, FORMAT, DISCONNECT_MESSAGE, CHUNK

def send(s, msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length)) # Padding com espaço
    s.send(send_length)
    s.send(message)

def receive_message(s):
    """Recebe uma mensagem usando o protocolo estabelecido."""
    msg_length = s.recv(HEADER).decode(FORMAT)
    if msg_length:
        msg_length = int(msg_length.strip())
        msg = s.recv(msg_length).decode(FORMAT)
        return msg
    return None

def handle_user(s):
    connected = True
    print("usage:")
    print("PLAY: ___ : choose a certain track to start playing")
    print("LIST_FILES : lists the music tracks available")
    print(f"{DISCONNECT_MESSAGE} : disconnect")

    while connected:
        msg = input()
        
        if msg.startswith("PLAY:"):
            send(s, msg)
            response = receive_message(s)
            if response == "AUDIO_READY":
                print("[AUDIO] Starting playback...")
                stream_audio(s)
            elif response and response.startswith("AUDIO_ERROR"):
                print(f"[ERROR] {response}")

        elif msg == "LIST_FILES":
            send(s, msg)
            response = receive_message(s)
            if response and response.startswith("FILES:"):
                files = response.split(":", 1)[1]
                print(f"Available files: {files}")
        
        elif msg == DISCONNECT_MESSAGE:
            send(s, msg)
            connected = False

def stream_audio(s):
    """Recebe e reproduz o stream de áudio do servidor."""
    try:
        # Inicializa PyAudio
        p = pyaudio.PyAudio()
        
        # Configura o stream de saída (16-bit, 44.1kHz, stereo)
        stream = p.open(format=pyaudio.paInt16,
                       channels=2,
                       rate=44100,
                       output=True,
                       frames_per_buffer=1024)
        
        print("[AUDIO] Playing audio...")
        
        # Recebe e reproduz chunks de áudio
        while True:
            chunk = s.recv(CHUNK)
            if not chunk or len(chunk) == 0:
                break
            stream.write(chunk)
        
        print("[AUDIO] Playback finished")
        
        # Limpa recursos
        stream.stop_stream()
        stream.close()
        p.terminate()
        
    except Exception as e:
        print(f"[AUDIO ERROR] Playback error: {e}")