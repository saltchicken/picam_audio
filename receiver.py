import pyaudio
import zmq
import opuslib
import numpy as np

# Set up ZeroMQ context and subscriber socket (server side)
context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.bind("tcp://*:50003")  # Server binds to port 5555 to listen for clients
socket.setsockopt_string(zmq.SUBSCRIBE, "")  # Subscribe to all messages

# Set up PyAudio for audio playback (server side)
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16,
                channels=1,
                rate=32000,
                output=True,
                frames_per_buffer=1024)

# Set up Opus decoder (server side)
frame_size = 960  # 20ms at 48 kHz for stereo, 960 samples per frame
decoder = opuslib.Decoder(32000, 1)  # 48000 Hz sample rate, mono

while True:
    # Receive compressed Opus data from the client
    opus_data = socket.recv()

    # Decode with Opus
    decoded_data = decoder.decode(opus_data, frame_size, decode_fec=False)

    # Convert decoded data back to numpy array for playback
    pcm_data = np.frombuffer(decoded_data, dtype=np.int16)

    # Play the decoded PCM audio
    stream.write(pcm_data.tobytes())

