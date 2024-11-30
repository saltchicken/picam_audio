import pyaudio
import socket

# Configuration
CHUNK = 1024  # Number of audio samples per frame
FORMAT = pyaudio.paInt16  # 16-bit resolution
CHANNELS = 1  # Mono audio
RATE = 32000  # Sampling rate in Hz
HOST = '10.0.0.3'  # Replace with receiver's IP address
PORT = 5000  # Port to send data

device_index = 0

# Initialize PyAudio
audio = pyaudio.PyAudio()
stream = audio.open(format=FORMAT, channels=CHANNELS,
                    rate=RATE, input=True, input_device_index=device_index, frames_per_buffer=CHUNK)

# Initialize socket
# sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))

print("Streaming audio...")
try:
    while True:
        data = stream.read(CHUNK)
        sock.sendto(data, (HOST, PORT))
except KeyboardInterrupt:
    print("Stopping...")
finally:
    stream.stop_stream()
    stream.close()
    audio.terminate()
    sock.close()

