#Lettura frasi da terminale
#Interpretazione frasi con uso della libreria SpeechRecognition

#import SpeechRecognition as sr

class SpeechRecognizer: 

    @classmethod
    def read_from_terminal(cls):
        """read from terminal"""
        
        return input("Student: ")

    def response_interpretation(cls, response: str):
        #qui uso di speech recognition NEL FUTURO!
        pass