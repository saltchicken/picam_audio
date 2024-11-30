import pyaudio
import numpy as np
from vidgear.gears import AudioStream
import socket

# Define constants for audio
CHUNK = 1024  # Number of frames per buffer
FORMAT = pyaudio.paInt16  # Audio format (16-bit signed integers)
CHANNELS = 1  # Mono audio
RATE = 32000  # Sample rate (44.1 kHz)

# Set up UDP client socket
UDP_IP = "10.0.0.3"  # IP address of the receiver
UDP_PORT = 5005  # Port to stream to
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Initialize PyAudio for capturing audio
p = pyaudio.PyAudio()
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

# Initialize VidGear AudioStream object
audio_stream = AudioStream()

print("Recording and streaming audio...")

try:
    while True:
        # Capture audio from microphone
        data = stream.read(CHUNK)
        
        # Convert audio data to numpy array (optional)
        audio_data = np.frombuffer(data, dtype=np.int16)

        # Send the audio data over UDP
        sock.sendto(audio_data.tobytes(), (UDP_IP, UDP_PORT))

except KeyboardInterrupt:
    print("Audio streaming stopped.")

finally:
    # Stop the stream and clean up
    stream.stop_stream()
    stream.close()
    p.terminate()
    sock.close()

