import pyaudio
import zmq
from pydub import AudioSegment
from io import BytesIO
import numpy as np

# Set up ZeroMQ context and publisher socket (client side)
context = zmq.Context()
socket = context.socket(zmq.PUSH)  # Client will push data to the server
socket.connect("tcp://10.0.0.3:50003")  # Connect to the server at port 5555

# Set up PyAudio for audio capture (client side)
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16,
                channels=1,
                rate=32000,
                input=True,
                frames_per_buffer=1024)

while True:
    # Read raw PCM data from microphone
    audio_data = stream.read(1024)

    # Convert PCM data to AudioSegment for MP3 encoding
    audio = AudioSegment(
        data=audio_data,
        sample_width=2,
        frame_rate=32000,
        channels=1
    )

    # Encode the audio to MP3 in memory
    mp3_data = BytesIO()
    audio.export(mp3_data, format="mp3")

    # Send the MP3 data to the server
    socket.send(mp3_data.getvalue())

