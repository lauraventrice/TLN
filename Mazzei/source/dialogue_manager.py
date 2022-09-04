import pandas as pd
import random
from tabulate import tabulate
from dialogue_context import DialogueContext
from dialogue_control import DialogueControl

class DialogueManager:
    """A class that manages the dialogue between the user and the system.
    """

    def __init__(self):
        self.potions_chosen = []
        self.memory = pd.DataFrame(columns=["Intent", "Ingredient asked", "Answer", "Correct ingredients", "Incorrect ingredients", "Indifferent ingredients", "Expected", "Potion"], dtype=str)
        self.ingredients_available = None
        self.current_potion = pd.DataFrame()
        self.dialogue_context = DialogueContext(self.memory)
        self.dialogue_control = DialogueControl(self.dialogue_context, self)
        self.expected_current_answer = ""
        self.ingredients_potions_chosen = []
        self.index_current_potion = -1

    def create_potion_data_frame(self, column_name: str, row_num: int):
        """Creates a data frame with the given column name and row number.

        Args:
            column_name (str): The name of the column, aka the name of the potion.
            row_num (int): The number of rows in the data frame, which is the number of ingredients of the potion. 
        
        Returns:
            pandas.DataFrame: The data frame that will represent the potion with its ingredients.
        """
        df = pd.DataFrame(index=range(row_num),columns=[column_name], dtype=str)
        return df

    def choose_potions(self, potions: dict):
        """Chooses 3 random potions from the given dictionary.

        Args:
            potions (dict): The dictionary with the potions available with ingredients.
        """
        #random_indexes = list(random.sample(range(1, len(potions)), 3))
        #sentence = I think that Fluxweed, Rose Thorn, Chinese Chomping cabbage and Caterpillar are in the potion.
        random_indexes = [0, 1, 2]    # questo serve solo per testare -> rimuovere e rimettere l'indice random
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
        self.dialogue_control.set_ingredient_available(ingredients)
        print("INGREDIENTS AVAILABLE: \n", self.ingredients_available)

    def next_potion(self):
        """Gets the next potion to ask.
        """

        self.index_current_potion += 1

        self.current_potion = self.potions_chosen[self.index_current_potion]

        self.dialogue_context.set_current_potion(self.current_potion, self.ingredients_potions_chosen[self.index_current_potion])
        self.dialogue_control.set_current_potion(self.current_potion, self.ingredients_potions_chosen[self.index_current_potion])

    def start_dialogue(self):
        """Starts the dialogue.

        Returns:
            intent (int): The intent of the first question to ask.
        """
        self.index_current_potion = 0
        self.current_potion = self.potions_chosen[self.index_current_potion]
        self.dialogue_context.set_current_potion(self.current_potion, self.ingredients_potions_chosen[0])
        self.dialogue_control.set_current_potion(self.current_potion, self.ingredients_potions_chosen[0])

        memory, intent, to_ask, expected, _ = self.dialogue_control.manage_intent()
        self.memory = memory
        self.expected_current_answer = expected

        return intent, to_ask
        

    def update_dialogue(self, ingredient_asked: str, last_answer: str, in_potion: list, out_potion: list, y_n: str):
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
        self.dialogue_context.update_memory(ingredient_asked, last_answer, current_intent, in_potion, out_potion, y_n, self.expected_current_answer) 
        memory, intent, to_ask, expected, name_potion = self.dialogue_control.manage_intent()
        self.memory = memory
        self.expected_current_answer = expected
           
        return self.memory, intent, to_ask, name_potion