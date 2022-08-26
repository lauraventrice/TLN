from .dialogue_manager import DialogueManager
from .response_generation import ResponseGeneration
from .speech_recognition import SpeechRecognizer
from .language_understanding import LanguageUnderstanding

class DialogueSystem: 

    def __init__(self, dialogue_manager: DialogueManager, language_understanding: LanguageUnderstanding, 
        response_generation: ResponseGeneration, speech_recognizer: SpeechRecognizer):
        
        self.dialogue_manager = dialogue_manager
        self.language_understanding = language_understanding
        self.response_generation = response_generation
        self.speech_recognizer = speech_recognizer
        

    def start_dialogue(self): 

        memory, intent = self.dialogue_manager.start_dialogue()
        self.response_generation.generate_answer(memory, intent)

        while intent != "evaluation_end": 
            response = self.speech_recognizer.read_from_terminal()
            claims, negatives, neutrals, is_correct = self.language_understanding.interpret_response(response)
            memory, intent = self.dialogue_manager.update_dialogue(response, claims, negatives, neutrals)
            question = self.response_generation.generate_answer(memory, intent, is_correct)
            print("Piton: " + question)  