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
        #creare oggetto DialogueContext e DialogueControl?
        

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
        """
        # Parte 3!
        # prima verrà chiamato dialog context che ci restiuirà la memoria 
        # poi verrà chiamato dialog control che ci restituirà l'intent che dovrà avere la risposta
        # e il discourse planning
        pass

    def update_dialogue(self, last_answer: str, claims: list, negatives: list, neutrals: list):
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


    # qui ci dovrebbe essere l'automa di cui abbiamo parlato?
    # sarà presente un current state 
    #TODO 1. se si risponde alla prima giusto subito si chiede un'altra pozione
    #TODO 2. se le prime due sono corrette si da punteggio pieno
    #TODO 3. se non si risponde con almeno la metà degli ingredienti corretti si va avanti???
    # dovrà restituire l'intent scelto in base allo stato della conversazione
    # e dovrà restituire il discourse planning --- bisogna restituire i futuri parametri per SIMPLE NLG!!!



class DialogueContext: 
    """A class that is responsible for maintaining the information that is useful for the performance of the dialogue. 
    Specifically common ground by the system via Intents and by the user with Memory and Frames. 
    """

    def add_answer(self, answer: str, current_intent: str):
        pass