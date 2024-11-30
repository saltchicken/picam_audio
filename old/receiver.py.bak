import socket
import pyaudio

# Set up audio playback parameters
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 32000
CHUNK = int(1024 / 4)

# Set up TCP connection
HOST = '0.0.0.0'  # Listen on all available interfaces
PORT = 50002
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(1)

print(f"Server listening on {HOST}:{PORT}...")

# Wait for a client to connect
client_socket, client_address = server_socket.accept()
print(f"Connection from {client_address}")

# Set up PyAudio for playback
p = pyaudio.PyAudio()
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                output=True,
                frames_per_buffer=CHUNK)

try:
    while True:
        data = client_socket.recv(CHUNK)
        if not data:
            break
        stream.write(data)  # Play the received audio data
finally:
    client_socket.close()
    server_socket.close()
    stream.stop_stream()
    stream.close()
    p.terminate()

