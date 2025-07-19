from protocol import HEADER, FORMAT, DISCONNECT_MESSAGE, CHUNK

def send(s, msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length)) # Padding com espaço
    s.send(send_length)
    s.send(message)

def handle_user(s):
    connected = True
    print("usage:")
    print("PLAY: ___ : choose a certain track to start playing")
    print("LIST_FILES : lists the music tracks available")
    print(f"{DISCONNECT_MESSAGE} : disconnect")

    # TODO implementar pause e play enquanto uma música está sendo streamada

    while connected:
        msg = input()
        
        if msg.startswith("PLAY:"):
            send(s, msg)
            stream_audio(s)

        elif msg == "LIST_FILES":
            send(s, msg)
        
        elif msg == DISCONNECT_MESSAGE:
            send(s, msg)
            connected = False # sai do loop
            # e desconecta no client.py
            # já que a conexão foi feita por um with

def stream_audio(s):
    s.recieve(CHUNK) # TODO definir tamanho consistente para CHUNKS
    # TODO encontrar a melhor interpretação para o audio player. pydub ou pyaudio?