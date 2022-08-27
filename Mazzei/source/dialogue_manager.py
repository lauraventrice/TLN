# Parte 1: INIT!
# - funzione che carica un file con tutte le pozioni
# - crea dizionario con chiave nome della pozione e valore lista ingredienti
# - crea lista di ingredienti completa

# Parte 2:
# - scelta di 3 pozioni random dal dizionario
# - creazione dei frame relativi alle pozioni solo con nome e campi vuoti (forse sarà un oggetto??)

# Parte 3:
# - gestione degli intent tipo automa, come se fosse lo stato della conversazione, dataflow: 
#   1. handshake
#   2. chiedi ingredienti ("Quali sono gli ingredienti di questa pozione?" oppure "Quali sono il resto degli ingredienti?" oppure "Quindi quali sono gli ingredienti?") 
#   2. chiedi se un particolare ingrediente è presente negli ingredienti della pozione (PIù DI UNA VOLTA)
#   3. chiede se è sicuro della presenza di un ingrediente citato precedentemente o se sono stati citati tutti (SI DEVE POI RITORNARE A 2 o 4)
#   4. evaluation con voto e mini commento 
#   4. chiedi gli ingredienti di un'altra pozione (restart) 


# Parte 4:
# - gestione della memoria con intent-domanda-risposta DECIDERE

import pandas as pd
import random


class DialogueManager:
    """A class that manages the dialogue between the user and the system.
    """

    def __init__(self):
        self.potions_chosen = []
        self.memory = pd.DataFrame(columns=["Intent", "Answer", "Ingredients in potion", "Ingrediends not in potion", "Expected", "Potion"], dtype=str)
        self.ingredients_available = None
        self.current_potion = pd.DataFrame()
        self.dialogue_context = DialogueContext(self.memory, self.current_potion)
        self.dialogue_control = DialogueControl(self.memory, self.current_potion)
        self.expected_current_answer = ""
        

    def create_potion_data_frame(self, column_name: str, row_num: int):
        """Creates a data frame with the given column name and row number.

        Args:
            column_name (str): The name of the column, aka the name of the potion.
            row_num (int): The number of rows in the data frame, which is the number of ingredients of the potion. 
        
        Returns:
            pandas.DataFrame: The data frame that will represent the potion with its ingredients.
        """
        df = pd.DataFrame(index=range(row_num),columns=[column_name])
        return df

    def choose_potions(self, potions: dict):
        """Chooses 3 random potions from the given dictionary.

        Args:
            potions (dict): The dictionary with the potions available with ingredients.
        """
        random_indexes = list(random.sample(range(1, len(potions)), 3)) #TODO: controllare che gli indici sono diversi quando si genera 

        for i in range(len(random_indexes)):
            potion_name = list(potions.keys())[random_indexes[i]]
            potion_ingredients = list(potions.values())[random_indexes[i]]
            df = self.create_potion_data_frame(potion_name, len(potion_ingredients))
            self.potions_chosen.append(df)
        
        print("POTIONS CHOSEN: \n", self.potions_chosen)

    def set_ingredients(self, ingredients: list):
        """Sets the ingredients of the potions.
        
        Args:
            ingredients (list): The list of the ingredients of the potions.
        """
        self.ingredients_available = ingredients
        print("INGREDIENTS AVAILABLE: \n", self.ingredients_available)


    def start_dialogue(self):
        """Starts the dialogue.

        Returns:
            intent (int): The intent of the first question to ask.
        """
        self.current_potion = self.potions_chosen[0]
        memory, intent, to_ask, expected = self.dialogue_control.manage_intent()

        self.expected_current_answer = expected

        return intent
        

    def update_dialogue(self, last_answer: str, in_potion: list, not_in_potion: list, y_n: str):
        """Update dialogue, adding the last answer to the memory with all information from understanding.

        Args:
            last_answer (str): The last answer of the user.
            in_potion (list): The ingredients of the potion that are mentioned as in the potion.
            not_in_potion (list): The ingredients of the potion that are mentioned as not in the potion.
            y_n (str): The answer of the user to the questions about the ingredients.

        Returns:
            memory (pandas.DataFrame): The updated memory.
            intent (str): The intent of the next question to ask.
            to_ask (str) or potion (str): The ingredient to ask or the potion to ask. 
            potion_to_ask (str): The potion asked in the exam.
        """
       
        current_intent = self.dialogue_control.get_current_intent()
        self.dialogue_context.update_memory(last_answer, current_intent, in_potion, not_in_potion, y_n, self.expected_current_answer) 
        memory, intent, to_ask, expected = self.dialogue_control.manage_intent()
        self.expected_current_answer = expected
        # se l'intent è una domanda si no quindi con indice 2 o 3, allora si deve decidere anche l'ingrediente su cui si deve basare la domanda
        if intent == "ingredients_yes_no": 
            ingredient = self.choose_ingredient_general()
            # bisogna chiamare il generatore della risposta con un ingrediente random della lista totale ma che non sia stato detto dall'utente
        elif intent == "question_tricky": 
            ingredient = self.choose_ingredient_from_answer()
            # bisogna chiamare il generatore della risposta con un ingrediente detto dall'utente in risposta alla prima domanda

        return self.memory, intent, to_ask

    def choose_ingredient_general(self):
        ingredients_to_choose = []
        for i in range(len(self.ingredients_available)):
            if self.ingredients_available[i] not in self.memory["Answer"].values:
                ingredients_to_choose.append(self.ingredients_available[i])
        
        random_indexes = list(random.sample(range(len(ingredients_to_choose)), 1)) 
        return random_indexes[0]

    def choose_ingredient_from_answer(self):
        #controllare risposta con riga dell'intent 1, gli ingredienti citati
        
        #crea una lista

        #elimina gli ingredienti già chiesti eventualmente in domande con intent 2 o 3 precedentemente

        #scegli casuale e restituisci l'ingrediente da chiedere
        pass


    # Tentativo di inserimento di un valore in un dataframe
    # print(data_frame_list[0].columns[0])
    # data_frame_list[0].at[0, data_frame_list[0].columns[0]] = "CIAO"
    # print(data_frame_list)


