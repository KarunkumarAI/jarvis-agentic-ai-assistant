import pyttsx3    #uses the speech voices installed on Windows and works offline


def speak(text: str) -> None:
    engine = pyttsx3.init()
    engine.setProperty("rate", 175)

    engine.say(text)
    engine.runAndWait()   #speaks it.