# sfrutta la memoria per diversi output possibili: 
# - saluti
# - inizio esame
# - risposta giusta e continuo
# - risposta sbagliata e continuo
# - input incomprensibile e chiede di ripetere
# - fine esame e valutazione

# Uso di simpleNLG per generare risposte

# Usiamo pyttsx3 per generare audio????? o alternative!!!!!!!!!!

import pandas 
import random 

class ResponseGenerator: 

    CONTEXT_ANSWERS = ["greetings", "init_exam", "feedback_continue", "unclear_input", "end_exam_eval", "restart"]

    @classmethod
    def generate_answer(cls, current_intent: str, to_ask = "", memory = None, unclear_answer = False): 
        """Generates an answer for the current intent based on memory.
        
        Args:
            memory (pandas.DataFrame): The memory of the system.
            current_intent (str): The current intent of the system.
            unclear_answer (bool, optional): Whether the answer is unclear. Defaults to False. Based on language_understanding module.
        """

        if unclear_answer: 
            return cls.generate_unclear_answer()
        elif current_intent == "handshake":
            return cls.generate_greetings()
        elif current_intent == "ingredients_generic":
            return cls.generate_init_exam(to_ask)
        elif current_intent == "ingredients_yes_no" or current_intent == "question_tricky":
            return cls.generate_feedback_continue()
        elif current_intent == "evaluation":
            return cls.generate_end_exam_eval()
        elif current_intent == "restart":
            return cls.generate_restart(to_ask)
        else:
            return "I don't know what to say."

    @classmethod
    def generate_greetings(cls): #rispondiamo a partire da una lista di possibili risposte
        
        possible_sentences = ["Good morning Mr Potter.", "Welcome to the potions examination Mr Potter."]
        choose_sentence = list(random.sample(range(0, len(possible_sentences)), 1))
             
        return possible_sentences[choose_sentence[0]]

    @classmethod
    def generate_init_exam(cls, to_ask: str): #rispondiamo a partire da una lista di possibili risposte
        
        possible_sentences = ["Mr. Potter tell me the ingredients of the potion " + to_ask + ".", \
             "Mr. Potter can you tell me the ingredients of the potion " + to_ask + "?",   \
                "Mr. Potter could you tell me the ingredients of the potion" + to_ask + "?"]
        
        choose_sentence = list(random.sample(range(0, len(possible_sentences)), 1))
             
        return possible_sentences[choose_sentence[0]]
    
    @classmethod
    def generate_feedback_continue(cls): #usiamo simpleNLG per generare risposte 
        #bisogna stare attenti agli ingredienti delle risposte dell'utente e quelli richiesti dal sistema per evitare ripetizioni
        pass
    
    @classmethod
    def generate_end_exam_eval(cls): #rispondiamo a partire da una lista di possibili risposte
        pass
    
    @classmethod
    def generate_restart(cls, to_ask: str): #rispondiamo a partire da una lista di possibili risposte
        pass    


    # forse alla fine di questa fase ci conviene restituire sia la domanda da stampare che la domanda attesa??