#Lettura frasi da terminale
#Interpretazione frasi con uso della libreria SpeechRecognition

"""
pip install SpeechRecognition
pip install pyttsx3
pip install pyaudio
"""

import speech_recognition as sr
import pyttsx3
from sys import platform

class SpeechRecognizer: 

    @classmethod
    def read_from_terminal(cls):
        """read from terminal"""
        
        return input("Student: ")

    @classmethod
    def response_interpretation(cls):
        #qui uso di speech recognition NEL FUTURO!
        # Initialize the recognizer
        r = sr.Recognizer()
        # use the microphone as source for input.
        with sr.Microphone() as source2:
            # wait for a second to let the recognizer
            # adjust the energy threshold based on
            # the surrounding noise level
            r.adjust_for_ambient_noise(source2,duration=0.2)
            print("Student: ")
            #Listens for the user's input
            audio2 = r.listen(source2)


            try:
                dest = r.recognize_google(audio2)
                print ("You have said : " + dest)

            except Exception:
                print("Sorry, I didn't hear you.")

            # # Using ggogle to recognize audio
            # MyText = r.recognize_google(audio2)
            # MyText = MyText.lower()
            # print ("Did you say: " + MyText)

            #SpeechRecognizer.SpeakText("Hello mr Potter! Are you ready for the exam?")



if __name__ == "__main__":
    SpeechRecognizer.response_interpretation()