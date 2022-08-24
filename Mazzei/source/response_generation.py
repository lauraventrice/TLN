# sfrutta la memoria per diversi output possibili: 
# - saluti
# - inizio esame
# - risposta giusta e continuo
# - risposta sbagliata e continuo
# - input incomprensibile e chiede di ripetere
# - fine esame e valutazione

# Uso di simpleNLG per generare risposte

# Usiamo pyttsx3 per generare audio????? o alternative!!!!!!!!!!

class ResponseGeneration: 

    CONTEXT_ANSWERS = ["greetings", "init_exam", "feedback_continue", "unclear_input", "end_exam_eval", "restart"]

    def generate_answer(self, memory, current_intent: str, unclear_answer = False): 
        """Generates an answer for the current intent based on memory.
        
        Args:
            memory (pandas.DataFrame): The memory of the system.
            current_intent (str): The current intent of the system.
            unclear_answer (bool, optional): Whether the answer is unclear. Defaults to False. Based on language_understanding module.
        """

        if unclear_answer: 
            return self.generate_unclear_answer()
        elif current_intent == "handshake":
            return self.generate_greetings()
        elif current_intent == "ingredients_generic":
            return self.generate_init_exam()
        elif current_intent == "ingredients_yes_no" or current_intent == "question_tricky":
            return self.generate_feedback_continue()
        elif current_intent == "evaluation":
            return self.generate_end_exam_eval()
        elif current_intent == "restart":
            return self.generate_restart()
        else:
            return "I don't know what to say."

    def generate_greetings(self): #rispondiamo a partire da una lista di possibili risposte
        pass 

    def generate_init_exam(self): #rispondiamo a partire da una lista di possibili risposte
        pass
    
    def generate_feedback_continue(self): #usiamo simpleNLG per generare risposte 
        #bisogna stare attenti agli ingredienti delle risposte dell'utente e quelli richiesti dal sistema per evitare ripetizioni
        pass
    
    def generate_end_exam_eval(self): #rispondiamo a partire da una lista di possibili risposte
        pass

    def generate_restart(self): #rispondiamo a partire da una lista di possibili risposte
        pass    