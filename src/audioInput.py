import speech_recognition as sr

r = sr.Recognizer()

def interpret_speech(lan="en-US"):
    
    with sr.Microphone() as source:
        print("Recording...")

        audio_data = r.record(source, duration=5)

        print("Recognizing...")

        text = r.recognize_google(audio_data, lan)

        print(text)

