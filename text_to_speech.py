from gtts import gTTS
from io import BytesIO
import pygame
import os

# Initialize Pygame mixer
pygame.mixer.init()

def text_to_speech(text):
    pygame.mixer.init()
    # Create a temporary file to save the speech
    tmp_file = 'temp_audio.mp3'
    tts = gTTS(text=text, lang='en')
    cnt = 0
    while os.path.exists(tmp_file):
        tmp_file = tmp_file.split('.')
        tmp_file[0] += str(cnt) + "."
        tmp_file = "".join(tmp_file)
        cnt += 1
    tts.save(tmp_file)
    pygame.mixer.music.load(tmp_file)
    pygame.mixer.music.play()