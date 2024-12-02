import socket
import pyaudio



print("picam_audio started", flush=True)

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024


# Set up TCP connection
HOST = '10.0.0.3'  # Server IP address
PORT = 50002
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))




# Set up PyAudio for recording
p = pyaudio.PyAudio()

device_index = 0
device_count = p.get_device_count()
found = False

print("Available audio devices:", flush=True)
for i in range(device_count):
    # Get device info by index
    device_info = p.get_device_info_by_index(i)
    print(f"Device Index {i}: {device_info['name']}", flush=True)
    if "pulse" in device_info['name'].lower():
        found = True
        print("Pulse found", flush=True)
        device_index = i

if not found:
    print("Pulse was not found. Exitting...", flush=True)
    sys.exit(1)

print(f"Using device index {device_index}", flush=True)

stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK,
                input_device_index=device_index)
_ = stream.read(CHUNK, exception_on_overflow=False)

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

