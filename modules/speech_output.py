from gtts import gTTS
import pygame
import tempfile
import os

def speak_text(text):
    try:
        tts = gTTS(text)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
            tts.save(fp.name)
            try:
                pygame.mixer.init()
                pygame.mixer.music.load(fp.name)
                pygame.mixer.music.play()
                while pygame.mixer.music.get_busy():
                    pygame.time.Clock().tick(10)
            except pygame.error as audio_err:
                print(f"🔊 Voice error: {audio_err}")
    except Exception as e:
        print(f"🔊 TTS error: {e}")
    finally:
        try:
            os.remove(fp.name)
        except Exception:
            pass