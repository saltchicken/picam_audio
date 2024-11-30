import pyaudio

# Initialize PyAudio
audio = pyaudio.PyAudio()

# Get the number of available devices
device_count = audio.get_device_count()

print("Available audio devices:")
for i in range(device_count):
    # Get device info by index
    device_info = audio.get_device_info_by_index(i)
    print(f"Device Index {i}: {device_info['name']}")

# Terminate PyAudio
audio.terminate()

