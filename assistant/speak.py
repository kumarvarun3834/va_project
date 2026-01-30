import threading
import pyttsx3

# Initialize TTS engine once
tts_engine = pyttsx3.init()
tts_engine.setProperty('rate', 170)   # speaking speed
tts_engine.setProperty('volume', 1)   # max volume

tts_lock = threading.Lock()

def speak(text):
    """Speak text in a separate thread to avoid blocking."""
    def run_speech():
        try:
            tts_engine.say(text)
            tts_engine.runAndWait()
        except Exception as e:
            print(f"[Speak error] {e} | Text: {text}")

    threading.Thread(target=run_speech, daemon=True).start()
