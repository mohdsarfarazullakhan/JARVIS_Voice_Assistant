import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import os
import smtplib
import pyjokes
import pywhatkit as kit
import cv2
import pyautogui
import time
import sounddevice as sd
import numpy as np
import subprocess

# Initialize text-to-speech engine
engine = pyttsx3.init("sapi5")
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[0].id)  # 0 = male, 1 = female voice

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def wishMe():
    hour = int(datetime.datetime.now().hour)
    if 0 <= hour < 12:
        speak("Good Morning!")
    elif 12 <= hour < 18:
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")
    speak("I am Jarvis sir. Please tell me how may I help you")

# Take command using sounddevice (no PyAudio needed)
def takecommand():
    r = sr.Recognizer()
    fs = 44100  # Sample rate
    duration = 5  # seconds

    print("Listening...")
    speak("Listening...")

    # Record audio
    audio_data = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int16')
    sd.wait()

    # Convert to speech_recognition AudioData
    audio = sr.AudioData(audio_data.tobytes(), fs, 2)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language="en-in")
        print(f"User said: {query}")
    except Exception:
        print("Could not recognize. Please try again...")
        return "None"
    return query.lower()

# Send email function
def sendEmail(to, content):
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.ehlo()
    server.starttls()
    server.login("your_email@gmail.com", "your_password")  # Replace with real creds
    server.sendmail("your_email@gmail.com", to, content)
    server.close()

# Open URL in Chrome if installed, else default browser
def open_in_chrome(url):
    chrome_paths = [
        "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
        "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe",
        os.path.expanduser("~\\AppData\\Local\\Google\\Chrome\\Application\\chrome.exe")
    ]
    for path in chrome_paths:
        if os.path.exists(path):
            subprocess.Popen([path, url])
            return
    webbrowser.open(url)

# Main program
if __name__ == "__main__":
    wishMe()
    while True:
        query = takecommand()

        if query == "none":
            continue

        # Wikipedia
        if "wikipedia" in query:
            speak("Searching Wikipedia...")
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=2)
            speak("According to Wikipedia")
            print(results)
            speak(results)

        # Open YouTube
        elif "open youtube" in query:
            speak("Opening YouTube")
            open_in_chrome("https://www.youtube.com")

        # Open Google
        elif "open google" in query:
            speak("Opening Google")
            open_in_chrome("https://www.google.com")

        # Open StackOverflow
        elif "open stackoverflow" in query:
            speak("Opening Stack Overflow")
            open_in_chrome("https://stackoverflow.com")

        # Open Notepad
        elif "open notepad" in query:
            speak("Opening Notepad")
            os.startfile("C:\\Windows\\System32\\notepad.exe")

        # Open Calculator
        elif "open calculator" in query:
            speak("Opening Calculator")
            os.startfile("C:\\Windows\\System32\\calc.exe")

        # Open Camera
        elif "open camera" in query:
            speak("Opening Camera")
            os.system("start microsoft.windows.camera:")

        # Play music
        elif "play music" in query:
            music_dir = "C:\\Music"  # Replace with your music folder
            if os.path.exists(music_dir):
                songs = os.listdir(music_dir)
                if songs:
                    os.startfile(os.path.join(music_dir, songs[0]))
                else:
                    speak("No music found in your folder")
            else:
                speak("Music folder not found")

        # Time
        elif "the time" in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"Sir, the time is {strTime}")

        # Joke
        elif "tell me a joke" in query:
            joke = pyjokes.get_joke()
            print(joke)
            speak(joke)

        # Quit
        elif "quit" in query or "exit" in query:
            speak("Goodbye sir!")
            break
