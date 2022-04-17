import speech_recognition as sr
import sys

# filename = sys.argv[1]

# initialize the recognizer
r = sr.Recognizer()

# open the file
with sr.Microphone() as source:
    # listen for the data (load audio to memory)
    r.adjust_for_ambient_noise(source)
    print("say...")
    audio_data = r.listen(source)
    try:
        # recognize (convert from speech to text)
        text = r.recognize_google(audio_data)
        print(text)
    except:
        print("srry")
