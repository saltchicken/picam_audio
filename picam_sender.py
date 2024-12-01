import socket
import pyaudio

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024

p = pyaudio.PyAudio()
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)
_ = input_stream.read(CHUNK, exception_on_overflow=False)

# Set up TCP connection
HOST = '10.0.0.3'  # Server IP address
PORT = 50002
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

# Set up PyAudio for recording

try:
    while True:
        try:
            data = stream.read(CHUNK)
        except:
            continue
        client_socket.sendall(data)  # Send audio data over TCP
except:
    print("Something bad happened")

finally:
    client_socket.close()
    stream.stop_stream()
    stream.close()
    p.terminate()

