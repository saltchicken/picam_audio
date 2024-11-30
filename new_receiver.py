import numpy as np
import pyaudio
import socket

# Define constants for audio
CHUNK = 1024  # Number of frames per buffer
FORMAT = pyaudio.paInt16  # Audio format (16-bit signed integers)
CHANNELS = 1  # Mono audio
RATE = 32000  # Sample rate (44.1 kHz)

# Set up UDP server socket
UDP_IP = "0.0.0.0"  # IP address of the receiver
UDP_PORT = 5005  # Port to receive audio
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

# Initialize PyAudio for playback
p = pyaudio.PyAudio()

# Open output audio stream (for playback)
output_stream = p.open(format=FORMAT,
                       channels=CHANNELS,
                       rate=RATE,
                       output=True,
                       frames_per_buffer=CHUNK)

print("Receiving and playing audio...")

try:
    while True:
        # Receive audio data from the sender
        data, addr = sock.recvfrom(CHUNK * 2)  # 2 bytes per sample for int16 format
        
        # Convert received bytes to numpy array
        audio_data = np.frombuffer(data, dtype=np.int16)

        # Play the received audio data
        output_stream.write(audio_data.tobytes())

except KeyboardInterrupt:
    print("Audio streaming stopped.")

finally:
    # Stop the stream and clean up
    output_stream.stop_stream()
    output_stream.close()
    p.terminate()
    sock.close()

