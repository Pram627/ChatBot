import speech_recognition as sr
from gtts import gTTS
import transformers
import time
import os
import datetime
import numpy as np

class ChatBot():
    def __init__(self, name):
        print("----- Starting up", name, "-----")
        self.name = name

    def speech_to_text(self):
        recognizer = sr.Recognizer()
        with sr.Microphone() as mic:
            print("Listening...")
            audio = recognizer.listen(mic)
            self.text ="ERROR"
        try:
            self.text = recognizer.recognize_google(audio)
            print("Me  --> ", self.text)
        except:
            print("Me  -->  ERROR")

    @staticmethod
    def text_to_speech(text):
        print("Dev --> ", text)
        speaker = gTTS(text=text, lang="en", slow=False)

        speaker.save("res.mp3")
        statbuf = os.stat("res.mp3")
        mbytes = statbuf.st_size / 1024
        duration = mbytes / 200
        os.system('start res.mp3')
        os.system("close res.mp3")
        time.sleep(int(5.0*duration))
        os.remove("res.mp4")

    def wake_up(self, text):
        return True if self.name in text.lower() else False

    @staticmethod
    def action_time():
        return datetime.datetime.now().time().strftime('%H:%M')


if __name__ == "__main__":

    ai = ChatBot(name="Dev")
    nlp = transformers.pipeline("conversational", model="microsoft/DialoGPT-medium")
    os.environ["TOKENIZERS_PARALLELISM"] = "true"

    ex = True
    while ex:
        ai.speech_to_text()

        if ai.wake_up(ai.text) is True:
            res = "Hello I am Dev the AI, what can I do for you?"

        elif "time" in ai.text:
            res = ai.action_time()

        elif any(i in ai.text for i in ["thank you", "thanks"]):
            res = np.random.choice
                (["You're welcome!", "Anytime!", "np", "cool cool cool", "I'm here if you need me!", "sure dude"])

        elif any(i in ai.text for i in ["exit", "close"]):
            res = np.random.choice(["Sayonara", "Have a good day", "Byeee", "Goodbye", "Hope to help", "Dev out!"])

            ex = False
      
        else:
            if ai.text =="ERROR":
                res = "Sorry, come again?"
            else:
                chat = nlp(transformers.Conversation(ai.text), pad_token_id=0)
                res = str(chat)
                res = res[res.find("bot >> ") + 6:].strip()

        ai.text_to_speech(res)
    print("----- Closing down Dev -----")
