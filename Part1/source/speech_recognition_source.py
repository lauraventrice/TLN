import speech_recognition as sr

class SpeechRecognizer: 

    @classmethod
    def read_from_terminal(cls):
        """read from terminal"""
        
        return input("Student: ")

    @classmethod
    def vocal_response(cls):
        # Initialize the recognizer
        r = sr.Recognizer()
        # use the microphone as source for input.
        response = ""

        with sr.Microphone() as source:
            while response == "":
                # wait for a second to let the recognizer
                # adjust the energy threshold based on
                # the surrounding noise level
                r.adjust_for_ambient_noise(source,duration=0.2)
                print("\nStudent: ")
                #Listens for the user's input
                audio = r.listen(source)

                try:
                    response = r.recognize_google(audio)
                    print ("\nYou have said : " + response)

                except Exception:
                    print("\nSorry, I didn't hear you.")
        
        return response
