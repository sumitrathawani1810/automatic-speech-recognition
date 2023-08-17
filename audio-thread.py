import sounddevice as sd
import queue
import threading
import soundfile as sf
import whisper

model = whisper.load_model("medium")
# Initialize variables
audio_queue = queue.Queue()
sample_rate = 44100  # Adjust as needed
channels = 1

# Callback function for audio streaming


def audio_callback(indata, frames, time, status):
    if status:
        print(status)
    audio_queue.put(indata.copy())


# Start audio streaming in a separate thread
def audio_stream_thread():
    with sd.InputStream(callback=audio_callback,
                        channels=channels,
                        samplerate=sample_rate,
                        blocksize=int(44100*2)):
        print("Audio streaming thread started.")
        # Sleep indefinitely, recording in the background
        sd.sleep(-1)


# Start the audio streaming thread
stream_thread = threading.Thread(target=audio_stream_thread)
stream_thread.start()


i = 0
# Main program loop
try:
    while True:
        # Process audio chunks from the queue
        while not audio_queue.empty():
            audio_chunk = audio_queue.get()
            chunk_filename = f"chunk.wav"
            sf.write(chunk_filename, audio_chunk, 44100)
            response = model.transcribe(chunk_filename)
            print(response['text'])
            # Perform processing on the audio chunk as needed
            # For example, send it for transcription or other analysis


except KeyboardInterrupt:
    print("Recording stopped.")
    # Clean up after recording
    stream_thread.join()  # Wait for the audio streaming thread to finish