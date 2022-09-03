import pandas as pd
import random
from tabulate import tabulate


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

        self.dialogue_context.set_current_potion(self.current_potion)
        self.dialogue_control.set_current_potion(self.current_potion, self.ingredients_potions_chosen[self.index_current_potion])

    def start_dialogue(self):
        """Starts the dialogue.

        Returns:
            intent (int): The intent of the first question to ask.
        """
        self.index_current_potion = 0
        self.current_potion = self.potions_chosen[self.index_current_potion]
        self.dialogue_context.set_current_potion(self.current_potion)
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

        print("memory in dialogue control: \n", tabulate(memory, headers='keys', tablefmt='psql'))

        incomplete, length = self.check_correct_current_potion(memory)
        length_interview = self.check_length_interview(memory)
        expected = ""
        to_ask = ""

        if not incomplete: 
            self.current_intent = 4
            to_ask = self.get_evaluation(memory) #TODO: calcolo la valutazione
            expected = ""
        elif length > 4 and length_interview < 3: 
            self.current_intent = 5
            self.dialogue_manager.next_potion() # TODO: chiedere la nuova pozione
            expected = ','.join(self.ingredients_current_potion) 
        elif length > 4 and length_interview == 3:
            self.current_intent = 4
            to_ask = self.get_evaluation(memory) #TODO: calcolo la valutazione
            expected = ""
        elif self.current_intent == -1:
            self.current_intent = 0 #handshake
            to_ask = "greeting"
            expected = "greeting"
        elif self.current_intent == 0: 
            self.current_intent = 1 #start asking ingredients
            to_ask = "start_ingredients_generic"
            expected = ','.join(self.ingredients_current_potion) 
        elif self.current_intent == 1 or self.current_intent == 5: #ingredients_generic or restart
            
            # if self.remaining_ingredients_asked:
            #     next_state = range(2, 4)
            # else:
            #     next_state = range(1, 4)

            # momentaneamente andiamo solo in 1
            next_state = [4]

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
                random_index = list(random.sample(range(0, 2), 1)) #non deterministic choose type of questions 
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
                print("INGREDIENTS IN FRAME: \n \n \n", ingredients_in_frame)
                remaining_ingredients = list(set(self.ingredients_current_potion).difference(set(ingredients_in_frame))) 
                expected = ','.join(remaining_ingredients)
            elif self.current_intent == 2:
                to_ask = self.choose_ingredient_general() 
                if to_ask in self.ingredients_current_potion:
                    expected = "yes"
                else:
                    expected = "no"
            elif self.current_intent == 3: 
                random_index = list(random.sample(range(0, 2), 1)) #non deterministic choose type of questions 
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
                to_ask = self.get_evaluation(memory) #TODO: calcolo la valutazione
                expected = ""
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
                print("INGREDIENTS IN FRAME: \n \n \n", ingredients_in_frame)
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
                to_ask = self.get_evaluation(memory) #TODO: calcolo la valutazione
                expected = ""
        else:
            self.current_intent = -1
        
        return memory, self.INTENTS[self.current_intent], to_ask, expected, self.frame.columns[0]

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
        
        random_indexes = list(random.sample(range(len(ingredients_to_ask)), 1)) 
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
        #print("LUNGHEZZA :", last_value + 1, "\n \n")
        if last_value > 0:
            incomplete = pd.isna(self.frame.loc[last_value, name_potion]) # check if the last value is nan
        #print("MISTAKES: ", mistakes, "\n \n")

        memory_current_potion = memory.query("Potion == @name_potion") # get the current potion from the memory
        length = len(memory_current_potion.index) # get the length of the interview current potion

        #print("Length: ", length, "\n \n")
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
        print("print tabulate in check_length: \n ", tabulate(memory, headers='keys', tablefmt='psql'))
        print("length interview: ", length_interview, "\n \n")

        return length_interview

    def get_current_intent(self): 
        return self.INTENTS[self.current_intent]

    def get_evaluation(self, memory: pd.DataFrame):
        """Gets the evaluation of the conversation based on the memory.

        Args:
            memory (pd.DataFrame): The memory of the student.

        Returns:
            evaluation (str): The evaluation of the conversation.
        """

        count_correct = 0
        count_incorrect = 0
        count_indiff = 0
        
        print("memory index: ", memory.index)
        for i in memory.index:
            print("\n \n correct ingredients count: ", memory.loc[i, "Correct ingredients"].split(","))
            count_correct += len(memory.loc[i, "Correct ingredients"].split(","))
            print("\n \n incorrect ingredients count: ", memory.loc[i, "Incorrect ingredients"].split(","))
            count_incorrect += len(memory.loc[i, "Incorrect ingredients"].split(","))
            print("\n \n indifferent ingredients count: ", memory.loc[i, "Indifferent ingredients"].split(","))
            count_indiff += len(memory.loc[i, "Indifferent ingredients"].split(","))
        
        evaluation = (count_correct - count_incorrect) / (count_correct + count_incorrect + count_indiff)
        
        print("count_correct: ", count_correct)
        print("count_incorrect: ", count_incorrect)
        print("count_indiff: ", count_indiff)

        print("EVALUATION: ", evaluation)

        if evaluation >= 2:
            evaluation = "excellent"
        elif evaluation > 0 and evaluation < 2:
            evaluation = "satisfactory"
        elif evaluation == 0:
            evaluation = "mediocre"
        elif evaluation < 0 and evaluation > -2:
            evaluation = "insufficient"
        elif evaluation <= -2:
            evaluation = "failure"
        
        """
        E (Excellent)
        S (Satisfactory)
        M (Mediocre)
        I (Insufficient)
        F (Failure)
        """
        return evaluation

