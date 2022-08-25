#Lettura frasi da terminale
#Interpretazione frasi con uso della libreria SpeechRecognition

#import SpeechRecognition as sr

class SpeechRecognizer: 

    def read_from_terminal(self):
        return input("Student: ")

    def response_interpretation(self, response: str):
        #qui uso di speech recognition
        pass