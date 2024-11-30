import socket
import pyaudio

# Set up audio capture parameters
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 32000
CHUNK = 1024

# Set up TCP connection
HOST = '10.0.0.3'  # Server IP address
PORT = 50002
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

# Set up PyAudio for recording
p = pyaudio.PyAudio()
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

try:
    while True:
        data = stream.read(CHUNK)
        client_socket.sendall(data)  # Send audio data over TCP
finally:
    client_socket.close()
    stream.stop_stream()
    stream.close()
    p.terminate()