class DialogueContext: 
    """A class that is responsible for maintaining the information that is useful for the performance of the dialogue. 
    Specifically common ground by the system via Intents and by the user with Memory and Frames. 
    """
    def __init__(self, memory: pd.DataFrame):
        self.memory = memory
        
    def set_current_potion(self, current_potion: pd.DataFrame): 
        self.frame = current_potion
        self.index = 0
        self.ingredients_mentioned = []

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
        indifferent_ingredient = []
        if current_intent == "ingredients_generic":
            ingredients_potion = expected.split(",")
            print("&&&&&&&&&&&&&&&&& ingredients_potion: " , ingredients_potion, "\n \n")
            for ingredient in in_potion:
                if ingredient in ingredients_potion:
                    correct_ingredients.append(ingredient)
                    if not ingredient in self.frame[self.frame.columns[0]].unique().tolist():
                        print(" \n \n l'ingrediente non è già presente nel frame! \n \n")
                        self.frame.loc[self.index, self.frame.columns[0]] = ingredient
                        print("\n \n Frame aggiornato: \n \n ", self.frame, "\n \n")
                        self.index += 1
                else:
                    incorrect_ingredients.append(ingredient)

            for ingredient in out_potion:
                if ingredient not in ingredients_potion:
                    indifferent_ingredient.append(ingredient)
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
        
        self.ingredients_mentioned = list(set(self.ingredients_mentioned + in_potion + out_potion + indifferent_ingredient))

        self.memory = self.memory.append({'Intent': current_intent, 'Ingredient asked' : ingredient_asked, 'Answer': answer, 
                'Correct ingredients': ','.join(correct_ingredients), 'Incorrect ingredients': ','.join(incorrect_ingredients), 
                'Indifferent ingredients': ','.join(indifferent_ingredient),
                'Expected': expected, 'Potion': self.frame.columns[0]}, ignore_index=True)

        print("EXPECTED: \n \n", expected, "\n \n")
        print("Correct ingredients: \n \n", correct_ingredients, "\n \n")
        print(tabulate(self.memory, headers='keys', tablefmt='psql'))
        #print("QUESTA è LA MEMORY AGGIORNATA: \n \n", self.memory.to_markdown(), "\n \n")