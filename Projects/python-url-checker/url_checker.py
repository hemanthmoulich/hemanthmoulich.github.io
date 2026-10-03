import tkinter as tk
import threading
import sounddevice as sd
import numpy as np
import whisper
import queue
import tempfile
import soundfile as sf
import pyperclip
import webbrowser
import os

# Load Whisper model
model = whisper.load_model("small")

# Globals
recording = False
audio_chunks = []
q = queue.Queue()

SAMPLE_RATE = 16000
CHANNELS = 1
BLOCK_DURATION = 5  # seconds per chunk

def audio_callback(indata, frames, time, status):
    if recording:
        q.put(indata.copy())

def record_audio():
    global recording, audio_chunks
    print("🎙️ Recording started...")
    audio_chunks = []
    while recording:
        frames = []
        for _ in range(int(BLOCK_DURATION * SAMPLE_RATE / 1024)):
            if not recording:
                break
            try:
                frames.append(q.get(timeout=1))
            except queue.Empty:
                continue
        if frames:
            audio_chunks.append(np.concatenate(frames, axis=0))

def stop_and_process():
    global recording
    recording = False
    print("🛑 Recording stopped. Processing...")

    if not audio_chunks:
        print("No audio recorded.")
        return

    # Combine all chunks
    full_audio = np.concatenate(audio_chunks, axis=0)

    # Save to temporary WAV
    temp_wav = os.path.join(tempfile.gettempdir(), "meeting_audio.wav")
    sf.write(temp_wav, full_audio, SAMPLE_RATE)

    # Transcribe
    result = model.transcribe(temp_wav)
    text = result["text"].strip()
    print("🗣️ Transcribed Text:")
    print(text)

    # Copy to clipboard
    pyperclip.copy(text)

    # Open ChatGPT in default browser
    webbrowser.open("https://chat.openai.com/chat")
    print("✅ Text copied to clipboard. Paste it in ChatGPT search bar.")

    # Cleanup
    os.remove(temp_wav)

# GUI callbacks
def start_button_clicked():
    global recording
    if recording:
        return
    recording = True
    threading.Thread(target=record_audio, daemon=True).start()
    start_btn.config(state="disabled")
    stop_btn.config(state="normal")

def stop_button_clicked():
    stop_btn.config(state="disabled")
    start_btn.config(state="normal")
    threading.Thread(target=stop_and_process, daemon=True).start()

# GUI setup
root = tk.Tk()
root.title("System Audio to ChatGPT")
root.geometry("400x200")

tk.Label(root, text="🎧 System Audio → ChatGPT", font=("Arial", 16, "bold")).pack(pady=15)

start_btn = tk.Button(root, text="Start Recording 🎙️", width=25, bg="green", fg="white", font=("Arial", 12, "bold"), command=start_button_clicked)
start_btn.pack(pady=10)

stop_btn = tk.Button(root, text="Stop & Send ⏹️", width=25, bg="red", fg="white", font=("Arial", 12, "bold"), command=stop_button_clicked, state="disabled")
stop_btn.pack(pady=10)

# Start audio stream
stream = sd.InputStream(samplerate=SAMPLE_RATE, channels=CHANNELS, callback=audio_callback)
stream.start()

root.mainloop()
