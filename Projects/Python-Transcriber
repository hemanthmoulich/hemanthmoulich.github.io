
import pyaudio, wave, time, pyperclip, speech_recognition as sr

# === SETTINGS ===
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
SECONDS = 5           # record chunk length
TEMP_FILE = "temp.wav"

# === INIT AUDIO ===
p = pyaudio.PyAudio()
stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE,
                input=True, frames_per_buffer=CHUNK)
r = sr.Recognizer()

print("Listening from Stereo Mix... (Ctrl+C to stop)\n")

try:
    while True:
        # record short chunk
        frames = [stream.read(CHUNK) for _ in range(int(RATE / CHUNK * SECONDS))]

        # write to wav
        with wave.open(TEMP_FILE, "wb") as wf:
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(p.get_sample_size(FORMAT))
            wf.setframerate(RATE)
            wf.writeframes(b"".join(frames))

        # speech recognition
        with sr.AudioFile(TEMP_FILE) as src:
            audio = r.record(src)
            try:
                text = r.recognize_google(audio)
                if text.strip():
                    pyperclip.copy(text)
                    print("Copied:", text)
            except sr.UnknownValueError:
                pass
            except sr.RequestError as e:
                print("Network error:", e)

except KeyboardInterrupt:
    print("\nStopped.")
finally:
    stream.stop_stream()
    stream.close()
    p.terminate()
