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
            #SpeechRecognizer.SpeakText(MyText)

    # Function to convert text to
    # speech
    @classmethod
    def SpeakText (cls, command) :
        # Initialize the engine
        engine = pyttsx3.init()
        engine.say(command)
        engine.runAndwait()

if __name__ == "__main__":
    SpeechRecognizer.test()