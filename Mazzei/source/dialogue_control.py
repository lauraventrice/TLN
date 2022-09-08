import pandas as pd
import random
from tabulate import tabulate


class DialogueControl: 
    """A class that manages how to continue the interaction, and
    defines the Intent based on the state of the memory
    """

    INTENTS = ["handshake", "ingredients_generic", "ingredients_yes_no", "question_tricky", "evaluation_end", "restart"]

    def __init__(self, dialogue_context, dialogue_manager):
        self.dialogue_context = dialogue_context 
        self.current_intent = -1
        self.remaining_ingredients_asked = False
        self.dialogue_manager = dialogue_manager
    
    def set_ingredient_available(self, ingredients_available: list):
        self.ingredients_available = ingredients_available

    def set_current_potion(self, current_potion: pd.DataFrame, ingredients_current_potion: list): 
        self.frame = current_potion
        self.ingredients_current_potion = ingredients_current_potion

    def set_potions_recipe(self, potions_recipe: dict):
        self.potions_recipe = potions_recipe

    def manage_intent(self):
        """Manages the intent, implements automata. 

        Returns:
            memory (pd.DataFrame): The updated memory.
            intent (str): The intent of the question to ask.
            to_ask (str): The ingredient or potion to ask.   
            expected (str): Expecting the answer of the user.
            name_potion (str): The name of the potion.
        """

        memory = self.dialogue_context.memory

        incomplete, length = self.check_correct_current_potion(memory)
        length_interview = self.check_length_interview(memory)
        expected = ""
        to_ask = ""

        number_of_potion = 2    # numero di pozioni da chiedere
        questions_for_potion = 3    # numero di domande da porre per ogni pozione

        if not incomplete: 
            self.current_intent = 4
            to_ask = self.get_evaluation(memory) 
        elif length > questions_for_potion and length_interview < number_of_potion: 
            self.current_intent = 5
            self.dialogue_manager.next_potion() 
            expected = ','.join(self.ingredients_current_potion) 
        elif length > questions_for_potion and length_interview == number_of_potion:
            self.current_intent = 4
            to_ask = self.get_evaluation(memory) 
        elif self.current_intent == -1:
            self.current_intent = 0 #handshake
            to_ask = "greeting"
            expected = "greeting"
        elif self.current_intent == 0: 
            self.current_intent = 1 #start asking ingredients
            to_ask = "start_ingredients_generic"
            expected = ','.join(self.ingredients_current_potion) 
        elif self.current_intent == 1 or self.current_intent == 5: #ingredients_generic or restart
            
            if self.remaining_ingredients_asked:
                next_state = range(2, 4)
            else:
                next_state = range(1, 4)

            random_index = list(random.sample(next_state, 1)) #non deterministic next state 1 or 2 or 3
            self.current_intent = random_index[0]

            if self.current_intent == 1: ## "What are the remaining ingredients?"
                to_ask = "remaining_ingredients"
                ingredients_in_frame = self.frame[self.frame.columns[0]].tolist()
                ingredients_in_frame = [ingredient for ingredient in ingredients_in_frame if not pd.isnull(ingredient)]
                print("INGREDIENTS IN FRAME: \n \n \n", ingredients_in_frame)
                remaining_ingredients = list(set(self.ingredients_current_potion).difference(set(ingredients_in_frame))) 
                expected = ','.join(remaining_ingredients)
                self.remaining_ingredients_asked = True
            elif self.current_intent == 2: ## "Is INGNAME in the ingredient list of the POTNAME potion?"
                to_ask = self.choose_ingredient_general() 
                if to_ask in self.ingredients_current_potion:
                    expected = "yes"
                else:
                    expected = "no"
                print("TO_ASK: \n \n", to_ask, " expected: ", expected, "\n \n \n")
            else: # question_tricky (self.current_intent == 3)
                if self.check_question_tricky_ingredient(memory):
                    possible_indexes = [0, 1]
                else: 
                    possible_indexes = [1]
                random_index = list(random.sample(possible_indexes, 1)) #non deterministic choose type of questions 
                if random_index[0] == 0: ## "Are you sure that this INGNAME is in the potion?"
                    to_ask = self.choose_ingredient_from_answer()
                    if to_ask in self.ingredients_current_potion:
                        expected = "yes"
                    else:
                        expected = "no"   
                else: ## "Are you sure you have mentioned all the ingredients?"
                    incomplete, _ = self.check_correct_current_potion(memory)
                    if incomplete:
                        expected = "no"
                    else: 
                        expected = "yes"  
                    to_ask = "question_tricky"
                print("TO_ASK: \n \n", to_ask, " expected: ", expected, "\n \n \n")
        elif self.current_intent == 2:
            if self.remaining_ingredients_asked:
                next_state = range(2, 5)
            else:
                next_state = range(1, 5)

            random_index = list(random.sample(next_state, 1)) #non deterministic next state 2 or 3 or 4
            self.current_intent = random_index[0] 
            if self.current_intent == 1:
                to_ask = "remaining_ingredients"
                ingredients_in_frame = self.frame[self.frame.columns[0]].tolist()
                ingredients_in_frame = [ingredient for ingredient in ingredients_in_frame if not pd.isnull(ingredient)]
                remaining_ingredients = list(set(self.ingredients_current_potion).difference(set(ingredients_in_frame))) 
                expected = ','.join(remaining_ingredients)
            elif self.current_intent == 2:
                to_ask = self.choose_ingredient_general() 
                if to_ask in self.ingredients_current_potion:
                    expected = "yes"
                else:
                    expected = "no"
            elif self.current_intent == 3: 
                if self.check_question_tricky_ingredient(memory):
                    possible_indexes = [0, 1]
                else: 
                    possible_indexes = [1]
                random_index = list(random.sample(possible_indexes, 1)) #non deterministic choose type of questions 
                if random_index[0] == 0: ## "Are you sure that this INGNAME is in the potion?"
                    to_ask = self.choose_ingredient_from_answer()
                    if to_ask in self.ingredients_current_potion:
                        expected = "yes"
                    else:
                        expected = "no"   
                else: ## "Are you sure you have mentioned all the ingredients?"
                    incomplete, _ = self.check_correct_current_potion(memory)
                    if incomplete:
                        expected = "no"
                    else: 
                        expected = "yes"
                    to_ask = "question_tricky"
            else: # (self.current_intent == 4)
                to_ask = self.get_evaluation(memory) 
        elif self.current_intent == 3:

            if self.remaining_ingredients_asked:
                next_state = [2, 4] 
            else:
                next_state = [1, 2, 4]

            random_index = list(random.sample(next_state, 1)) #non deterministic next state 1 or 2 or 4
            self.current_intent = random_index[0]
            if self.current_intent == 1:
                to_ask = "remaining_ingredients"
                ingredients_in_frame = self.frame[self.frame.columns[0]].tolist()
                ingredients_in_frame = [ingredient for ingredient in ingredients_in_frame if not pd.isnull(ingredient)]
                remaining_ingredients = list(set(self.ingredients_current_potion).difference(set(ingredients_in_frame)))
                expected = ','.join(remaining_ingredients)
            elif self.current_intent == 2:
                to_ask = self.choose_ingredient_general() 
                if to_ask in self.ingredients_current_potion:
                    expected = "yes"
                else:
                    expected = "no"
            else:
                self.current_intent = 4
                to_ask = self.get_evaluation(memory) 
        else:
            self.current_intent = -1
        
        return memory, self.INTENTS[self.current_intent], to_ask, expected, self.frame.columns[0]
    
    def check_question_tricky_ingredient(self, memory: pd.DataFrame):
        """ Check if is possible to ask question_tricky with an ingredient.
        
        Args:
            memory (pd.DataFrame): the memory of the dialogue.
        
        Returns:
            bool: True if is possible to ask question_tricky with an ingredient, False otherwise.
        """
        exists_mentioned = len(self.dialogue_context.ingredients_mentioned) > 0
        exists_ingredients_to_ask = len(list(set(self.dialogue_context.ingredients_mentioned).difference(set(memory["Ingredient asked"].unique().tolist())))) > 0
        return exists_mentioned and exists_ingredients_to_ask

    def choose_ingredient_general(self):
        """Chooses an ingredient to ask from the list of ingredients available without ingredients mentioned by the user.

        Returns:
            ingredient (str): The ingredient to ask.
        """
        ingredients_to_ask = list(set(self.ingredients_available).difference(set(self.dialogue_context.ingredients_mentioned)))
        
        random_indexes = list(random.sample(range(len(ingredients_to_ask)), 1)) 
        return ingredients_to_ask[random_indexes[0]]

    def choose_ingredient_from_answer(self):
        """ Chooses an ingredient to ask from the list of ingredients mentioned by the user.

        Returns:
            ingredient (str): The ingredient to ask.
        """
        
        ingredients_to_ask= list(set(self.dialogue_context.ingredients_mentioned).difference(set(self.dialogue_context.memory["Ingredient asked"].unique().tolist())))
        
        random_indexes = list(random.sample(range(len(ingredients_to_ask)), 1)) #
        return ingredients_to_ask[random_indexes[0]]

    def check_correct_current_potion(self, memory: pd.DataFrame): 
        """Checks if the student has answered correctly for the current potion.
        
        Args:
            memory (pd.DataFrame): The student's memory.
        Returns:
            incomplete (bool): True if there is some ingredients of the current potion that is missing, False otherwise.
            length (int): interview length for the current potion.
        """
        incomplete = True
        last_value = len(self.frame.index) - 1
        name_potion = self.frame.columns[0]

        #if last_value > 0:
        print(self.frame.loc[last_value, name_potion])
        incomplete = pd.isna(self.frame.loc[last_value, name_potion]) # check if the last value is nan

        memory_current_potion = memory.query("Potion == @name_potion") # get the current potion from the memory
        length = len(memory_current_potion.index) # get the length of the interview current potion

        return incomplete, length
        

    def check_length_interview(self, memory: pd.DataFrame):
        """Checks the number of potions asked in the whole interview. 

        Args:
            memory (pd.DataFrame): The memory of the student.

        Returns:
            int: The number of potions asked in the whole interview.
        """
        
        length_interview = 0
        potions_asked = list(set(memory["Potion"].to_list())) # get the list of potions asked in the whole interview
        
        length_interview = len(potions_asked)
        print("length interview: ", length_interview, "\n \n")

        return length_interview

    def get_current_intent(self): 
        return self.INTENTS[self.current_intent]

    def get_evaluation(self, memory: pd.DataFrame):
        """Gets the evaluation of the conversation based on the memory.
            The scale of grades is: 
                E (Excellent)
                S (Satisfactory)
                M (Mediocre)
                I (Insufficient)
                F (Failure)
        Args:
            memory (pd.DataFrame): The memory of the student.

        Returns:
            evaluation (str): The evaluation of the conversation.
        """

        potions_list = memory["Potion"].unique()   # potions asked in the whole interview

        print("POTIONS LIST: ", potions_list)

        evaluation_list = []

        for potion in potions_list:

            count_correct = 0
            count_incorrect = 0
            count_indiff = 0
 
            rows_of_potion = memory.loc[memory['Potion'] == potion]    # rows of the interview of the potion

            potion_recipe = self.potions_recipe[potion]

            for i in rows_of_potion.index:

                correct_ingredients = [ingredient for ingredient in rows_of_potion.loc[i, "Correct ingredients"].split(",") if ingredient != ""]
                count_correct += len(correct_ingredients)

                incorrect_ingredients = [ingredient for ingredient in rows_of_potion.loc[i, "Incorrect ingredients"].split(",") if ingredient != ""]
                count_incorrect += len(incorrect_ingredients)

                indifferent_ingredients = [ingredient for ingredient in rows_of_potion.loc[i, "Indifferent ingredients"].split(",") if ingredient != ""]
                count_indiff += len(indifferent_ingredients)

            not_mentioned_correct_ingredients = list(set(potion_recipe).difference(set(correct_ingredients)))

            evaluation = count_correct / (count_correct + count_incorrect + count_indiff) - len(not_mentioned_correct_ingredients) * 0.1
            print("EVALUATION ", potion, ": ", evaluation)

            evaluation_list.append(evaluation)

        evaluation = round(sum(evaluation_list) / len(evaluation_list), 2) 

        print("FINAL EVALUATION ", evaluation)


        if evaluation >= 0.8:
            evaluation = "excellent"
        elif evaluation > 0 and evaluation < 0.8:
            evaluation = "satisfactory"
        elif evaluation == 0:
            evaluation = "mediocre"
        elif evaluation < 0 and evaluation > -0.8:
            evaluation = "insufficient"
        elif evaluation <= -0.8:
            evaluation = "failure"
        
        return evaluation