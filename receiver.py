import pyaudio
import zmq
from pydub import AudioSegment
from io import BytesIO

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

while True:
    # Receive compressed MP3 data from the client
    mp3_data = socket.recv()

    # Decode MP3 data with pydub
    audio = AudioSegment.from_mp3(BytesIO(mp3_data))

    # Convert the audio to raw PCM data
    pcm_data = audio.set_frame_rate(32000).set_channels(1).set_sample_width(2).raw_data

    # Play the decoded PCM audio
    stream.write(pcm_data)

