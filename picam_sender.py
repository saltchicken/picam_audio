import pyaudio
import zmq
import opuslib
import numpy as np

# Set up ZeroMQ context and publisher socket (client side)
context = zmq.Context()
socket = context.socket(zmq.PUSH)  # Client will push data to the server
socket.connect("tcp://10.0.0.3:5003")  # Connect to the server at port 5555

# Set up PyAudio for audio capture (client side)
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16,
                channels=1,
                rate=32000,
                input=True,
                frames_per_buffer=1024)

# Set up Opus encoder (client side)
frame_size = 960  # 20ms at 48 kHz for stereo, 960 samples per frame
encoder = opuslib.Encoder(32000, 1, opuslib.APPLICATION_AUDIO)  # 48000 Hz sample rate, mono

while True:
    # Read raw PCM data from microphone
    audio_data = stream.read(1024)

    # Convert to numpy array for easier handling
    pcm_data = np.frombuffer(audio_data, dtype=np.int16)

    # Encode with Opus
    opus_data = encoder.encode(pcm_data.tobytes(), frame_size)

    # Send compressed Opus data to the server
    socket.send(opus_data)

