import pyaudio
import socket

# Configuration
CHUNK = 1024  # Same as sender
FORMAT = pyaudio.paInt16  # Same as sender
CHANNELS = 1  # Same as sender
RATE = 32000  # Same as sender
HOST = '0.0.0.0'  # Listen on all interfaces
PORT = 5000  # Port to receive data

# Initialize PyAudio
audio = pyaudio.PyAudio()
stream = audio.open(format=FORMAT, channels=CHANNELS,
                    rate=RATE, output=True, frames_per_buffer=CHUNK)

# Initialize socket
# sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((HOST, PORT))
sock.listen(1)

print("Receiving audio...")
try:
    while True:
        data, addr = sock.recvfrom(CHUNK * 2)  # 2 bytes per sample
        stream.write(data)
except KeyboardInterrupt:
    print("Stopping...")
finally:
    stream.stop_stream()
    stream.close()
    audio.terminate()
    sock.close()

