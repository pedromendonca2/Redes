import os
import threading
from pydub import AudioSegment
from pydub.utils import make_chunks

class AudioHandler:
    def __init__(self, media_directory="../media"):
        self.media_directory = media_directory
        self.current_audio = None
        self.audio_chunks = []
        self.current_chunk_index = 0
        self.is_playing = False
        self.audio_lock = threading.Lock()
        
    def load_audio_file(self, filename):
        """Carrega um arquivo MP3 e converte para chunks de áudio."""
        file_path = os.path.join(self.media_directory, filename)
        
        if not os.path.exists(file_path):
            print(f"[AUDIO ERROR] File not found: {file_path}")
            return False
            
        try:
            # Carrega o arquivo MP3
            audio = AudioSegment.from_mp3(file_path)
            
            # Converte para formato adequado para streaming (16-bit, 44.1kHz, stereo)
            audio = audio.set_frame_rate(44100).set_channels(2).set_sample_width(2)
            
            # Divide em chunks de 1024 frames cada
            chunk_length_ms = int((1024 / 44100) * 1000)  # converte frames para milissegundos
            chunks = make_chunks(audio, chunk_length_ms)
            
            with self.audio_lock:
                self.current_audio = audio
                self.audio_chunks = [chunk.raw_data for chunk in chunks]
                self.current_chunk_index = 0
                
            print(f"[AUDIO] Loaded {filename}: {len(chunks)} chunks, {len(audio)}ms duration")
            return True
            
        except Exception as e:
            print(f"[AUDIO ERROR] Failed to load {filename}: {e}")
            return False
    
    def get_next_chunk(self):
        """Retorna o próximo chunk de áudio para streaming."""
        with self.audio_lock:
            if not self.audio_chunks or self.current_chunk_index >= len(self.audio_chunks):
                return None
                
            chunk = self.audio_chunks[self.current_chunk_index]
            self.current_chunk_index += 1
            return chunk
    
    def reset_playback(self):
        """Reinicia a reprodução do arquivo atual."""
        with self.audio_lock:
            self.current_chunk_index = 0
            
    def has_more_chunks(self):
        """Verifica se ainda há chunks para enviar."""
        with self.audio_lock:
            return self.current_chunk_index < len(self.audio_chunks)
    
    def get_available_files(self):
        """Lista todos os arquivos MP3 disponíveis no diretório de mídia."""
        try:
            if os.path.exists(self.media_directory):
                files = [f for f in os.listdir(self.media_directory) if f.lower().endswith('.mp3')]
                return files
            return []
        except Exception as e:
            print(f"[AUDIO ERROR] Failed to list files: {e}")
            return []
