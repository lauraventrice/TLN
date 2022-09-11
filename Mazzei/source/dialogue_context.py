import pandas as pd
from tabulate import tabulate

class DialogueContext: 
    """A class that is responsible for maintaining the information that is useful for the performance of the dialogue. 
    Specifically common ground by the system via Intents and by the user with Memory and Frames. 
    """
    def __init__(self, memory: pd.DataFrame):
        self.memory = memory
        
    def set_current_potion(self, current_potion: pd.DataFrame, ingredient_current_potion: list): 
        self.frame = current_potion
        self.index = 0
        self.ingredients_mentioned = []
        self.ingredients_current_potion = ingredient_current_potion

    def update_memory(self, ingredient_asked: str, answer: str, current_intent: str, in_potion: list, out_potion: list, y_n: str, expected: str):
        """ Updates the memory with the answer of the student.

        Args:
            answer (str): The answer of the student.
            current_intent (str): The current intent of the student.
            in_potion (list): The ingredients of the potion that the student is currently asking.
            out_potion (list): The ingredients of the potion that the student is currently asking.
            y_n (str): The answer of the student to the question y_n.
            expected (str): The expected answer of the student.
        """

        correct_ingredients = []
        incorrect_ingredients = []
        indifferent_ingredients = []
        if current_intent == "ingredients_generic" or current_intent == "restart":
            ingredients_potion_expected = expected.split(",")
            for ingredient in in_potion:
                if ingredient in self.ingredients_current_potion and ingredient in ingredients_potion_expected:
                    correct_ingredients.append(ingredient)
                    if not ingredient in self.frame[self.frame.columns[0]].unique().tolist():
                        self.frame.loc[self.index, self.frame.columns[0]] = ingredient
                        self.index += 1
                elif not ingredient in self.ingredients_current_potion:
                    incorrect_ingredients.append(ingredient)
                else: 
                    indifferent_ingredients.append(ingredient)

            for ingredient in out_potion:
                if ingredient not in ingredients_potion_expected:
                    indifferent_ingredients.append(ingredient)
                else: 
                    incorrect_ingredients.append(ingredient)
        
        elif current_intent == "ingredients_yes_no" or current_intent == "question_tricky": 
            if ingredient_asked != "":
                if y_n == expected:
                    correct_ingredients.append(ingredient_asked)
                else: 
                    incorrect_ingredients.append(ingredient_asked)
            else: 
                if y_n == expected:
                    correct_ingredients.append("x")
                else: 
                    incorrect_ingredients.append("x")
        
        self.ingredients_mentioned = list(set(self.ingredients_mentioned + in_potion + out_potion + indifferent_ingredients))

        self.memory = self.memory.append({'Intent': current_intent, 'Ingredient asked' : ingredient_asked, 'Answer': answer, 
                'Correct ingredients': ','.join(correct_ingredients), 'Incorrect ingredients': ','.join(incorrect_ingredients), 
                'Indifferent ingredients': ','.join(indifferent_ingredients),
                'Expected': expected, 'Potion': self.frame.columns[0]}, ignore_index=True)

        # PRINT MEMORY
        # print(tabulate(self.memory, headers='keys', tablefmt='grid'))