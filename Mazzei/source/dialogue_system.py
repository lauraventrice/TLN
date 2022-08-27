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
        
        print("\n \nProfessor Piton: ", ResponseGenerator.generate_answer(intent))

        """
        while intent != "evaluation_end": 
            response = SpeechRecognizer.read_from_terminal()
            claims, negatives, neutrals, is_correct = self.language_understanding.interpret_response(response)
            memory, intent, ingredient_to_ask = self.dialogue_manager.update_dialogue(response, claims, negatives, neutrals)
            question = ResponseGenerator.generate_answer(memory, intent, ingredient_to_ask, is_correct)
            print("Piton: " + question)  
        """