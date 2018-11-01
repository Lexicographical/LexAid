import pyttsx3
from threading import Thread

def scanVoices():
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    for voice in voices:
        print(voice, voice.id)
        engine.setProperty('voice', voice.id)
        engine.say("The quick brown fox jumps over the lazy dog!")
        engine.runAndWait()
        engine.stop()
# 150 sounds ok
def tryRates():
    engine = pyttsx3.init()
    rate = 50
    while rate <= 300:
        test(rate)
        rate += 50

def test(n):
    engine = pyttsx3.init()
    engine.setProperty("rate", n)
    engine.say("The quick brown fox jumps over the lazy dog.")
    engine.runAndWait()

Thread(target=test, args=(150,)).start()