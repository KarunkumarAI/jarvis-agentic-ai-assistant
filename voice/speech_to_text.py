import io

import speech_recognition as sr


def transcribe_audio(audio_bytes: bytes) -> str:
    recognizer = sr.Recognizer()

    with sr.AudioFile(io.BytesIO(audio_bytes)) as source:  # reads the audio
        audio = recognizer.record(source)

    return recognizer.recognize_google(audio) #converts speech to text