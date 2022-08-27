#Dialog control: definisce l'Intent sulla base della memoria

#Dialog context: mantiene lo storico della conversazione, la common ground, 
#con una memoria dell'interazione, frame delle pozioni e intent per il tipo di domanda

# si sceglie la pozione su cui interrogare, processa l'input e aggiorna la memoria

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
        self.memory = pd.DataFrame(columns=["Intent", "Answer", "Number correct ingredients", "Number wrong ingredients", "Expected"])
        self.ingredients_available = None
        self.current_potion = None
        self.dialogue_context = DialogueContext(self.memory)
        self.dialogue_control = DialogueControl(self.memory, self.current_potion)
        

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
        # Parte 2
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
        self.current_potion = 0
        intent = self.dialogue_control.manage_intent()

        return intent
        

    def update_dialogue(self, last_answer: str, claims: list, negatives: list, neutrals: list):
        # Parte 3!
        self.dialogue_context.update_memory() 
        intent = self.dialogue_control.manage_intent()
        # se l'intent è una domanda si no quindi con indice 2 o 3, allora si deve decidere anche l'ingrediente su cui si deve basare la domanda
        if intent == 2: 
            ingredient = self.choose_ingredient_general()
            # bisogna chiamare il generatore della risposta con un ingrediente random della lista totale ma che non sia stato detto dall'utente
        elif intent == 3: 
            ingredient = self.choose_ingredient_from_answer()
            # bisogna chiamare il generatore della risposta con un ingrediente detto dall'utente in risposta alla prima domanda

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
            str: The intent of the question to ask. 
        """

        if self.current_intent == -1:
            self.current_intent = 0

        """
        are_correct, length = self.check_correct_current_potion()
        length_interview = self.check_length_interview()

        #controlla la memoria se abbiamo fatto 4 domande ferma la conversazione fai il voto
        if are_correct: #appena ne fa giusta una finisce la conversazione
            self.current_intent = 4
        elif length > 3 and length_interview < 3: #facciamo restart solo se abbiamo fatto 4 domande, ha ancora qualcosa di sbagliato e non abbiamo ancora chiesto 3 pozioni
            self.current_intent = 5
        elif length > 3 and length_interview == 3:
            self.current_intent = 4
        elif self.current_intent == -1:
            self.current_intent = 0 #handshake
        elif self.current_intent == 0: 
            self.current_intent = 1 #start asking ingredients
        elif self.current_intent == 1 or self.current_intent == 5: #ingredients_generic or restart
            random_index = list(random.sample(range(2, 4), 1)) #non determinist next state 2 or 3
            self.current_intent = random_index[0] #2 or 3
        elif self.current_intent == 2:
            random_index = list(random.sample(range(2, 5), 1)) #non determinist next state 2 or 3 or 4
            self.current_intent = random_index[0] #2 or 3 or 4
        elif self.current_intent == 3:
            random_index = list(random.sample(range(1), 1)) #non determinist next state 2 or 3
            if random_index[0] == 0:
                self.current_intent = 2 #2 or 4
            else: 
                self.current_intent = 4
        else:
            self.current_intent = -1
        """
        return self.INTENTS[self.current_intent]


    def check_correct_current_potion(self): 
        """Checks if the student has answered correctly the current potion.
        
        Returns:
            bool: True if the ingredients of the current potion are correct, False otherwise.
        """
        
        #controllare il frame se è pieno della current potion se è pieno
        pass

    def check_length_interview(self):
        """Checks the number of potions asked in the whole interview. 
        
        Returns:
            int: The number of potions asked in the whole interview.
        """

        # sarebbe quanti valori differenti sono presenti nella colonna della current_potion dellla memoria
        pass

class DialogueContext: 
    """A class that is responsible for maintaining the information that is useful for the performance of the dialogue. 
    Specifically common ground by the system via Intents and by the user with Memory and Frames. 
    """
    def __init__(self, memory: pd.DataFrame):
        self.memory = memory
        self.frames = []

    def update_memory(self, answer: str, current_intent: str, number_correct_ingredients: int, number_wrong_ingredients: int, expected: str):
        pass