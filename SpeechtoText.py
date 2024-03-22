import speech_recognition as sr

# speech recognition through mic
def speech_to_text():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)
        try:
            text = r.recognize_google(audio)
            print("You said: ", text)
            return text
        except:
            print("Sorry, could not recognize your voice.")
            return ""

speech_to_text()