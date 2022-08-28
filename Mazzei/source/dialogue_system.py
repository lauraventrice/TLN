from dialogue_manager import DialogueManager
from response_generation import ResponseGenerator
from speech_recognition import SpeechRecognizer
from language_understanding import LanguageUnderstanding

class DialogueSystem: 

    def __init__(self, dialogue_manager: DialogueManager, language_understanding: LanguageUnderstanding):
        self.dialogue_manager = dialogue_manager
        self.language_understanding = language_understanding
        

    def start_dialogue(self): 

        intent = self.dialogue_manager.start_dialogue()
        
        begin = ResponseGenerator.generate_answer(intent)
        print("\n \nProfessor Piton: ", begin, "\n")

        expected = "greetings"

        while intent != "evaluation_end": 
            response = SpeechRecognizer.read_from_terminal()
            in_potion, not_in_potion, y_n, unclear_answer = self.language_understanding.interpret_response(response)
            memory, intent, to_ask = self.dialogue_manager.update_dialogue(response, in_potion, not_in_potion, y_n)
            question = ResponseGenerator.generate_answer(intent, to_ask, memory, unclear_answer)
            print("Professor Piton: " + question) 
            
            intent = "evaluation_end"
        