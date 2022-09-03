from dialogue_manager import DialogueManager
from response_generation import ResponseGenerator
from speech_recognition_source import SpeechRecognizer
from language_understanding import LanguageUnderstanding

class DialogueSystem: 

    def __init__(self, dialogue_manager: DialogueManager, language_understanding: LanguageUnderstanding):
        self.dialogue_manager = dialogue_manager
        self.language_understanding = language_understanding
        

    def start_dialogue(self): 

        intent, to_ask = self.dialogue_manager.start_dialogue()
        
        begin = ResponseGenerator.generate_answer(intent)
        print("\n \nProfessor Piton: ", begin, "\n")

        while intent != "evaluation_end": 
            if intent == "handshake" or intent == "ingredients_generic" or to_ask == "question_tricky": 
                ingredient_asked = ""
            else: 
                ingredient_asked = to_ask
            response = SpeechRecognizer.read_from_terminal()
            in_potion, out_potion, y_n, unclear_answer = self.language_understanding.interpret_response(response, intent)
            print("IN POTION: \n \n \n", in_potion, "\n \n \n")
            memory, intent, to_ask, name_potion = self.dialogue_manager.update_dialogue(ingredient_asked, response, in_potion, out_potion, y_n) 
            question = ResponseGenerator.generate_answer(intent, to_ask, memory, unclear_answer, name_potion)

            print("Professor Piton: " + question) 