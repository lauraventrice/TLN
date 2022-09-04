#Lettura frasi da terminale
#Interpretazione frasi con uso della libreria SpeechRecognition

"""
pip install SpeechRecognition
pip install pyttsx3
pip install pyaudio
"""

#import SpeechRecognition as sr
import speech_recognition as sr
import pyttsx3
from sys import platform

class SpeechRecognizer: 

    @classmethod
    def read_from_terminal(cls):
        """read from terminal"""
        
        return input("Student: ")

    @classmethod
    def response_interpretation(cls, response: str):
        #qui uso di speech recognition NEL FUTURO!
        pass

    @classmethod
    def test(cls):
        #qui uso di speech recognition NEL FUTURO!
        # Initialize the recognizer
        r = sr.Recognizer()
        # use the microphone as source for input.
        with sr.Microphone() as source2:
            # wait for a second to let the recognizer
            # adjust the energy threshold based on
            # the surrounding noise level
            r.adjust_for_ambient_noise(source2,duration=0.2)
            print("PARLA ORA")
            #Listens for the user's input
            audio2 = r.listen(source2)
            # Using ggogle to recognize audio
            MyText = r.recognize_google(audio2)
            MyText = MyText.lower()
            print ("Did you say: " + MyText)
            SpeechRecognizer.SpeakText("Hello mr Potter! Are you ready for the exam?")

    # Function to convert text to
    # speech
    @classmethod
    def SpeakText (cls, command) :

        if platform == "darwin":
            # OS X
            voice_id = "com.apple.speech.synthesis.voice.Alex"
        elif platform == "win32":
            # Windows...
            voice_id = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_DAVID_11.0"
        # Initialize the engine
        engine = pyttsx3.init()

        voices = engine.getProperty('voices')
  
        for voice in voices:
        #    to get the info. about various voices in our PC 
            print("Voice:")
            print("ID: %s" %voice.id)
            print("Name: %s" %voice.name)
            print("Age: %s" %voice.age)
            print("Gender: %s" %voice.gender)
            print("Languages Known: %s" %voice.languages)

        # Use female voice
        engine.setProperty('voice', voice_id)

        engine.say(command)
        engine.runAndWait()

if __name__ == "__main__":
    SpeechRecognizer.test()