class DialogueControl: 
    """A class that manages how to continue the interaction, and
    defines the Intent based on the state of the memory
    """

    INTENTS = ["handshake", "ingredients_generic", "ingredients_yes_no", "question_tricky", "evaluation_end", "restart"]

    def __init__(self, memory: pd.DataFrame, current_potion: pd.DataFrame):
        self.memory = memory
        self.current_intent = -1
        self.current_potion = current_potion

    def manage_intent(self):
        """Manages the intent, implements automata. 

        Returns:
            memory (pd.DataFrame): The updated memory.
            intent (str): The intent of the question to ask.
            to_ask (str): The ingredient or potion to ask.   
            expected (str): Expecting the answer of the user.
        """

        are_correct, length = self.check_correct_current_potion()
        length_interview = self.check_length_interview()
        expected = ""
        to_ask = ""
        #controlla la memoria se abbiamo fatto 4 domande ferma la conversazione fai il voto
        if are_correct: #appena ne fa giusta una finisce la conversazione
            self.current_intent = 4
            #calcola la valutazione della conversazione
            expected = "end"
        elif length > 3 and length_interview < 3: #facciamo restart solo se abbiamo fatto 4 domande, ha ancora qualcosa di sbagliato e non abbiamo ancora chiesto 3 pozioni
            self.current_intent = 5
            expected = "restart"
        elif length > 3 and length_interview == 3:
            self.current_intent = 4
            #calcola la valutazione della conversazione
            expected = "end"
        elif self.current_intent == -1:
            self.current_intent = 0 #handshake
            to_ask = ""
            expected = "greeting"
        elif self.current_intent == 0: 
            self.current_intent = 1 #start asking ingredients
            to_ask = self.current_potion.columns[0]
            expected = ' '.join(self.current_potion.values) #qua ci deve essere la stringa con tutti gli ingredienti presenti

        elif self.current_intent == 1 or self.current_intent == 5: #ingredients_generic or restart
            random_index = list(random.sample(range(2, 4), 1)) #non determinist next state 2 or 3
            self.current_intent = random_index[0] #2 or 3
            if self.current_intent == 2:
                #prima scelgo gli ingredienti da chiedere
                expected = "ingredients_yes_no"
            else: 
                #prima scelgo gli ingredienti da chiedere
                expected = ""    
        elif self.current_intent == 2:
            random_index = list(random.sample(range(2, 5), 1)) #non determinist next state 2 or 3 or 4
            self.current_intent = random_index[0] #2 or 3 or 4
            if self.current_intent == 2:
                #prima scelgo gli ingredienti da chiedere
                expected = "ingredients_yes_no"
            elif self.current_intent == 3: 
                #prima scelgo gli ingredienti da chiedere
                expected = ""
            else:
                #calcolo la valutazione
                expected = ""
        elif self.current_intent == 3:
            random_index = list(random.sample(range(2), 1)) #non determinist next state 2 or 3
            if random_index[0] == 0:
                self.current_intent = 2 #2 or 4
                expected = "ingredients_yes_no"
            else: 
                self.current_intent = 4
                #calcolo la valutazione
                expected = ""
        else:
            self.current_intent = -1
        
        return self.memory, self.INTENTS[self.current_intent], to_ask, expected


    def check_correct_current_potion(self): 
        """Checks if the student has answered correctly the current potion.
        
        Returns:
            bool: True if the ingredients of the current potion are correct, False otherwise.
            length: interview length for the current potion.
        """
        mistakes = True
        i = len(self.current_potion) - 1
        if i > 0:
            mistakes = pd.isna(self.current_potion.loc[i, self.current_potion.columns[0]]) # check if the last value is nan
        return not mistakes, i + 1
        

    def check_length_interview(self):
        """Checks the number of potions asked in the whole interview. 
            
        Returns:
            int: The number of potions asked in the whole interview.
        """
        
        length = 0
        if len(self.current_potion) > 0:
            name_current_potion = self.current_potion.columns[0]
            change_zero = self.memory["Potion"].where(self.memory != name_current_potion, 0)
            result = change_zero["Potion"].where(change_zero == name_current_potion, 1)
            length = result["Potion"].sum()
        return length

    def get_current_intent(self): 
        return self.INTENTS[self.current_intent]

    def get_evaluation(self):
        """Gets the evaluation of the conversation based on the memory.
        """
        pass

