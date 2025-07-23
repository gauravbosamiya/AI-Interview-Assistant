import speech_recognition as sr

def transcribe_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        audio = recognizer.listen(source, phrase_time_limit=10)
    try:
        return recognizer.recognize_google(audio)
    except Exception:
        return None