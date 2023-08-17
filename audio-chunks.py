import pyaudio
import wave

# Parameters for audio capture
CHUNK_SIZE = 1024  # Number of audio frames per buffer
FORMAT = pyaudio.paInt16  # Audio format (16-bit signed integer)
CHANNELS = 1  # Number of audio channels (1 for mono, 2 for stereo)
SAMPLE_RATE = 44100  # Sample rate in Hz
RECORD_SECONDS = 5  # Duration in seconds

# Initialize PyAudio
p = pyaudio.PyAudio()

# Open microphone stream
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=SAMPLE_RATE,
                input=True,
                frames_per_buffer=CHUNK_SIZE)

print("Recording...")

audio_frames = []

# Capture audio frames
for _ in range(int(SAMPLE_RATE / CHUNK_SIZE * RECORD_SECONDS)):
    audio_data = stream.read(CHUNK_SIZE)
    audio_frames.append(audio_data)

print("Recording finished.")

# Close the stream and terminate PyAudio
stream.stop_stream()
stream.close()
p.terminate()

# Save the recorded audio to a WAV file
with wave.open("recorded_audio.wav", "wb") as wf:
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(SAMPLE_RATE)
    wf.writeframes(b''.join(audio_frames))
