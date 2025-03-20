import os
import google.generativeai as genai
from dotenv import load_dotenv
import time
import speech_recognition as sr
import pyttsx3
import numpy as np
from gtts import gTTS

mytext = 'Welcome to me'
language = 'en'

genai.configure(api_key = "")
model = genai.GenerativeModel('gemini-2.0-flash-exp',
    generation_config=genai.GenerationConfig(
        candidate_count=1,
        top_p = 0.95,
        top_k = 40,
        max_output_tokens=256, # 100 tokens correspond to roughly 60-80 words.
        temperature = 0.9,
    ))

load_dotenv()

# Set up the speech recognition and text-to-speech engines
r = sr.Recognizer()
engine = pyttsx3.init()

name = "Paul"
greetings = [f"whats up master {name}",
             "yeah?",
             "Well, hello there, Master of Puns and Jokes - how's it going today?",
             f"Ahoy there, Captain {name}! How's the ship sailing?",
             #f"Bonjour, Monsieur {name}! Comment ça va? Wait, why the hell am I speaking French?",
             "Hows about ye?",
             f"Whats the crack {name}?"
             ]

chat = model.start_chat(history=[])

def listen_for_wake_word(source):
    print("Listening for 'Hey'...")

    while True:
        audio = r.listen(source)
        try:
            text = r.recognize_google(audio)
            if "bingo" in text.lower():
                print("Wake word detected.")
                engine.say(np.random.choice(greetings))
                engine.runAndWait()
                listen_and_respond(source)
                break
        except sr.UnknownValueError:
            pass
# Listen for input and respond with OpenAI API
def listen_and_respond(source):
    print("Listening...")
    while True:
        audio = r.listen(source)
        try:
            text = r.recognize_google(audio)
            print(f"You said: {text}")
            if not text:
                continue

            response = chat.send_message(f"{text}")
            responseText = response.text.replace('*', '').replace('"', '')
            print(responseText)
            print("generating audio")
            myobj = gTTS(text = responseText, lang = language, slow = False)
            myobj.save("response.mp3")
            print("speaking")
            os.system("vlc response.mp3")
            # Speak the response
            print("speaking")
            engine.say(responseText)
            engine.runAndWait()
            if not audio:
                listen_for_wake_word(source)
        except sr.UnknownValueError:
            time.sleep(2)
            print("Silence found, shutting up, listening...")
            listen_for_wake_word(source)
            break
        except sr.RequestError as e:
            print(f"Could not request results; {e}")
            engine.say(f"Could not request results; {e}")
            engine.runAndWait()
            listen_for_wake_word(source)
            break

# Use the default microphone as the audio source
with sr.Microphone() as source:
    listen_for_wake_word(source)