class DialogueContext: 
    """A class that is responsible for maintaining the information that is useful for the performance of the dialogue. 
    Specifically common ground by the system via Intents and by the user with Memory and Frames. 
    """
    def __init__(self, memory: pd.DataFrame, current_potion: pd.DataFrame):
        self.memory = memory
        self.frame = current_potion

    def update_memory(self, answer: str, current_intent: str, in_potion: list, not_in_potion: list, y_n: str, expected: str):
        
        number_correct = []
        number_incorrect = []
        for ingredient in in_potion: 
            if ingredient in self.memory.values:
                number_correct.append[ingredient]
            else: 
                number_incorrect.append[ingredient]
        
        for ingredient in not_in_potion:
            if ingredient in self.memory.values:
                number_incorrect.append(ingredient)
            else: 
                number_correct.append(ingredient)

#QUI C'è DA CAPIRE DA DOVE PRENDERE INGREDIENT, PERCHè SARà QUELLO MENZIONATO NELLA DOMANDA E NON SARà SEMPRE PRESENTE NELLA RISPOSTA
#        if current_intent == "" or current_intent == "": 
#            if y_n == expected:
#                number_correct.append(ingredient)
#            else:
#                number_incorrect.append(ingredient)
        

        self.memory.append({'Intent': current_intent, 'Answer': answer, 
                'In potion': ' '.join(in_potion), 'Not in potion': ' '.join(not_in_potion), 
                'Expected': expected, 'Potion': self.frame.columns[0]})

        print("QUESTA è LA MEMORY AGGIORNATAAAA: \n \n", self.memory)