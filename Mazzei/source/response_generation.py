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

class ResponseGenerator: 

    CONTEXT_ANSWERS = ["greetings", "init_exam", "feedback_continue", "unclear_input", "end_exam_eval", "restart"]

    def generate_answer(cls, memory: pandas.DataFrame, current_intent: str, unclear_answer = False): 
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
            return cls.generate_init_exam()
        elif current_intent == "ingredients_yes_no" or current_intent == "question_tricky":
            return cls.generate_feedback_continue()
        elif current_intent == "evaluation":
            return cls.generate_end_exam_eval()
        elif current_intent == "restart":
            return cls.generate_restart()
        else:
            return "I don't know what to say."

    def generate_greetings(cls): #rispondiamo a partire da una lista di possibili risposte
        pass 

    def generate_init_exam(cls): #rispondiamo a partire da una lista di possibili risposte
        pass
    
    def generate_feedback_continue(cls): #usiamo simpleNLG per generare risposte 
        #bisogna stare attenti agli ingredienti delle risposte dell'utente e quelli richiesti dal sistema per evitare ripetizioni
        pass
    
    def generate_end_exam_eval(cls): #rispondiamo a partire da una lista di possibili risposte
        pass

    def generate_restart(cls): #rispondiamo a partire da una lista di possibili risposte
        pass    


    # forse alla fine di questa fase ci conviene restituire sia la domanda da stampare che la domanda attesa??