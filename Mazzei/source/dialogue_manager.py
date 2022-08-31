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
from tabulate import tabulate


class DialogueManager:
    """A class that manages the dialogue between the user and the system.
    """

    def __init__(self):
        self.potions_chosen = []
        self.memory = pd.DataFrame(columns=["Intent", "Answer", "Ingredients in potion", "Ingredients not in potion", "Expected", "Potion"], dtype=str)
        self.ingredients_available = None
        self.current_potion = pd.DataFrame()
        self.dialogue_context = DialogueContext(self.memory)
        self.dialogue_control = DialogueControl(self.dialogue_context)
        self.expected_current_answer = ""
        self.ingredients_potions_chosen = []

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
        random_indexes = list(random.sample(range(1, len(potions)), 3))


        for i in range(len(random_indexes)):
            potion_name = list(potions.keys())[random_indexes[i]]
            potion_ingredients = list(potions.values())[random_indexes[i]]
            df = self.create_potion_data_frame(potion_name, len(potion_ingredients))
            self.ingredients_potions_chosen.append(potion_ingredients)
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
        self.dialogue_context.set_current_potion(self.current_potion)
        self.dialogue_control.set_current_potion(self.current_potion, self.ingredients_potions_chosen[0])

        memory, intent, to_ask, expected = self.dialogue_control.manage_intent()
        self.memory = memory
        self.expected_current_answer = expected

        return intent
        

    def update_dialogue(self, last_answer: str, in_potion: list, out_potion: list, y_n: str):
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
        """
       
        current_intent = self.dialogue_control.get_current_intent()
        self.dialogue_context.update_memory(last_answer, current_intent, in_potion, out_potion, y_n, self.expected_current_answer) 
        memory, intent, to_ask, expected = self.dialogue_control.manage_intent()
        self.memory = memory
        self.expected_current_answer = expected
        # se l'intent è una domanda si no quindi con indice 2 o 3, allora si deve decidere anche l'ingrediente su cui si deve basare la domanda
        if intent == "ingredients_yes_no": 
            to_ask = self.choose_ingredient_general()
            # bisogna chiamare il generatore della risposta con un ingrediente random della lista totale ma che non sia stato detto dall'utente
        elif intent == "question_tricky": 
            to_ask = self.choose_ingredient_from_answer()
            # bisogna chiamare il generatore della risposta con un ingrediente detto dall'utente in risposta alla prima domanda

        #print("INTENT: ", intent)
        return self.memory, intent, to_ask

    def choose_ingredient_general(self):
        ingredients_to_choose = []
        for i in range(len(self.ingredients_available)):
            if not any(self.ingredients_available[i] in answer for answer in self.memory["Answer"].values):
            #if self.ingredients_available[i] not in self.memory["Answer"].values:
                ingredients_to_choose.append(self.ingredients_available[i])
        
        random_indexes = list(random.sample(range(len(ingredients_to_choose)), 1)) 
        return ingredients_to_choose[random_indexes[0]]

    def choose_ingredient_from_answer(self):
        #controllare risposta con riga dell'intent 1, gli ingredienti citati
        ingredient_to_ask = []
        name_potion = self.current_potion.columns[0] #nome della pozione
        row_ingredient_generic = self.memory.loc[self.memory["Potion"] == name_potion & self.memory["Intent"] == "ingredients_generic"]
        #crea una lista
        ingredients_mentioned = list(set(row_ingredient_generic["Ingredients in potion"][0] + row_ingredient_generic["Ingredients not in potion"][0]))
         
        #elimina gli ingredienti già chiesti eventualmente in domande con intent 2 o 3 precedentemente si ma devo averli in memoria!

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

    def __init__(self, dialogue_context):
        self.dialogue_context = dialogue_context 
        self.current_intent = -1

    def set_current_potion(self, current_potion: pd.DataFrame, ingredients_current_potion: list): 
        self.frame = current_potion
        self.ingredients_current_potion = ingredients_current_potion

    def manage_intent(self):
        """Manages the intent, implements automata. 

        Returns:
            memory (pd.DataFrame): The updated memory.
            intent (str): The intent of the question to ask.
            to_ask (str): The ingredient or potion to ask.   
            expected (str): Expecting the answer of the user.
        """

        memory = self.dialogue_context.memory

        print("memory in dialogue control: \n", tabulate(memory, headers='keys', tablefmt='psql'))

        are_correct, length = self.check_correct_current_potion(memory)
        length_interview = self.check_length_interview(memory)
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
            to_ask = self.frame.columns[0] # name of potion
            expected = ' '.join(self.ingredients_current_potion) # o non lo faccio, oppure devo trovare un modo per avere gli ingredienti veri della pozione
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
            random_index = list(random.sample([2, 4], 1)) #non determinist next state 2 or 4
            self.current_intent = random_index[0]
            if self.current_intent == 2:
                #prima scelgo gli ingredienti da chiedere
                expected = "ingredients_yes_no"
            else: 
                self.current_intent = 4
                #calcolo la valutazione
                expected = ""
        else:
            self.current_intent = -1
        
        return memory, self.INTENTS[self.current_intent], to_ask, expected


    def check_correct_current_potion(self, memory: pd.DataFrame): 
        """Checks if the student has answered correctly the current potion.
        
        Returns:
            bool: True if the ingredients of the current potion are correct, False otherwise.
            length: interview length for the current potion.
        """
        mistakes = True
        last_value = len(self.frame.index) - 1
        name_potion = self.frame.columns[0]
        #print("LUNGHEZZA :", last_value + 1, "\n \n")
        if last_value > 0:
            mistakes = pd.isna(self.frame.loc[last_value, name_potion]) # check if the last value is nan
        #print("MISTAKES: ", mistakes, "\n \n")

        memory_current_potion = memory.query("Potion == @name_potion") # get the current potion from the memory
        length = len(memory_current_potion.index) # get the length of the interview current potion

        #print("Length: ", length, "\n \n")
        return not mistakes, length
        

    def check_length_interview(self, memory: pd.DataFrame):
        """Checks the number of potions asked in the whole interview. 
            
        Returns:
            int: The number of potions asked in the whole interview.
        """
        
        length_interview = 0
        potions_asked = list(set(memory["Potion"].to_list())) # get the list of potions asked in the whole interview
        
        length_interview = len(potions_asked)
        print("print tabulate in check_length: \n ", tabulate(memory, headers='keys', tablefmt='psql'))
        print("length interview: ", length_interview, "\n \n")

        return length_interview

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
    def __init__(self, memory: pd.DataFrame):
        self.memory = memory
        
    def set_current_potion(self, current_potion: pd.DataFrame): 
        self.frame = current_potion

    def update_memory(self, answer: str, current_intent: str, in_potion: list, out_potion: list, y_n: str, expected: str):
        """ Updates the memory with the answer of the student.

        Args:
            answer (str): The answer of the student.
            current_intent (str): The current intent of the student.
            in_potion (list): The ingredients of the potion that the student is currently asking.
            out_potion (list): The ingredients of the potion that the student is currently asking.
            y_n (str): The answer of the student to the question y_n.
            expected (str): The expected answer of the student.
        """

#QUI C'è DA CAPIRE DA DOVE PRENDERE INGREDIENT, PERCHè SARà QUELLO MENZIONATO NELLA DOMANDA E NON SARà SEMPRE PRESENTE NELLA RISPOSTA
#        if current_intent == "" or current_intent == "": 
#            if y_n == expected:
#                number_correct.append(ingredient)
#            else:
#                number_incorrect.append(ingredient)
        

        self.memory = self.memory.append({'Intent': current_intent, 'Answer': answer, 
                'Ingredients in potion': ' '.join(in_potion), 'Ingredients not in potion': ' '.join(out_potion), 
                'Expected': expected, 'Potion': self.frame.columns[0]}, ignore_index=True)

        print("EXPECTED: \n \n", in_potion, "\n \n")
        print(tabulate(self.memory, headers='keys', tablefmt='psql'))
        #print("QUESTA è LA MEMORY AGGIORNATA: \n \n", self.memory.to_markdown(), "\n \n")